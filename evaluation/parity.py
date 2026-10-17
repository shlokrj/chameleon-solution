"""Capture complete layouts and decoded real-render pixels for exact comparison."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image
from jsonschema import Draft202012Validator
from engine.resize import resize
from engine.quality import quality
from evaluation.contract import check_contract
from evaluation.development import tasks
from evaluation.profile import scaling_task
from renderer.converter.convert import render_design_to_png


def cases():
    for path in sorted(Path('input').glob('*.json')):
        yield path.stem, json.loads(path.read_text())
    for task in tasks():
        yield task['case'], task
    for path in sorted(Path('tests/fixtures/m3').glob('*.json')):
        task = json.loads(path.read_text())
        if 'source' in task:
            yield 'regression-'+path.stem, task
    for count in [12, 48, 120]:
        for name, width, height in [('wide', 1200, 300), ('portrait', 360, 900)]:
            yield f'scale-{count}-{name}', scaling_task(count, width, height)
    for i, fields in enumerate([
        {'font_weight': 'bold'}, {'font_style': 'italic'}, {'letter_spacing': 2},
        {'line_height': 1.6},
        {'style_runs': [{'start': 0, 'end': 6, 'font_weight': 'bold', 'font_style': 'italic'}]},
        {'style_runs': [{'start': 0, 'end': 2, 'font_weight': 'bold'}, {'start': 3, 'end': 6, 'font_style': 'italic'}]},
    ]):
        task = scaling_task(1, 600, 160)
        task['source']['elements'][0].update(content='A café', **fields)
        yield f'typography-{i}', task


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reference', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    records = {}
    for name, task in cases():
        Draft202012Validator(schema).validate(task['source'])
        original = copy.deepcopy(task)
        design = resize(task['source'], task['target_canvas'])
        issues = check_contract(original['source'], original['target_canvas'], design, schema)
        if task != original:
            issues.append({'code': 'input_mutation'})
        png = args.output/(name+'.png')
        warnings = render_design_to_png(design, Path('brand_kit/assets'), png)
        with Image.open(png) as image:
            pixels = image.convert('RGBA')
            digest = hashlib.sha256(str(pixels.size).encode()+pixels.tobytes()).hexdigest()
        records[name] = dict(task=original, design=design, pixel_sha256=digest, quality=quality(original['source'], design), issues=issues, warnings=warnings)
    differences = []
    if args.reference:
        prior = json.loads(args.reference.read_text())['cases']
        for name in sorted(set(prior) | set(records)):
            if name not in prior or name not in records:
                differences.append({'case': name, 'field': 'case_missing'})
                continue
            for field in ['task', 'design', 'pixel_sha256', 'quality']:
                if prior[name].get(field) != records[name][field]:
                    differences.append({'case': name, 'field': field})
    report = dict(cases=records, differences=differences,
                  engine_hashes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('engine').glob('*.py'))})
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(case_count=len(records), differences=differences,
                          issue_count=sum(len(c['issues']) for c in records.values()))))
    return int(bool(differences) or any(c['issues'] for c in records.values()))


if __name__ == '__main__':
    raise SystemExit(main())
