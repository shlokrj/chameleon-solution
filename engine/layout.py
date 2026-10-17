"""Deterministic retargeting with explicit groups and font-aware text fitting."""
from copy import deepcopy
import math
from engine.typography import fit_text, text_extent
from engine.relationships import support_pairs


def bounds(elements):
    """Include unrotated boxes and rotated extents under the strict contract."""
    boxes = []
    for el in elements:
        x, y, w, h = (el[k] for k in ('x', 'y', 'width', 'height'))
        angle = math.radians(el.get('rotation', 0))
        rw = abs(w * math.cos(angle)) + abs(h * math.sin(angle))
        rh = abs(w * math.sin(angle)) + abs(h * math.cos(angle))
        boxes.extend([(x, y, x+w, y+h), (x+(w-rw)/2, y+(h-rh)/2, x+(w+rw)/2, y+(h+rh)/2)])
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def place(unit, slot):
    """Uniformly transform the whole unit so relationships/ratios survive."""
    left, top, right, bottom = bounds(unit)
    x, y, w, h = slot
    ratios = [slot_size/source_size for slot_size, source_size in
              ((w, right-left), (h, bottom-top)) if source_size > 0]
    scale = min(ratios) if ratios else 1.0
    dx, dy = x+(w-(right-left)*scale)/2, y+(h-(bottom-top)*scale)/2
    for el in unit:
        el['x'] = dx + (el['x']-left)*scale
        el['y'] = dy + (el['y']-top)*scale
        el['width'] *= scale
        el['height'] *= scale
        if el['type'] == 'text':
            fit_text(el, el['font_size']*scale)


def stack(units, slot, gap, horizontal=False):
    if not units:
        return
    x, y, w, h = slot
    gap = min(gap, (w if horizontal else h) / max(1, 2*len(units)))
    sizes = []
    for unit in units:
        a, b, c, d = bounds(unit)
        sizes.append(max(1e-6, (c-a)/max(d-b, 1e-6) if horizontal else (d-b)/max(c-a, 1e-6)))
    available = max(0, (w if horizontal else h) - gap*(len(units)-1))
    offset = 0
    for unit, size in zip(units, sizes):
        extent = available*size/sum(sizes)
        place(unit, (x+offset, y, extent, h) if horizontal else (x, y+offset, w, extent))
        offset += extent+gap


def text_stack(units, slot, gap, upper_scale):
    if not units:
        return
    x, y, width, height = slot
    # These units are singleton text boxes. Preserve their relative type sizes.
    elements = [u[0] for u in units]
    gap = min(gap, height / max(1, 2*len(elements)))
    def measurements(scale):
        measured = []
        for el in elements:
            rotated = bool(el.get('rotation', 0))
            wrap_width = min(width, height) if rotated else width
            ew, eh, lines = text_extent(el, max(1, el['font_size']*scale), wrap_width)
            box_width = max(ew, 1e-6) if rotated else width
            angle = math.radians(el.get('rotation', 0))
            bw = max(box_width, abs(box_width*math.cos(angle))+abs(eh*math.sin(angle)))
            bh = max(eh, abs(box_width*math.sin(angle))+abs(eh*math.cos(angle)))
            measured.append((box_width, eh, bw, bh, lines, ew))
        return measured
    def fits(extents):
        return (sum(e[3] for e in extents)+gap*(len(elements)-1) <= height
                and all(e[2] <= width and e[5] <= e[0] and
                        (el.get('max_lines') is None or e[4] <= el['max_lines'])
                        for el, e in zip(elements, extents)))
    low, high = 0.0, upper_scale
    if fits(measurements(high)):
        low = high
    else:
        for _ in range(18):
            scale = (low+high)/2
            if fits(measurements(scale)):
                low = scale
            else:
                high = scale
    extents = measurements(low)
    total = sum(e[3] for e in extents)
    available = max(0, height-gap*(len(elements)-1))
    compression = min(1, available/max(total, 1e-9))
    offset = max(0, (available-total)/2)
    for el, (ew, eh, bw, bh, _, _) in zip(elements, extents):
        el.update(x=x+(width-ew)/2, y=y+offset+(bh-eh)*compression/2,
                  width=ew, height=eh*compression)
        fit_text(el, max(1, el['font_size']*low))
        if el.get('rotation', 0) and compression < 1:
            place([el], (x, y+offset, width, bh*compression))
        offset += bh*compression+gap


def source_grid(units):
    """Recognize complete aligned rows, without inferring columns from prose."""
    rows = []
    for unit in units:
        el = unit[0]
        if el.get('rotation', 0):
            return None
        if not rows or abs(el['y']-rows[-1][0][0]['y']) > max(1e-6, min(el['height'], rows[-1][0][0]['height'])*0.01):
            rows.append([])
        rows[-1].append(unit)
    if len(rows) < 2 or len(rows[0]) < 2:
        return None
    columns = len(rows[0])
    for row in rows:
        row.sort(key=lambda unit: unit[0]['x'])
    for row in rows:
        if len(row) != columns:
            return None
        for i, unit in enumerate(row):
            el = unit[0]
            if abs(el['x']-rows[0][i][0]['x']) > max(1e-6, min(el['width'], rows[0][i][0]['width'])*0.01):
                return None
            if i and row[i-1][0]['x']+row[i-1][0]['width'] > el['x']:
                return None
    if any(max(u[0]['y']+u[0]['height'] for u in row) > following[0][0]['y']
           for row, following in zip(rows, rows[1:])):
        return None
    return rows


