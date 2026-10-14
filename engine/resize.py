"""Bounded deterministic candidate selection; diagnostics stay out of output."""
import json
from engine.layout import build_layout
from engine.quality import hard_issues, quality, regression_reasons

MAX_CANDIDATES = 6


def resize_with_diagnostics(source, target_canvas, *, max_candidates=MAX_CANDIDATES):
    if not isinstance(max_candidates, int) or isinstance(max_candidates, bool) or not 1 <= max_candidates <= MAX_CANDIDATES:
        raise ValueError(f'max_candidates must be an integer from 1 to {MAX_CANDIDATES}')
    wide = target_canvas['width'] >= target_canvas['height']
    allocations = [(None, None, False), *[(image, group, True) for image, group in
        ([(0.12, 0.26), (0.18, 0.26), (0.25, 0.30), (0.18, 0.36), (0.32, 0.30)] if wide else
         [(0.25, 0.30), (0.36, 0.30), (0.25, 0.40), (0.45, 0.30), (0.36, 0.40)])]]
    seen, records = set(), []
    baseline = best = None
    baseline_quality = None
    best_key = None
    selected = None
    for index, (image, group, force) in enumerate(allocations[:max_candidates]):
        design = build_layout(source, target_canvas, image_share=image, group_share=group, force_reflow=force)
        record = {'index': index, 'image_share': image, 'group_share': group, 'force_reflow': force}
        records.append(record)
        issues = hard_issues(source, target_canvas, design)
        if issues:
            record.update(status='invalid', issues=issues)
            continue
        fingerprint = json.dumps(design, sort_keys=True, allow_nan=False)
        if fingerprint in seen:
            record['status'] = 'duplicate'
            continue
        seen.add(fingerprint)
        metrics = quality(source, design)
        record['quality'] = metrics
        if index == 0:
            baseline = design
            baseline_quality = metrics
        reasons = regression_reasons(source, baseline, design) if baseline is not None else []
        if baseline_quality is not None and metrics['new_overlap'] > baseline_quality['new_overlap'] + 1e-6:
            reasons.append('increased unintended-overlap proxy')
        if reasons:
            record.update(status='regression', reasons=reasons)
            continue
        # Text fit is lexicographically prior to all aesthetic proxies.
        key = (len(metrics['overflow_ids']), metrics['loss'])
        record['status'] = 'eligible'
        if best_key is None or key < best_key:
            best, best_key, selected = design, key, index
        # An already readable, collision-free baseline does not need extra work.
        if index == 0 and key == (0, 0):
            break
    if best is None:
        raise ValueError('No structurally valid layout candidate; refusing invalid output')
    return best, {'selected': selected, 'candidate_count': len(records), 'candidates': records}


def resize(source, target_canvas):
    return resize_with_diagnostics(source, target_canvas)[0]
