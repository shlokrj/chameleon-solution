"""Deterministic retargeting with explicit groups and font-aware text fitting."""
from copy import deepcopy
from functools import lru_cache
import math
from pathlib import Path
from PIL import Image
from renderer.converter.assets import asset_path
from engine.typography import fit_text, text_extent
from engine.relationships import support_pairs

ASSETS_DIR = str(Path(__file__).resolve().parents[1] / 'brand_kit/assets')
# Smaller copy may keep this size while larger copy shrinks, but stays at most
# HIERARCHY_RATIO of the largest copy so the headline remains dominant.
# ponytail: one absolute floor; per-role floors if catalogue tuning shows a need.
MIN_READABLE_PX = 10.0
HIERARCHY_RATIO = 0.7
STYLE_LENGTHS = ('corner_radius', 'stroke_width')


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


@lru_cache(maxsize=64)
def ink(asset_id):
    """Asset pixel size and opaque-pixel bbox, or None (missing/unreadable)."""
    path = asset_path(ASSETS_DIR, asset_id)
    if path is None:
        return None
    try:
        with Image.open(path) as image:
            box = image.getchannel('A').getbbox() if 'A' in image.getbands() else None
            return image.size, box or (0, 0, *image.size)
    except OSError:
        return None


def visual_bounds(elements):
    """Like bounds(), but contain images count only their visible pixels.

    Logos and cut-out products carry wide transparent margins; packing and
    collision checks on the ink, not the box, use that space. The box itself
    still governs on-canvas checks (see keep_on_canvas).
    """
    boxes = []
    for el in elements:
        found = (ink(el.get('asset_id')) if el['type'] == 'image' and el.get('fit', 'contain') == 'contain'
                 and not el.get('rotation', 0) and el['width'] > 0 and el['height'] > 0 else None)
        if found is None:
            boxes.append(bounds([el]))
            continue
        (iw, ih), (l, t, r, b) = found
        scale = min(el['width']/iw, el['height']/ih)
        ox, oy = el['x']+(el['width']-iw*scale)/2, el['y']+(el['height']-ih*scale)/2
        boxes.append((ox+l*scale, oy+t*scale, ox+r*scale, oy+b*scale))
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def keep_on_canvas(units, width, height):
    """Shrink a packed zone about its visible center until its boxes fit.

    Scaling about the ink center keeps visible pixels inside their slot (a
    shift could push a logo's ink into the copy column); the zone transforms
    as one rigid unit so the packed arrangement survives.
    """
    elements = [el for unit in units for el in unit]
    if not elements:
        return
    def inside(box):
        return box[0] >= -1e-9 and box[1] >= -1e-9 and box[2] <= width+1e-9 and box[3] <= height+1e-9
    a, b, c, d = bounds(elements)
    if inside((a, b, c, d)):
        return
    va, vb, vc, vd = visual_bounds(elements)
    cx, cy = (va+vc)/2, (vb+vd)/2
    def scaled(s):  # box extent after scaling the zone by s about (cx, cy)
        return (cx+(a-cx)*s, cy+(b-cy)*s, cx+(c-cx)*s, cy+(d-cy)*s)
    low, high = 0.0, 1.0
    for _ in range(30):
        mid = (low+high)/2
        low, high = (mid, high) if inside(scaled(mid)) else (low, mid)
    left, top, right, bottom = scaled(low)
    place(elements, (left, top, right-left, bottom-top))


def expand_images(units, slot, canvas, gap):
    """Use spare image-zone space without shrinking or pushing neighbors.

    Only standalone, unrotated contain images qualify. Smaller visible images
    get first use of free space; each can grow at most 50%, shifting only as needed to stay in its
    existing free-space compartment.
    No semantic role or asset-name inference is needed.
    """
    x, y, w, h = slot
    cw, ch = canvas
    def area(unit):
        a, b, c, d = visual_bounds(unit)
        return (c-a)*(d-b)
    ordered = sorted(units, key=area)
    for unit in ordered:
        if len(unit) != 1:
            continue
        el = unit[0]
        if (el['type'] != 'image' or el.get('fit', 'contain') != 'contain'
                or el.get('rotation', 0) or el['width'] <= 0 or el['height'] <= 0):
            continue
        ink_box = visual_bounds(unit)
        others = [visual_bounds(other) for other in units if other is not unit]
        cx, cy = el['x']+el['width']/2, el['y']+el['height']/2
        offsets = (ink_box[0]-cx, ink_box[1]-cy, ink_box[2]-cx, ink_box[3]-cy)
        def placement(scale):
            l, t, r, b = (v*scale for v in offsets)
            hw, hh = el['width']*scale/2, el['height']*scale/2
            xmin, xmax = max(hw, x-l), min(cw-hw, x+w-r)
            ymin, ymax = max(hh, y-t), min(ch-hh, y+h-b)
            for other in others:
                # Retain an existing separating direction rather than jumping
                # over a neighbor to reach unrelated free space.
                if ink_box[2]+gap <= other[0]+1e-9:
                    xmax = min(xmax, other[0]-gap-r)
                elif ink_box[0]-gap >= other[2]-1e-9:
                    xmin = max(xmin, other[2]+gap-l)
                elif ink_box[3]+gap <= other[1]+1e-9:
                    ymax = min(ymax, other[1]-gap-b)
                elif ink_box[1]-gap >= other[3]-1e-9:
                    ymin = max(ymin, other[3]+gap-t)
                else:
                    return None
            if xmin > xmax or ymin > ymax:
                return None
            nx, ny = min(max(cx, xmin), xmax), min(max(cy, ymin), ymax)
            return nx-hw, ny-hh, 2*hw, 2*hh
        if placement(1) is None:
            continue
        low, high = 1.0, 1.5
        if placement(high) is not None:
            low = high
        else:
            for _ in range(20):
                mid = (low+high)/2
                low, high = (mid, high) if placement(mid) is not None else (low, mid)
        if low <= 1+1e-6:
            continue
        a, b, width, height = placement(low)
        el.update(x=a, y=b, width=width, height=height)