def arrange_text(units, slot, gap, upper_scale, use_grid):
    rows = source_grid(units) if use_grid else None
    if rows is None:
        text_stack(units, slot, gap, upper_scale)
        return
    x, y, w, h = slot
    columns = len(rows[0])
    gap = min(gap, w/(2*columns), h/(2*len(rows)))
    cw, ch = (w-gap*(columns-1))/columns, (h-gap*(len(rows)-1))/len(rows)
    for r, row in enumerate(rows):
        for c, unit in enumerate(row):
            text_stack([unit], (x+c*(cw+gap), y+r*(ch+gap), cw, ch), 0, upper_scale)


def build_layout(source, target_canvas, *, image_share=None, group_share=None, force_reflow=False, text_grid=False):
    result = deepcopy(source)
    result['canvas'] = deepcopy(target_canvas)
    sw, sh = source['canvas']['width'], source['canvas']['height']
    tw, th = target_canvas['width'], target_canvas['height']
    sx, sy = tw/sw, th/sh
    elements = result['elements']
    grouped = {}
    for index, el in enumerate(elements):
        key = ('group', el['group_id']) if el.get('group_id') is not None else ('single', index)
        grouped.setdefault(key, []).append(el)
    # Merge connected backing chains without relying on element input order.
    owners = {index: ('single', index) for index, el in enumerate(elements)
              if el.get('group_id') is None}
    for panel_index, child_index in support_pairs(source):
        parent_key, child_key = owners[panel_index], owners[child_index]
        if parent_key == child_key:
            continue
        grouped[parent_key].extend(grouped.pop(child_key))
        for index, key in owners.items():
            if key == child_key:
                owners[index] = parent_key
    units = list(grouped.values())
    foreground, decorative = [], []
    min_foreground_z = min((e.get('z_index', 0) for e in elements if e['type'] == 'text'), default=0)
    for unit in units:
        el = unit[0]
        is_single = len(unit) == 1
        full_canvas = (el['x'] <= 0 and el['y'] <= 0 and el['x']+el['width'] >= sw and el['y']+el['height'] >= sh)
        if is_single and full_canvas and ((el['type'] == 'image' and el.get('fit') == 'cover') or el['type'] == 'shape') and not el.get('rotation', 0):
            el.update(x=0.0, y=0.0, width=float(tw), height=float(th))
        elif is_single and el['type'] == 'shape' and el.get('group_id') is None and el.get('z_index', 0) < min_foreground_z:
            decorative.append(unit)
        else:
            foreground.append(unit)
    # Map decorative layers without interpreting metadata/IDs as instructions.
    for unit in decorative:
        el = unit[0]
        w, h = el['width']*min(sx, sy), el['height']*min(sx, sy)
        place(unit, (max(0, min(tw-w, el['x']*sx)), max(0, min(th-h, el['y']*sy)), min(w, tw), min(h, th)))
    ratio_change = sx/sy
    if not force_reflow and 0.67 <= ratio_change <= 1.5:
        for unit in foreground:
            a, b, c, d = bounds(unit)
            # Preserve normalized centers, but scale complete groups uniformly.
            w, h = min(tw, (c-a)*min(sx, sy)), min(th, (d-b)*min(sx, sy))
            x = max(0, min(tw-w, (a+c)/2*sx-w/2))
            y = max(0, min(th-h, (b+d)/2*sy-h/2))
            place(unit, (x, y, w, h))
        return result
    foreground.sort(key=lambda u: (bounds(u)[1], bounds(u)[0], min(e.get('z_index', 0) for e in u)))
    images = [u for u in foreground if all(e['type'] == 'image' for e in u)]
    text = [u for u in foreground if len(u) == 1 and u[0]['type'] == 'text']
    groups = [u for u in foreground if u not in images and u not in text]
    margin = min(tw, th)*0.04
    gap = min(tw, th)*0.025
    x, y, w, h = margin, margin, tw-2*margin, th-2*margin
    if tw >= th:
        image_width = w*(0.25 if image_share is None else image_share) if images and (text or groups) else w if images else 0
        stack(images, (x, y, image_width, h), gap)
        if image_width and (text or groups):
            x += image_width+gap
            w -= image_width+gap
        group_height = h*(0.22 if group_share is None else group_share) if groups and text else h if groups else 0
        stack(groups, (x, y+h-group_height, w, group_height), gap, horizontal=True)
        arrange_text(text, (x, y, w, max(0, h-group_height-(gap if groups else 0))), gap, max(sx, sy), text_grid)
    else:
        image_height = h*(0.36 if image_share is None else image_share) if images and (text or groups) else h if images else 0
        stack(images, (x, y, w, image_height), gap, horizontal=True)
        if image_height and (text or groups):
            y += image_height+gap
            h -= image_height+gap
        group_height = h*(0.25 if group_share is None else group_share) if groups and text else h if groups else 0
        stack(groups, (x, y+h-group_height, w, group_height), gap)
        arrange_text(text, (x, y, w, max(0, h-group_height-(gap if groups else 0))), gap, max(sx, sy), text_grid)
    return result
