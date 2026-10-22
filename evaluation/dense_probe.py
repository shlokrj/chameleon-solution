"""Bounded offline allocation study; never used by the runtime engine."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from engine.layout import build_layout, expand_images, refine_text
from engine.quality import quality, regression_reasons
from engine.resize import resize, refine_group_labels
from evaluation.contract import check_contract
from renderer.converter.convert import render_design_to_png


def probe(source, target, schema):
    Draft202012Validator(schema).validate(source)
    baseline = resize(source, target)
    best_allocation = None
    original = deepcopy(source)
    rows, best = [], baseline
    base_quality = quality(source, baseline)
    best_key = (len(base_quality['overflow_ids']), base_quality['loss'])
    # 50 fixed alternatives; deliberately much wider than the runtime budget.
    for image in (0.15, 0.25, 0.35, 0.45, 0.55):
        for group in (0.20, 0.35, 0.50, 0.65, 0.80):
            for side in (False, True):
                if side and target['width'] < target['height']:
                    continue
                zones, refinements = [], []
                candidate = build_layout(source, target, image_share=image,
                    group_share=group, force_reflow=True, group_side=side,
                    image_zones=zones, text_refinements=refinements)
                for zone in zones:
                    expand_images(*zone)
                before = deepcopy(candidate)
                refine_text(refinements)
                old, new = quality(source, before), quality(source, candidate)
                if (new['loss'] > old['loss']+1e-9 or
                    new['hierarchy_inversion'] > old['hierarchy_inversion']+1e-9 or
                    len(new['overflow_ids']) > len(old['overflow_ids'])):
                    candidate = before
                refine_group_labels(source, candidate)
                metrics = quality(source, candidate)
                issues = check_contract(source, target, candidate, schema)
                reasons = regression_reasons(source, baseline, candidate)
                if metrics['new_overlap'] > base_quality['new_overlap']+1e-6:
                    reasons.append('increased unintended overlap')
                key = (len(metrics['overflow_ids']), metrics['loss'])
                accepted = not issues and not reasons and key < best_key
                if accepted:
                    best, best_key = candidate, key
                    best_allocation = {"image_share": image, "group_share": group, "group_side": side}
                rows.append({'image_share': image, 'group_share': group,
                             'group_side': side, 'quality': metrics,
                             'issues': issues, 'regression_reasons': reasons})
    assert source == original, 'probe mutated source'
    return baseline, best, {'baseline': base_quality, 'best': quality(source, best),
                            'best_allocation': best_allocation,
                            'candidates': rows, 'input_unchanged': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    task = json.loads(args.task.read_text())
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    baseline, best, report = probe(task['source'], task['target_canvas'], schema)
    for name, design in [('source', task['source']), ('baseline', baseline), ('best', best)]:
        (args.output/f'{name}.json').write_text(json.dumps(design, indent=2)+'\n')
        render_design_to_png(design, Path('brand_kit/assets'), args.output/f'{name}.png')
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'baseline': report['baseline'], 'best': report['best']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
