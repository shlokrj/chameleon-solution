"""Conservative geometric text/backing-panel relationships, without new labels."""
import math
from renderer.converter.colorutil import parse_rgba


def contains(panel, element, tolerance=1e-6):
    """Check all text-box corners in the rectangle's local coordinates."""
    angle = math.radians(element.get('rotation', 0))
    panel_angle = math.radians(panel.get('rotation', 0))
    cx, cy = element['x']+element['width']/2, element['y']+element['height']/2
    px, py = panel['x']+panel['width']/2, panel['y']+panel['height']/2
    for dx in (-element['width']/2, element['width']/2):
        for dy in (-element['height']/2, element['height']/2):
            x = cx + dx*math.cos(angle)-dy*math.sin(angle)-px
            y = cy + dx*math.sin(angle)+dy*math.cos(angle)-py
            local_x = x*math.cos(panel_angle)+y*math.sin(panel_angle)
            local_y = -x*math.sin(panel_angle)+y*math.cos(panel_angle)
            if abs(local_x) > panel['width']/2+tolerance or abs(local_y) > panel['height']/2+tolerance:
                return False
    return True


def support_pairs(source):
    """Return parent/child indices for text and its enclosing backing ancestry.

    Existing explicit groups take precedence. For nested panels, the frontmost
    containing panel wins, using the renderer's stable z/index paint ordering.
    Images qualify only with cover/fill: contain can leave transparent margins.
    This does not establish pixel contrast or infer arbitrary translucent layering.
    """
    elements = source['elements']
    width, height = source['canvas']['width'], source['canvas']['height']
    def background(el):
        return (not el.get('rotation', 0) and el['x'] <= 0 and el['y'] <= 0
                and el['x']+el['width'] >= width and el['y']+el['height'] >= height)
    panels = [(i, el) for i, el in enumerate(elements)
              if ((el['type'] == 'shape' and el.get('shape_type') == 'rectangle')
                  or (el['type'] == 'image' and el.get('fit') in {'cover', 'fill'}))
              and el.get('group_id') is None
              and el['width'] > 0 and el['height'] > 0 and not background(el)
              and el.get('opacity', 1)*(parse_rgba(el.get('fill_color'))[3] if el['type'] == 'shape' else 1) >= 0.5]
    # Stable paint order makes ancestry acyclic, even for coincident panels.
    # Only walk ancestors of supported text: unrelated shapes stay independent.
    parents = {}
    def parent(index, child):
        if index not in parents:
            candidates = [(i, panel) for i, panel in panels
                          if (panel.get('z_index', 0), i) < (child.get('z_index', 0), index)
                          and contains(panel, child)]
            parents[index] = (max(candidates, key=lambda pair: (pair[1].get('z_index', 0), pair[0]))[0]
                              if candidates else None)
        return parents[index]
    pairs, seen = [], set()
    for index, text in enumerate(elements):
        if text['type'] != 'text' or text.get('group_id') is not None:
            continue
        while True:
            panel_index = parent(index, elements[index])
            if panel_index is None or (panel_index, index) in seen:
                break
            seen.add((panel_index, index))
            pairs.append((panel_index, index))
            index = panel_index
    return pairs
