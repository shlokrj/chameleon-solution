import json
from pathlib import Path
import unittest
from engine.layout import bounds, build_layout, flow, keep_on_canvas, place, text_stack, visual_bounds
from engine.resize import resize


def pill(gid, x, y, width, height, label):
    return [dict(id=gid+'-bg', type='shape', x=x, y=y, width=width, height=height, z_index=1,
                 shape_type='rectangle', fill_color='rgba(232,106,58,1)', corner_radius=height/2, group_id=gid),
            dict(id=gid+'-label', type='text', x=x, y=y+height/4, width=width, height=height/2, z_index=2,
                 content=label, font_family='Solstice Sans', font_size=height/3, color='white',
                 text_align='center', group_id=gid)]


class CompositionTests(unittest.TestCase):
    def test_flow_keeps_relative_sizes(self):
        # A large button must stay larger than a small badge after packing.
        badge, button = pill('badge', 0, 0, 200, 40, 'NEW'), pill('cta', 0, 100, 400, 90, 'Shop now')
        flow([badge, button], (0, 0, 300, 60), 4, 10)
        self.assertGreater(button[0]['height'], badge[0]['height'])
        self.assertAlmostEqual(button[0]['height']/badge[0]['height'], 90/40, places=6)

    def test_flow_uses_columns_when_rows_would_shrink_units(self):
        # A feasible column layout fits at full scale, whereas greedy rows
        # require 85px of height in this 80px slot.
        units = [[dict(id=str(i), type='shape', shape_type='rectangle',
                       x=0, y=0, width=w, height=h)]
                 for i, (w, h) in enumerate([(100, 20), (20, 40), (20, 40)])]
        flow(units, (10, 15, 140, 80), 5, 1)
        self.assertAlmostEqual(units[0][0]['width'], 100)
        boxes = [bounds(unit) for unit in units]
        for a, b, c, d in boxes:
            self.assertGreaterEqual(a, 10)
            self.assertGreaterEqual(b, 15)
            self.assertLessEqual(c, 150)
            self.assertLessEqual(d, 95)
        for i, a in enumerate(boxes):
            for b in boxes[i+1:]:
                self.assertTrue(a[2] <= b[0] or b[2] <= a[0]
                                or a[3] <= b[1] or b[3] <= a[1])

    def test_place_scales_corner_radius(self):
        unit = pill('cta', 0, 0, 400, 90, 'Shop now')
        place(unit, (0, 0, 800, 180))
        self.assertAlmostEqual(unit[0]['corner_radius'], unit[0]['height']/2)

    def test_type_floor_preserves_order_and_dominance(self):
        head = dict(id='h', type='text', x=0, y=0, width=900, height=100, content='A long headline ' * 6,
                    font_family='Solstice Serif', font_size=40, color='white')
        legal = dict(id='l', type='text', x=0, y=100, width=900, height=30, content='Fine print ' * 8,
                     font_family='Solstice Sans', font_size=12, color='white')
        text_stack([[head], [legal]], (0, 0, 500, 70), 2, 1.0)
        self.assertGreater(head['font_size'], legal['font_size'])
        self.assertGreaterEqual(legal['font_size'], min(10.0, head['font_size']*0.7)-1e-6)
        self.assertGreater(legal['font_size'], 12*head['font_size']/40)  # better than proportional

    def test_missing_asset_leaves_hero_slot(self):
        task = json.loads(Path('input/chameleon_sample_level3_advanced.json').read_text())
        out = {e['id']: e for e in resize(task['source'], {'width': 1200, 'height': 628})['elements']}
        # The real product stays the larger image; the placeholder is secondary.
        self.assertGreater(out['product']['width']*out['product']['height'],
                           2*out['holiday_watermark']['width']*out['holiday_watermark']['height'])

    def test_near_ratio_uses_extra_room_without_new_collisions(self):
        task = json.loads(Path('input/chameleon_sample_level1_warmup.json').read_text())
        out = {e['id']: e for e in build_layout(task['source'], {'width': 1080, 'height': 1350})['elements']}
        self.assertGreater(out['headline']['font_size'], 60)

    def test_ink_packing_keeps_boxes_on_canvas_and_ink_in_slot(self):
        logo = dict(id='logo', type='image', x=0, y=0, width=320, height=100, asset_id='solstice_logo_lockup.png', fit='contain')
        a, _, c, _ = visual_bounds([logo])
        self.assertLess(c-a, 0.6*logo['width'])  # transparent margins excluded
        slot = (10, 10, 200, 60)
        flow([[logo]], slot, 0, 10)
        keep_on_canvas([[logo]], 220, 80)
        a, b, c, d = bounds([logo])
        self.assertTrue(a >= -1e-9 and b >= -1e-9 and c <= 220+1e-9 and d <= 80+1e-9)
        va, vb, vc, vd = visual_bounds([logo])
        self.assertTrue(va >= 10-1e-6 and vc <= 210+1e-6 and vb >= 10-1e-6 and vd <= 70+1e-6)


if __name__ == '__main__':
    unittest.main()
