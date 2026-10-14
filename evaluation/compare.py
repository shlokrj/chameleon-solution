"""Paired comparison against trusted local M1 source, including real renders."""
import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import statistics
import subprocess
import time
from pathlib import Path
from jsonschema import Draft202012Validator
from engine.resize import resize_with_diagnostics
from engine.quality import quality
from evaluation.contract import check_contract
from evaluation.development import tasks
from renderer.converter.convert import render_design_to_png


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', default='6d1dbe5')
    parser.add_argument('--output', type=Path, default=Path('artifacts/m2'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    # This loads trusted repository code, not fixture-supplied code. Require the
    # same typography implementation so the paired comparison is actually M1.
    typography = subprocess.check_output(['git', 'show', f'{args.baseline}:engine/typography.py'])
    if typography != Path('engine/typography.py').read_bytes():
        raise RuntimeError('Typography changed: use a fully isolated baseline checkout instead')
    old_path = args.output/'m1_resize.py'
    old_path.write_bytes(subprocess.check_output(['git', 'show', f'{args.baseline}:engine/resize.py']))
    spec = importlib.util.spec_from_file_location('m1_reference', old_path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    cases = list(tasks())
    for path in sorted(Path('input').glob('*.json')):
        task = json.loads(path.read_text())
        cases.append(dict(case=path.stem, family='supplied', source=task['source'], target_canvas=task['target_canvas']))
    report = {'baseline': args.baseline, 'candidate_parent': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'python': platform.python_version(), 'platform': platform.platform(),
              'code_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['engine', 'evaluation'] for p in sorted(Path(folder).glob('*.py'))},
              'cases': []}
    failed = False
    for task in cases:
        source, target = task['source'], task['target_canvas']
        Draft202012Validator(schema).validate(source)
        saved = copy.deepcopy(source)
        base = old.resize(source, target)
        candidate, diagnostics = resize_with_diagnostics(source, target)
        issues = check_contract(saved, target, candidate, schema)
        base_issues = check_contract(saved, target, base, schema)
        if source != saved:
            issues.append({'code': 'policy', 'detail': 'input mutated'})
        timing = {'baseline': [], 'candidate': []}
        for iteration in range(5):
            # Alternate execution order to reduce a simple order bias.
            names = ['baseline', 'candidate'] if iteration % 2 == 0 else ['candidate', 'baseline']
            for name in names:
                started = time.perf_counter()
                repeated = old.resize(source, target) if name == 'baseline' else resize_with_diagnostics(source, target)[0]
                timing[name].append(time.perf_counter()-started)
                if repeated != (base if name == 'baseline' else candidate) or source != saved:
                    issues.append({'code': 'policy', 'detail': f'{name} repetition differed or mutated input'})
        directory = args.output/task['case']
        directory.mkdir(exist_ok=True)
        (directory/'task.json').write_text(json.dumps(task, indent=2)+'\n')
        warnings = {}
        for name, design in [('source', source), ('baseline', base), ('candidate', candidate)]:
            (directory/f'{name}.json').write_text(json.dumps(design, indent=2)+'\n')
            warnings[name] = render_design_to_png(design, Path('brand_kit/assets'), directory/f'{name}.png')
        row = {'case': task['case'], 'family': task['family'], 'baseline_issues': base_issues, 'candidate_issues': issues,
               'baseline_quality': quality(source, base), 'candidate_quality': quality(source, candidate),
               'diagnostics': diagnostics, 'engine_seconds': timing, 'render_warnings': warnings}
        report['cases'].append(row)
        failed |= bool(issues)
        print(task['case'], 'selected', diagnostics['selected'], 'loss', round(row['baseline_quality']['loss'], 3), '->', round(row['candidate_quality']['loss'], 3), 'issues', len(issues), flush=True)
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
