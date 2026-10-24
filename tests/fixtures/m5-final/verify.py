import json, hashlib
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
from jsonschema import Draft202012Validator
from engine.resize import resize_with_diagnostics
from engine.quality import quality
from evaluation.contract import check_contract
from renderer.converter.convert import render_design_to_png
out=Path('artifacts/m5-final-judge'); schema=json.loads(Path('chameleon_design_schema_v0.9.json').read_text()); report=[]
for path in sorted(Path('tests/fixtures/m5-final').glob('*.json')):
 t=json.loads(path.read_text()); saved=deepcopy(t)
 errors=[e.message for e in Draft202012Validator(schema).iter_errors(t['source'])]
 assert not errors, errors
 a,d=resize_with_diagnostics(t['source'],t['target_canvas']); b,e=resize_with_diagnostics(t['source'],t['target_canvas'])
 with patch('engine.resize.refine_tail_text',return_value=[]): baseline,_=resize_with_diagnostics(t['source'],t['target_canvas'])
 for name,design in [('source',t['source']),('baseline',baseline),('output',a)]:
  render_design_to_png(design,Path('brand_kit/assets'),out/f'{path.stem}-{name}.png')
  (out/f'{path.stem}-{name}.json').write_text(json.dumps(design,indent=2)+'\n')
 r=dict(case=path.stem,source_errors=errors,contract_issues=check_contract(t['source'],t['target_canvas'],a,schema),input_unchanged=t==saved,exact_repeat=a==b and d==e,quality=quality(t['source'],a),baseline_quality=quality(t['source'],baseline),refined_tail_text=d['refined_tail_text'],fonts={x['id']:x['font_size'] for x in a['elements'] if x['type']=='text'})
 report.append(r)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
assert all(not r['source_errors'] and not r['contract_issues'] and r['input_unchanged'] and r['exact_repeat'] and not r['quality']['overflow_ids'] for r in report), 'Final M5 regression failed'
