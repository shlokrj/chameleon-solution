"""Cheap candidate gates and explicit local quality proxies, not official scores."""
import math
from collections import Counter
from engine.layout import bounds
from engine.typography import text_extent

MUTABLE = {'x', 'y', 'width', 'height', 'font_size'}
READABLE_FONT_PX = 12.0  # local diagnostic threshold, not a contest requirement


def hard_issues(source, target, design):
    """Gate generated output from a schema-valid source without a dev dependency.

    Complete Draft 2020-12 validation stays in the independent evaluator.
    All unchanged source fields are preserved; changed fields are checked here.
    """
    issues = []
    if design.get('canvas') != target or set(design) != set(source):
        issues.append('canvas or top-level structure changed')
    elements = design.get('elements', [])
    if Counter(e.get('id') for e in elements) != Counter(e['id'] for e in source['elements']):
        return issues + ['element identity mismatch']
    if len({e.get('id') for e in elements}) != len(elements):
        return issues + ['duplicate element IDs']
    originals = {e['id']: e for e in source['elements']}
    for el in elements:
        old = originals[el['id']]
        if set(el) != set(old) or any(el[k] != v for k, v in old.items() if k not in MUTABLE):
            issues.append(f"{el['id']}: preserved fields changed")
        numeric = [el.get(k) for k in ('x', 'y', 'width', 'height')]
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in numeric):
            issues.append(f"{el['id']}: invalid geometry")
            continue
        if el['width'] < 0 or el['height'] < 0:
            issues.append(f"{el['id']}: negative size")
        if el['type'] == 'text' and (not isinstance(el.get('font_size'), (int, float)) or not math.isfinite(el['font_size']) or el['font_size'] < 1):
            issues.append(f"{el['id']}: invalid font size")
        a, b, c, d = bounds([el])
        if a < -1e-6 or b < -1e-6 or c > target['width']+1e-6 or d > target['height']+1e-6:
            issues.append(f"{el['id']}: off canvas")
        if old['type'] == 'image' and old.get('fit', 'contain') != 'cover' and old['width'] > 0 and old['height'] > 0:
            if el['width'] <= 0 or el['height'] <= 0 or not math.isclose(el['width']*old['height'], el['height']*old['width'], rel_tol=1e-6):
                issues.append(f"{el['id']}: image ratio changed")
    return issues


def overlap(a, b):
    ax, ay, ar, ab = bounds([a])
    bx, by, br, bb = bounds([b])
    area = max(0, min(ar, br)-max(ax, bx))*max(0, min(ab, bb)-max(ay, by))
    return area / max(1e-9, min((ar-ax)*(ab-ay), (br-bx)*(bb-by)))


def quality(source, design):
    old = {e['id']: e for e in source['elements']}
    text = [e for e in design['elements'] if e['type'] == 'text' and e['content']]
    area_scale = math.sqrt(design['canvas']['width']*design['canvas']['height'] /
                           (source['canvas']['width']*source['canvas']['height']))
    deficits, overflow, tiny = [], [], []
    for el in text:
        desired = max(READABLE_FONT_PX, old[el['id']]['font_size']*min(1, area_scale))
        deficits.append(max(0, 1-el['font_size']/desired)**2)
        w, h, lines = text_extent(el, el['font_size'], el['width'])
        if w > el['width']+1e-6 or h > el['height']+1e-6 or (el.get('max_lines') is not None and lines > el['max_lines']):
            overflow.append(el['id'])
        if el['font_size'] < READABLE_FONT_PX:
            tiny.append(el['id'])
    # Penalize reversal of source font hierarchy, not arbitrary aesthetic taste.
    inversion = sum(max(0, b['font_size']-a['font_size'])/max(1, a['font_size'])
                    for a in text for b in text
                    if old[a['id']]['font_size'] > old[b['id']]['font_size']*1.5)
    relevant = [e for e in design['elements'] if e['type'] == 'text' or
                (e['type'] == 'image' and e.get('fit', 'contain') != 'cover')]
    collisions = 0.0
    for i, a in enumerate(relevant):
        for b in relevant[i+1:]:
            if a.get('group_id') is not None and a.get('group_id') == b.get('group_id'):
                continue
            # Preserve already-intentional layering; score only increased overlap.
            collisions += max(0, overlap(a, b)-overlap(old[a['id']], old[b['id']])-0.01)
    deficit = sum(deficits)/max(1, len(deficits))
    return {'overflow_ids': overflow, 'small_text_ids': tiny,
            'minimum_font_size': min((e['font_size'] for e in text), default=None),
            'readability_deficit': deficit, 'hierarchy_inversion': inversion,
            'new_overlap': collisions, 'loss': deficit + 0.1*inversion + collisions}


def regression_reasons(source, baseline, candidate):
    """Protect main copy and imagery from being sacrificed to average scores."""
    base = {e['id']: e for e in baseline['elements']}
    reasons = []
    for el in candidate['elements']:
        previous = base[el['id']]
        if el['type'] == 'text':
            if el['font_size'] < previous['font_size']*0.95 - 1e-6:
                reasons.append(f"{el['id']}: type shrank over 5%")
        if el['type'] == 'image' and el.get('fit', 'contain') != 'cover':
            if min(el['width'], el['height']) < 0.8*min(previous['width'], previous['height'])-1e-6:
                reasons.append(f"{el['id']}: image short edge shrank over 20%")
    return reasons
