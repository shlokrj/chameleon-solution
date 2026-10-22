"""Bounded deterministic candidate selection; diagnostics stay out of output."""
import json
from copy import deepcopy
from engine.layout import build_layout, expand_images, refine_text
from engine.quality import hard_issues, quality, regression_reasons, overlap
from engine.typography import fit_text

MAX_CANDIDATES = 6


def resize_with_diagnostics(source, target_canvas, *, max_candidates=MAX_CANDIDATES):
    if not isinstance(max_candidates, int) or isinstance(max_candidates, bool) or not 1 <= max_candidates <= MAX_CANDIDATES:
        raise ValueError(f'max_candidates must be an integer from 1 to {MAX_CANDIDATES}')
    wide = target_canvas['width'] >= target_canvas['height']
    # (image share, group share, group side column); side columns suit banners.
    allocations = [(None, None, False, False), *[(image, group, True, side) for image, group, side in
        ([(0.18, 0.26, False), (0.15, 0.22, True), (0.25, 0.30, False), (0.20, 0.28, True), (0.32, 0.30, False)] if wide else
         [(0.25, 0.30, False), (0.36, 0.30, False), (0.25, 0.40, False), (0.45, 0.30, False), (0.36, 0.40, False)])]]
    # Side columns squeeze secondary groups on nearly square canvases.
    # Spend the same budget on deeper bottom zones for these shapes.
    if wide and target_canvas['width'] / target_canvas['height'] < 2:
        allocations[2] = (0.25, 0.40, True, False)
        allocations[4] = (0.25, 0.50, True, False)
    seen, records = set(), []
    baseline = best = None
    baseline_quality = None
    best_key = None
    selected = None
    best_image_zones = []
    best_text_refinements = []
    for index, (image, group, force, side) in enumerate(allocations[:max_candidates]):
        image_zones = []
        text_refinements = []
        design = build_layout(source, target_canvas, image_share=image, group_share=group, force_reflow=force,
                              text_grid=index == MAX_CANDIDATES-1, group_side=side, image_zones=image_zones, text_refinements=text_refinements)
        record = {'index': index, 'image_share': image, 'group_share': group, 'force_reflow': force,
                  'group_side': side, 'text_grid': index == MAX_CANDIDATES-1}
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
            best_image_zones = image_zones
            best_text_refinements = text_refinements
        # An already readable, collision-free baseline does not need extra work.
        if index == 0 and key == (0, 0):
            break
    if best is None:
        raise ValueError('No structurally valid layout candidate; refusing invalid output')
    # A post-selection pass cannot change the winning layout or shrink a
    # product through the candidate regression guard. Zones hold references
    # into the selected design only; no internal metadata enters the output.
    for zone in best_image_zones:
        expand_images(*zone)
    # Compare final quality only when a refinement actually changes text.
    # A floor may otherwise invert hierarchy relative to grouped labels.
    original_copy = [(unit[0], deepcopy(unit[0]))
                     for units, *_ in best_text_refinements for unit in units]
    refined_text = refine_text(best_text_refinements)
    if refined_text:
        originals = {el['id']: saved for el, saved in original_copy}
        before = dict(best, elements=[originals.get(el['id'], el) for el in best['elements']])
        old_metrics, new_metrics = quality(source, before), quality(source, best)
        if (new_metrics['loss'] > old_metrics['loss']+1e-9
                or new_metrics['hierarchy_inversion'] > old_metrics['hierarchy_inversion']+1e-9
                or len(new_metrics['overflow_ids']) > len(old_metrics['overflow_ids'])):
            for el, saved in original_copy:
                el.clear()
                el.update(saved)
            refined_text = []
    refined_group_text = refine_group_labels(source, best)
    return best, {'refined_group_text': refined_group_text, 'refined_text': refined_text, 'selected': selected, 'candidate_count': len(records), 'candidates': records}


def refine_group_labels(source, design):
    """Enlarge explicit group labels in their existing boxes, with rollback."""
    originals = {el['id']: el for el in source['elements']}
    saved, changed = {}, []
    labels = [el for el in design['elements']
              if el['type'] == 'text' and el.get('group_id') is not None and el['content']]
    for el in labels:
        # Overlapping text boxes may encode intentional layering; do not fill
        # that shared space with larger glyphs based on box fit alone.
        if any(other is not el and other['group_id'] == el['group_id']
               and overlap(el, other) > 1e-9 for other in labels):
            continue
        upper = min(12.0, originals[el['id']]['font_size'])
        if upper <= el['font_size']+1e-6:
            continue
        prior = deepcopy(el)
        fit_text(el, upper)
        if el['font_size'] <= prior['font_size']+1e-6:
            el.update(prior)
            continue
        saved[el['id']] = prior
        changed.append(el['id'])
    if not changed:
        return []
    before = dict(design, elements=[saved.get(el['id'], el) for el in design['elements']])
    old, new = quality(source, before), quality(source, design)
    if (new['loss'] > old['loss']+1e-9
            or new['hierarchy_inversion'] > old['hierarchy_inversion']+1e-9
            or len(new['overflow_ids']) > len(old['overflow_ids'])):
        for el in labels:
            if el['id'] in saved:
                el.update(saved[el['id']])
        return []
    return changed


def resize(source, target_canvas):
    return resize_with_diagnostics(source, target_canvas)[0]
