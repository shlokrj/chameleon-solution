"""Run unchanged samples through the engine and direct renderer.

Run from repository root: python -m evaluation.baseline
Artifacts are local/ignored; JSON report records validation failures honestly.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
from pathlib import Path
from jsonschema import Draft202012Validator
from evaluation.contract import check_contract


def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path('brand_kit').rglob('*')) if p.is_file()}


def main():
    start = time.perf_counter()
    # Direct import: failure must never silently produce a placeholder preview.
    from renderer.converter.convert import render_design_to_png
    import_seconds = time.perf_counter() - start
    from engine.resize import resize
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('artifacts/baseline'))
    destination = parser.parse_args().output
    destination.mkdir(parents=True, exist_ok=True)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    before = hashes()
    report = {'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'python': platform.python_version(), 'platform': platform.platform(),
              'renderer_import_seconds': import_seconds,
              'packages': {p: importlib.metadata.version(p) for p in ['Pillow', 'jsonschema', 'cr-renderer']},
              'renderer_origin': importlib.metadata.distribution('cr-renderer').read_text('direct_url.json'),
              'code_hashes': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                              for folder in ['engine', 'evaluation'] for p in sorted(Path(folder).glob('*.py'))},
              'cases': []}
    for path in sorted(Path('input').glob('*.json')):
        task = json.loads(path.read_text())
        Draft202012Validator(schema).validate(task['source'])
        untouched = copy.deepcopy(task)
        t0 = time.perf_counter()
        output = resize(task['source'], task['target_canvas'])
        engine_seconds = time.perf_counter() - t0
        output_path = destination / f'{path.stem}_output.json'
        output_path.write_text(json.dumps(output, indent=2, allow_nan=False) + '\n')
        warnings = render_design_to_png(output, Path('brand_kit/assets'), destination / f'{path.stem}_output.png')
        pipeline_seconds = time.perf_counter() - t0
        render_design_to_png(task['source'], Path('brand_kit/assets'), destination / f'{path.stem}_source.png')
        issues = check_contract(untouched['source'], untouched['target_canvas'], output, schema)
        if task != untouched:
            issues.append({'code': 'policy', 'detail': 'input mutated'})
        warm_engine, warm_pipeline = [], []
        for _ in range(5):
            trial = copy.deepcopy(untouched)
            began = time.perf_counter()
            repeated = resize(trial['source'], trial['target_canvas'])
            warm_engine.append(time.perf_counter() - began)
            render_design_to_png(repeated, Path('brand_kit/assets'), destination / f'{path.stem}_repeat.png')
            warm_pipeline.append(time.perf_counter() - began)
            if repeated != output or trial != untouched:
                issues.append({'code': 'policy', 'detail': 'repeat differed or mutated input'})
        from engine.typography import text_extent
        text_diagnostics = []
        for el in output['elements']:
            if el['type'] != 'text':
                continue
            measured_width, measured_height, lines = text_extent(el, el['font_size'], el['width'])
            text_diagnostics.append({'id': el['id'], 'font_size': el['font_size'],
                'measured_width': measured_width, 'measured_height': measured_height,
                'box_width': el['width'], 'box_height': el['height'], 'lines': lines,
                'estimated_overflow': measured_width > el['width']+1e-6 or measured_height > el['height']+1e-6})
        report['cases'].append({'text_diagnostics': text_diagnostics, 'warm_engine_seconds': warm_engine, 'warm_pipeline_seconds': warm_pipeline, 'case': path.stem, 'engine_seconds': engine_seconds,
                                'pipeline_seconds': pipeline_seconds, 'warnings': warnings, 'issues': issues})
    report['brand_files_unchanged'] = before == hashes()
    report['brand_hashes'] = before
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'brand_hashes'}, indent=2))
    return 1 if any(c['issues'] for c in report['cases']) or not report['brand_files_unchanged'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
