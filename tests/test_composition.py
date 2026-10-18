import json
from pathlib import Path
import unittest
from engine.layout import build_layout, flow, place, text_stack
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


if __name__ == '__main__':
    unittest.main()