def box_overlap(a, b):
    return max(0, min(a[2], b[2])-max(a[0], b[0]))*max(0, min(a[3], b[3])-max(a[1], b[1]))


def new_collision(before, after):
    """True if any pair of units overlaps where the source pair did not."""
    old, new = [visual_bounds(u) for u in before], [visual_bounds(u) for u in after]
    return any(box_overlap(new[i], new[j]) > 1e-6 and box_overlap(old[i], old[j]) <= 1e-6
               for i in range(len(new)) for j in range(i+1, len(new)))


def place(unit, slot, measure=bounds):
    """Uniformly transform the whole unit so relationships/ratios survive.

    `measure` picks which extent is fitted into the slot (box or visible ink).
    """
    left, top, right, bottom = measure(unit)
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
        for key in STYLE_LENGTHS:  # a pill stays a pill at any size
            if key in el:
                el[key] *= scale
        if el['type'] == 'text':
            fit_text(el, el['font_size']*scale)


def flow(units, slot, gap, upper_scale):
    """Pack units into centered rows or columns at one shared scale.

    A shared scale keeps relative sizes (a large button stays larger than a
    small badge). Try both directions without rotating the units; retain
    rows on ties. This adds at most one bounded 24-step packing search.
    """
    if not units:
        return
    x, y, w, h = slot
    sizes = [(c-a, d-b) for a, b, c, d in map(visual_bounds, units)]
    def packing(transpose):
        # Evaluate both reading directions: narrow zones often fit larger
        # units in columns. Keep each unit rigid and preserve source order.
        dims = [(uh, uw) for uw, uh in sizes] if transpose else sizes
        major, minor = (h, w) if transpose else (w, h)
        def rows(scale):
            result, row, row_width = [], [], 0.0
            for i, (uw, _) in enumerate(dims):
                if row and row_width+gap+uw*scale > major:
                    result.append(row)
                    row, row_width = [], 0.0
                row_width += (gap if row else 0)+uw*scale
                row.append(i)
            return result+[row]
        def fits(scale):
            laid = rows(scale)
            heights = [max(dims[i][1] for i in row)*scale for row in laid]
            return (all(sum(dims[i][0] for i in row)*scale+gap*(len(row)-1) <= major+1e-9 for row in laid)
                    and sum(heights)+gap*(len(laid)-1) <= minor+1e-9)
        low, high = 0.0, upper_scale
        if fits(high):
            low = high
        else:
            for _ in range(24):
                mid = (low+high)/2
                low, high = (mid, high) if fits(mid) else (low, mid)
        laid = rows(low)
        heights = [max(dims[i][1] for i in row)*low for row in laid]
        top = max(0, minor-sum(heights)-gap*(len(laid)-1))/2
        slots = {}
        for row, row_height in zip(laid, heights):
            row_width = sum(dims[i][0] for i in row)*low+gap*(len(row)-1)
            left = max(0, major-row_width)/2
            for i in row:
                uw, uh = dims[i][0]*low, dims[i][1]*low
                cross = top+(row_height-uh)/2
                slots[i] = ((x+cross, y+left, uh, uw) if transpose
                            else (x+left, y+cross, uw, uh))
                left += uw+gap
            top += row_height+gap
        return low, slots
    scale, slots = packing(False)
    if len(units) > 1 and scale < upper_scale - 1e-6:
        column_scale, column_slots = packing(True)
        if column_scale > scale + 1e-6:
            slots = column_slots
    for i, unit in enumerate(units):
        place(unit, slots[i], visual_bounds)


