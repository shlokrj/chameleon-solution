"""Compare fixed-budget allocation replacements without changing production."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

from engine.layout import build_layout
from engine.resize import resize_with_diagnostics
from engine.quality import quality, regression_reasons
from evaluation.catalogue import sources, FORMATS
from evaluation.contract import check_contract


def replacement(source, target, slot):
    index = -1
    def build(*args, **kwargs):
        nonlocal index
        index += 1
        if index == slot:
            kwargs.update(image_share=0.15, group_share=0.35,
                          group_side=target['width'] >= target['height'],
                          force_reflow=True)
        return build_layout(*args, **kwargs)
    with patch('engine.resize.build_layout', side_effect=build):
        return resize_with_diagnostics(source, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    targets = dict(FORMATS)
    targets.update({f'boundary-{w}x{h}': (w, h) for w, h in
                    [(299,300),(300,300),(301,300),(599,300),(600,300),(601,300),(161,600)]})
    rows = []
    for name, source in sources():
        original = deepcopy(source)
        for fmt, (w,h) in targets.items():
            target = dict(width=w,height=h)
            baseline, _ = resize_with_diagnostics(source,target)
            old = quality(source,baseline)
            for slot in range(1,6):
                candidate, diagnostics = replacement(source,target,slot)
                new = quality(source,candidate)
                assert candidate == replacement(source,target,slot)[0]
                assert source == original
                rows.append(dict(case=name+'@'+fmt, slot=slot,
                    changed=candidate != baseline, before=old, after=new,
                    issues=check_contract(source,target,candidate,schema),
                    regressions=regression_reasons(source,baseline,candidate),
                    candidate_count=diagnostics['candidate_count']))
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'report.json').write_text(json.dumps(rows,indent=2)+'\n')
    summary = []
    for slot in range(1,6):
        cases=[r for r in rows if r['slot']==slot]
        summary.append(dict(slot=slot,cases=len(cases),changed=sum(r['changed'] for r in cases),
            improved=sum(r['after']['loss'] < r['before']['loss']-1e-9 for r in cases),
            worse=sum(r['after']['loss'] > r['before']['loss']+1e-9 for r in cases),
            regressions=sum(bool(r['regressions']) for r in cases),
            contract_failures=sum(bool(r['issues']) for r in cases)))
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
