"""Isolated local timing/RSS baseline; never substitutes for offline container tests."""
import argparse
import hashlib
import importlib.metadata
import os
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time


def scaling_task(count, width, height):
    columns = math.ceil(math.sqrt(count))
    rows = math.ceil(count / columns)
    return {'source': {'canvas': {'width': columns * 200, 'height': rows * 100},
            'elements': [dict(id=f'label-{i}', type='text', x=(i % columns)*200+10,
                              y=(i // columns)*100+10, width=180, height=80,
                              content=f'Item {i+1}', font_family='Solstice Sans',
                              font_size=24, color='rgba(0,0,0,1)') for i in range(count)]},
            'target_canvas': {'width': width, 'height': height}}


def peak_rss_bytes(value, system):
    # getrusage is bytes on Darwin, KiB on Linux. Do not guess other OS units.
    if system == 'Darwin':
        return int(value)
    if system == 'Linux':
        return int(value * 1024)
    return None


def worker(task_path, destination, repetitions):
    started = time.perf_counter()
    from engine.resize import resize_with_diagnostics
    from renderer.converter.convert import render_design_to_png
    import_seconds = time.perf_counter()-started
    import copy
    import cProfile
    import pstats
    import resource
    from jsonschema import Draft202012Validator
    from evaluation.contract import check_contract
    from engine.quality import quality
    task = json.loads(task_path.read_text())
    original = copy.deepcopy(task)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    Draft202012Validator(schema).validate(task['source'])
    destination.mkdir(parents=True, exist_ok=True)
    runs, reference, issues = [], None, []
    for iteration in range(repetitions+1):
        before = time.perf_counter()
        output, diagnostics = resize_with_diagnostics(task['source'], task['target_canvas'])
        engine_seconds = time.perf_counter()-before
        before = time.perf_counter()
        warnings = render_design_to_png(output, Path('brand_kit/assets'), destination/'output.png')
        render_seconds = time.perf_counter()-before
        findings = check_contract(original['source'], original['target_canvas'], output, schema)
        if task != original:
            findings.append({'code': 'input_mutation'})
        if reference is not None and output != reference:
            findings.append({'code': 'nondeterministic_output'})
        reference = copy.deepcopy(output)
        issues.extend(findings)
        runs.append(dict(engine_seconds=engine_seconds, render_seconds=render_seconds,
                         engine_plus_render_seconds=engine_seconds+render_seconds,
                         candidate_count=diagnostics['candidate_count'], warnings=warnings))
    # Peak includes interpreter, renderer, schema validation and all repetitions.
    # Sample before cProfile to avoid attributing instrumentation to normal RSS.
    peak = peak_rss_bytes(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, platform.system())
    hotspots = []
    if repetitions:
        profiler = cProfile.Profile()
        profiler.runcall(resize_with_diagnostics, task['source'], task['target_canvas'])
        stats = pstats.Stats(profiler)
        for (filename, line, function), (primitive, calls, own, cumulative, _) in sorted(
                stats.stats.items(), key=lambda item: item[1][3], reverse=True)[:15]:
            hotspots.append(dict(file=filename, line=line, function=function, calls=calls,
                                 self_seconds=own, cumulative_seconds=cumulative))
    report = dict(import_seconds=import_seconds, first=runs[0], warm=runs[1:],
                  peak_worker_rss_bytes=peak, issues=issues, quality=quality(task['source'], reference),
                  hotspots=hotspots)
    (destination/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return int(bool(issues))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('artifacts/profile'))
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--repetitions', type=int, default=5)
    args = parser.parse_args()
    if args.repetitions < 0:
        parser.error('repetitions must be nonnegative')
    if args.worker:
        return worker(args.worker, args.output, args.repetitions)
    if args.repetitions < 5:
        parser.error('use at least five warm repetitions')
    args.output.mkdir(parents=True, exist_ok=True)
    cases = [(p.stem, json.loads(p.read_text())) for p in sorted(Path('input').glob('*.json'))]
    for count in [12, 48, 120]:
        for name, width, height in [('wide', 1200, 300), ('portrait', 360, 900)]:
            cases.append((f'scale-{count}-{name}', scaling_task(count, width, height)))
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
              for folder in ['engine', 'evaluation'] for p in sorted(Path(folder).glob('*.py'))}
    report = dict(revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  python=sys.version, platform=platform.platform(), machine=platform.machine(),
                  logical_cpu_count=os.cpu_count(),
                  packages={p: importlib.metadata.version(p) for p in ['Pillow', 'jsonschema', 'cr-renderer']},
                  renderer_origin=importlib.metadata.distribution('cr-renderer').read_text('direct_url.json'),
                  code_hashes=hashes,
                  protocol='Each case gets separate cold and warm workers. Cold wall includes process startup, imports, validation, first engine/render, and report I/O; OS filesystem caches are not cleared. Warm has one untimed warmup then measured repeats. RSS is whole-worker peak before profiling; not engine-only allocation. No container/network-isolation claim.',
                  cases=[])
    for name, task in cases:
        case_dir = args.output/name
        case_dir.mkdir(parents=True, exist_ok=True)
        task_path = case_dir/'task.json'
        task_path.write_text(json.dumps(task, indent=2)+'\n')
        entry = dict(case=name, element_count=len(task['source']['elements']), modes={})
        for mode, repetitions in [('cold', 0), ('warm', args.repetitions)]:
            destination = case_dir/mode
            before = time.perf_counter()
            try:
                completed = subprocess.run([sys.executable, '-m', 'evaluation.profile', '--worker', str(task_path),
                                            '--output', str(destination), '--repetitions', str(repetitions)],
                                           capture_output=True, text=True, timeout=120)
                exit_code, stderr = completed.returncode, completed.stderr
            except subprocess.TimeoutExpired:
                exit_code, stderr = 124, 'Worker exceeded the 120-second profiling limit.'
            elapsed = time.perf_counter()-before
            path = destination/'report.json'
            entry['modes'][mode] = dict(exit_code=exit_code, process_wall_seconds=elapsed,
                stderr=stderr, report=json.loads(path.read_text()) if exit_code != 124 and path.exists() else None)
        report['cases'].append(entry)
        print(name, [entry['modes'][m]['exit_code'] for m in ['cold', 'warm']], flush=True)
    report['code_unchanged'] = all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p,h in hashes.items())
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return int(not report['code_unchanged'] or any(m['exit_code'] for c in report['cases'] for m in c['modes'].values()))


if __name__ == '__main__':
    raise SystemExit(main())