def text_stack(units, slot, gap, upper_scale):
    if not units:
        return
    x, y, width, height = slot
    # These units are singleton text boxes. Preserve their relative type sizes.
    elements = [u[0] for u in units]
    gap = min(gap, height / max(1, 2*len(elements)))
    largest = max(el['font_size'] for el in elements)
    def sizes(scale):
        # Shrink proportionally, but let small copy hold a readable floor
        # below the (shrunk) largest copy: order and dominance are preserved.
        floor = min(MIN_READABLE_PX, largest*scale*HIERARCHY_RATIO)
        return [max(1, min(el['font_size']*upper_scale, max(el['font_size']*scale, floor))) for el in elements]
    def measurements(scale):
        measured = []
        for el, size in zip(elements, sizes(scale)):
            rotated = bool(el.get('rotation', 0))
            wrap_width = min(width, height) if rotated else width
            ew, eh, lines = text_extent(el, size, wrap_width)
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
    for el, size, (ew, eh, bw, bh, _, _) in zip(elements, sizes(low), extents):
        el.update(x=x+(width-ew)/2, y=y+offset+(bh-eh)*compression/2,
                  width=ew, height=eh*compression)
        fit_text(el, size)
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


def build_layout(source, target_canvas, *, image_share=None, group_share=None, force_reflow=False, text_grid=False, group_side=False, image_zones=None):
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
        # Preserve normalized centers and scale complete groups uniformly.
        # Prefer the geometric-mean scale so extra room is used instead of
        # left as empty bands; fall back if units would newly collide.
        originals = [deepcopy(unit) for unit in foreground]
        geometric = math.sqrt(sx*sy)
        for scale in (geometric, (geometric+min(sx, sy))/2, min(sx, sy)):
            for unit, original in zip(foreground, originals):
                for el, src in zip(unit, original):
                    el.update(deepcopy(src))
                a, b, c, d = bounds(unit)
                w, h = min(tw, (c-a)*scale), min(th, (d-b)*scale)
                x = max(0, min(tw-w, (a+c)/2*sx-w/2))
                y = max(0, min(th-h, (b+d)/2*sy-h/2))
                place(unit, (x, y, w, h))
            if not new_collision(originals, foreground):
                break
        return result
    foreground.sort(key=lambda u: (bounds(u)[1], bounds(u)[0], min(e.get('z_index', 0) for e in u)))
    # A missing asset renders as a placeholder box: keep it, but as a
    # secondary unit beside the buttons/badges rather than in the hero slot.
    missing = [u for u in foreground if len(u) == 1 and u[0]['type'] == 'image'
               and asset_path(ASSETS_DIR, u[0].get('asset_id')) is None]
    images = [u for u in foreground if all(e['type'] == 'image' for e in u) and u not in missing]
    text = [u for u in foreground if len(u) == 1 and u[0]['type'] == 'text']
    groups = [u for u in foreground if u not in images and u not in text]
    margin = min(tw, th)*0.04
    gap = min(tw, th)*0.025
    upper = max(sx, sy)
    x, y, w, h = margin, margin, tw-2*margin, th-2*margin
    if tw >= th:
        image_width = w*(0.25 if image_share is None else image_share) if images and (text or groups) else w if images else 0
        flow(images, (x, y, image_width, h), gap, upper)
        keep_on_canvas(images, tw, th)
        if image_zones is not None:
            image_zones.append((images, (x, y, image_width, h), (tw, th), gap))
        if image_width and (text or groups):
            x += image_width+gap
            w -= image_width+gap
        if group_side and groups and text:
            # Banner archetype: buttons/badges get a full-height right column.
            group_width = w*(0.22 if group_share is None else group_share)
            flow(groups, (x+w-group_width, y, group_width, h), gap, upper)
            keep_on_canvas(groups, tw, th)
            arrange_text(text, (x, y, w-group_width-gap, h), gap, upper, text_grid)
            return result
        group_height = h*(0.22 if group_share is None else group_share) if groups and text else h if groups else 0
        flow(groups, (x, y+h-group_height, w, group_height), gap, upper)
        keep_on_canvas(groups, tw, th)
        arrange_text(text, (x, y, w, max(0, h-group_height-(gap if groups else 0))), gap, upper, text_grid)
    else:
        image_height = h*(0.36 if image_share is None else image_share) if images and (text or groups) else h if images else 0
        flow(images, (x, y, w, image_height), gap, upper)
        keep_on_canvas(images, tw, th)
        if image_zones is not None:
            image_zones.append((images, (x, y, w, image_height), (tw, th), gap))
        if image_height and (text or groups):
            y += image_height+gap
            h -= image_height+gap
        group_height = h*(0.25 if group_share is None else group_share) if groups and text else h if groups else 0
        flow(groups, (x, y+h-group_height, w, group_height), gap, upper)
        keep_on_canvas(groups, tw, th)
        arrange_text(text, (x, y, w, max(0, h-group_height-(gap if groups else 0))), gap, upper, text_grid)
    return result
