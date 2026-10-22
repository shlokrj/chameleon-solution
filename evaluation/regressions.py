"""Render saved adversarial tasks; distinguish contract failures from quality debt."""
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from engine.resize import resize_with_diagnostics
from evaluation.contract import check_contract
from renderer.converter.convert import render_design_to_png


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('artifacts/regressions'))
    parser.add_argument('--fixtures', type=Path, default=Path('tests/fixtures/m3'),
                        help='Directory of saved task JSON files (default: M3 cases)')
    args = parser.parse_args()
    if not args.fixtures.is_dir():
        parser.error(f'Fixture directory does not exist: {args.fixtures}')
    args.output.mkdir(parents=True, exist_ok=True)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    report = []
    for path in sorted(args.fixtures.glob('*.json')):
        task = json.loads(path.read_text())
        if 'source' not in task:  # manually constructed comparison witness
            continue
        Draft202012Validator(schema).validate(task['source'])
        output, diagnostics = resize_with_diagnostics(task['source'], task['target_canvas'])
        issues = check_contract(task['source'], task['target_canvas'], output, schema)
        for name, design in [('source', task['source']), ('output', output)]:
            render_design_to_png(design, Path('brand_kit/assets'), args.output/f'{path.stem}-{name}.png')
        (args.output/f'{path.stem}-output.json').write_text(json.dumps(output, indent=2)+'\n')
        report.append({'case': path.stem, 'contract_issues': issues, 'diagnostics': diagnostics})
    if not report:
        parser.error(f'No task fixtures found in {args.fixtures}')
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print([(r['case'], len(r['contract_issues'])) for r in report])
    return int(any(r['contract_issues'] for r in report))


if __name__ == '__main__':
    raise SystemExit(main())
