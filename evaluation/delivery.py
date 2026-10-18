"""Independently validate entrypoint JSON/PNG pairs; no renderer fallback allowed."""
import argparse
import json
from pathlib import Path
import tempfile
from PIL import Image
from jsonschema import Draft202012Validator
from evaluation.contract import check_contract
from renderer.converter.convert import render_design_to_png


def validate_pair(task, design, png, expected):
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    Draft202012Validator(schema).validate(task['source'])
    issues = check_contract(task['source'], task['target_canvas'], design, schema)
    if issues:
        return issues, []
    warnings = render_design_to_png(design, Path('brand_kit/assets'), expected)
    with Image.open(png) as actual, Image.open(expected) as rendered:
        if actual.format != 'PNG' or actual.size != rendered.size or actual.convert('RGBA').tobytes() != rendered.convert('RGBA').tobytes():
            issues.append({'code': 'render', 'detail': 'PNG does not match direct rendering of output JSON'})
    return issues, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('input'))
    parser.add_argument('--output', type=Path, default=Path('output'))
    parser.add_argument('--report', type=Path, default=Path('artifacts/delivery/report.json'))
    args = parser.parse_args()
    report = {'cases': [], 'issues': []}
    tasks = sorted(args.input.glob('*.json'))
    if not tasks:
        report['issues'].append('No input tasks found')
    with tempfile.TemporaryDirectory() as tmp:
        for path in tasks:
            entry = {'case': path.stem, 'issues': []}
            try:
                task = json.loads(path.read_text())
                design = json.loads((args.output/(path.stem+'_output.json')).read_text())
                entry['issues'], entry['warnings'] = validate_pair(task, design, args.output/(path.stem+'_output.png'), Path(tmp)/'expected.png')
            except Exception as error:
                entry['issues'].append({'code': 'exception', 'detail': f'{type(error).__name__}: {error}'})
            report['cases'].append(entry)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return int(bool(report['issues']) or any(c['issues'] for c in report['cases']))


if __name__ == '__main__':
    raise SystemExit(main())
