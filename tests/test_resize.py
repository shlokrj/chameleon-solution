import copy
import json
from pathlib import Path
import unittest
from evaluation.contract import check_contract
from engine.resize import resize
from engine.typography import fit_text, text_extent

SCHEMA = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())


def text(eid='a', **overrides):
    return dict(id=eid, type='text', x=10, y=10, width=160, height=60,
                font_family='Solstice Sans', content='A real headline',
                font_size=24, color='white', **overrides)


def document(elements):
    return {'canvas': {'width': 200, 'height': 200}, 'elements': elements}


class ResizeTests(unittest.TestCase):
    def assert_contract(self, source, target):
        snapshot = copy.deepcopy(source)
        result = resize(source, target)
        self.assertEqual(source, snapshot)
        self.assertEqual(check_contract(source, target, result, SCHEMA), [])
        self.assertEqual(result, resize(source, target))
        return result

    def test_samples_and_alternate_targets(self):
        for path in sorted(Path('input').glob('*.json')):
            task = json.loads(path.read_text())
            for target in [task['target_canvas'], {'width': 360, 'height': 800}, {'width': 1200, 'height': 300}]:
                with self.subTest(path=path, target=target):
                    self.assert_contract(task['source'], target)

    def test_group_transform_preserves_containment(self):
        label = text(group_id='unit', z_index=2)
        label.update(x=30, y=35, width=140, height=30, font_size=18)
        shape = dict(id='box', type='shape', x=20, y=20, width=160, height=60,
                     shape_type='rectangle', fill_color='black', group_id='unit', z_index=1)
        for target in [{'width': 800, 'height': 160}, {'width': 100, 'height': 600}]:
            result = self.assert_contract(document([shape, label]), target)
            box, txt = result['elements']
            self.assertGreaterEqual(txt['x'], box['x'])
            self.assertGreaterEqual(txt['y'], box['y'])
            self.assertLessEqual(txt['x']+txt['width'], box['x']+box['width']+1e-8)
            self.assertLessEqual(txt['y']+txt['height'], box['y']+box['height']+1e-8)

    def test_renaming_and_distinct_z_order(self):
        els = [text('first', z_index=1), text('second', z_index=2)]
        els[1]['y'] = 100
        source = document(els)
        target = {'width': 900, 'height': 200}
        expected = resize(source, target)
        renamed = copy.deepcopy(source)
        for i, el in enumerate(renamed['elements']):
            el['id'] = f'opaque-{i}'
        renamed['elements'].reverse()
        actual = resize(renamed, target)
        by_z = {e['z_index']: e for e in actual['elements']}
        for el in expected['elements']:
            other = by_z[el['z_index']]
            self.assertEqual({k:v for k,v in el.items() if k != 'id'},
                             {k:v for k,v in other.items() if k != 'id'})

    def test_nested_input_not_aliased(self):
        source = document([text(style_runs=[{'start': 0, 'end': 4, 'font_weight': 'bold'}])])
        result = resize(source, source['canvas'])
        result['elements'][0]['style_runs'][0]['end'] = 0
        self.assertEqual(source['elements'][0]['style_runs'][0]['end'], 4)

    def test_rotation_and_zero_area(self):
        image = dict(id='image', type='image', x=-10, y=0, width=200,
                     height=80, rotation=45, asset_id='missing.png')
        line = dict(id='line', type='shape', x=40, y=50, width=0,
                    height=0, shape_type='line', fill_color='white')
        self.assert_contract(document([image, line]), {'width': 60, 'height': 250})

    def test_dense_tiny_canvas_stays_structurally_valid(self):
        # Readability is infeasible; gaps must not push elements off canvas.
        self.assert_contract(document([text(str(i), z_index=i) for i in range(30)]),
                             {'width': 30, 'height': 1})

    def test_unbreakable_word_and_style_fitting(self):
        el = text(style_runs=[{'start': 0, 'end': 10, 'font_weight': 'bold'}], letter_spacing=1)
        el.update(content='SUPERCALIFRAGILISTIC', width=180, height=40)
        fit_text(el, 36)
        width, height, lines = text_extent(el, el['font_size'], el['width'])
        self.assertLessEqual(width, el['width']+1e-5)
        self.assertLessEqual(height, el['height']+1e-5)
        self.assertEqual(lines, 1)

    def test_empty_text_and_explicit_newlines(self):
        el = text()
        el['content'] = ''
        self.assertEqual(text_extent(el, 12, 100), (0, 0, 0))
        el['content'] = 'one\ntwo'
        self.assertEqual(text_extent(el, 12, 100)[2], 2)


if __name__ == '__main__':
    unittest.main()
