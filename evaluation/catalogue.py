"""Sweep supplied and development sources across common platform formats.

Writes per-case renders, one contact sheet per source, and a report with
contract issues and readability proxies. Pass --reference to print per-case
changes against an earlier report. Local proxies only, not official scores.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw
from engine.resize import resize_with_diagnostics
from engine.quality import quality
from evaluation.contract import check_contract
from evaluation.development import families
from renderer.converter.convert import render_design_to_png

# Representative real formats (RULES: targets come from a fixed catalogue).
FORMATS = {
    'ig-square': (1080, 1080), 'ig-portrait': (1080, 1350), 'story': (1080, 1920),
    'fb-link': (1200, 628), 'yt-thumb': (1280, 720), 'twitter-header': (1500, 500),
    'wide-banner': (1600, 400), 'leaderboard': (728, 90), 'med-rect': (300, 250),
    'skyscraper': (160, 600),
}


def sources():
    for path in sorted(Path('input').glob('*.json')):
        yield path.stem.replace('chameleon_sample_', ''), json.loads(path.read_text())['source']
    yield from families()


def contact_sheet(tiles, path, height=220):
    scaled = [(name, img.resize((max(1, round(img.width*height/img.height)), height))) for name, img in tiles]
    sheet = Image.new('RGB', (sum(i.width for _, i in scaled)+10*len(scaled), height+24), 'white')
    x = 0
    for name, img in scaled:
        sheet.paste(img, (x, 24))
        ImageDraw.Draw(sheet).text((x+2, 4), name, fill='black')
        x += img.width+10
    sheet.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('artifacts/catalogue'))
    parser.add_argument('--reference', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
    reference = {r['case']: r for r in json.loads(args.reference.read_text())} if args.reference else {}
    report, failed = [], False
    for name, source in sources():
        tiles = []
        render_design_to_png(source, Path('brand_kit/assets'), args.output/f'{name}-source.png')
        tiles.append(('source', Image.open(args.output/f'{name}-source.png')))
        for fmt, (w, h) in FORMATS.items():
            target = {'width': w, 'height': h}
            design, diagnostics = resize_with_diagnostics(source, target)
            issues = check_contract(source, target, design, schema)
            metrics = quality(source, design)
            fonts = sorted((e['font_size'] for e in design['elements'] if e['type'] == 'text' and e['content']), reverse=True)
            case = f'{name}@{fmt}'
            png = args.output/f'{name}-{fmt}.png'
            render_design_to_png(design, Path('brand_kit/assets'), png)
            tiles.append((fmt, Image.open(png)))
            row = {'case': case, 'issues': issues, 'selected': diagnostics['selected'],
                   'max_font': fonts[0] if fonts else None, 'min_font': fonts[-1] if fonts else None,
                   'overflow': metrics['overflow_ids'], 'loss': metrics['loss']}
            report.append(row)
            failed |= bool(issues)
            old = reference.get(case)
            delta = '' if not old else f"  (was max {old['max_font'] or 0:.1f} min {old['min_font'] or 0:.1f} loss {old['loss']:.3f})"
            print(f"{case:32} issues {len(issues)} max {row['max_font'] or 0:6.1f} min {row['min_font'] or 0:5.1f} "
                  f"loss {row['loss']:.3f} overflow {len(row['overflow'])}{delta}", flush=True)
        contact_sheet(tiles, args.output/f'{name}-sheet.png')
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
