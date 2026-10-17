import copy
import json
from pathlib import Path
import unittest
from engine.resize import resize
from engine.relationships import contains, support_pairs
from engine.quality import quality
from evaluation.contract import check_contract

SCHEMA = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())


def fixture(name):
    return json.loads((Path('tests/fixtures/m3')/(name+'.json')).read_text())


class RelationshipTests(unittest.TestCase):
    def test_challenger_contrast_panel_is_preserved(self):
        task = fixture('contrast-layer')
        output = resize(task['source'], task['target_canvas'])
        panel, text = output['elements']
        self.assertTrue(contains(panel, text))
        self.assertNotIn('group_id', panel)
        self.assertNotIn('group_id', text)
        self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])
        self.assertEqual(quality(task['source'], output)['support_violations'], [])

    def test_image_supported_label_stays_on_image(self):
        task = fixture('image-supported-label')
        output = resize(task['source'], task['target_canvas'])
        self.assertTrue(contains(*output['elements']))
        self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])
        self.assertEqual(output['elements'][0]['asset_id'], task['source']['elements'][0]['asset_id'])

    def test_contain_image_does_not_imply_solid_backing(self):
        task = fixture('image-supported-label')
        task['source']['elements'][0]['fit'] = 'contain'
        self.assertEqual(support_pairs(task['source']), [])

    def test_contrast_loss_is_not_scored_as_perfect(self):
        task = fixture('contrast-layer')
        broken = copy.deepcopy(task['source'])
        broken['elements'][1]['x'] = 0
        q = quality(task['source'], broken)
        self.assertEqual(q['support_violations'], ['copy'])
        self.assertGreater(q['loss'], 0)

    def test_line_keeps_its_nonzero_axis(self):
        task = fixture('zero-width-line')
        output = resize(task['source'], task['target_canvas'])
        self.assertEqual(output, task['source'])

    def test_rotated_relationship_and_multiple_labels(self):
        task = fixture('contrast-layer')
        panel, text = task['source']['elements']
        panel.update(rotation=10, width=460, height=180, x=70, y=155)
        text.update(rotation=10, width=160, height=40, x=180, y=220)
        second = copy.deepcopy(text)
        second.update(id='second', x=300, y=255, content='More')
        task['source']['elements'].append(second)
        self.assertEqual(len(support_pairs(task['source'])), 2)
        output = resize(task['source'], task['target_canvas'])
        self.assertTrue(all(contains(output['elements'][0], e) for e in output['elements'][1:]))

    def test_large_inset_backing_retains_complete_readable_text(self):
        for inset in [1, 20, 40]:
            task = fixture('large-inset-backing')
            panel = task['source']['elements'][0]
            panel.update(x=inset, y=inset, width=600-2*inset, height=600-2*inset)
            original = copy.deepcopy(task)
            output = resize(task['source'], task['target_canvas'])
            self.assertTrue(contains(*output['elements']))
            self.assertGreaterEqual(output['elements'][1]['font_size'], 12)
            self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])
            self.assertEqual(task, original)

    def test_nested_panel_chain_survives_reordered_input(self):
        task = fixture('nested-support-panels')
        expected = resize(task['source'], task['target_canvas'])
        task['source']['elements'].reverse()
        output = resize(task['source'], task['target_canvas'])
        by_id = {e['id']: e for e in output['elements']}
        self.assertTrue(contains(by_id['outer'], by_id['inner']))
        self.assertTrue(contains(by_id['inner'], by_id['label']))
        self.assertEqual({e['id']: e for e in expected['elements']}, by_id)
        self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])

    def test_shared_ancestors_and_multiple_labels_are_not_duplicated(self):
        task = fixture('nested-support-panels')
        label = copy.deepcopy(task['source']['elements'][-1])
        label.update(id='second', y=300, height=20, content='More', font_size=12)
        task['source']['elements'].append(label)
        pairs = support_pairs(task['source'])
        self.assertEqual(len(pairs), 3)
        self.assertEqual(len(set(pairs)), 3)
        output = resize(task['source'], task['target_canvas'])
        self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])
        self.assertTrue(all(contains(output['elements'][1], e) for e in output['elements'][2:]))

    def test_nested_panel_loss_is_reported(self):
        task = fixture('nested-support-panels')
        broken = copy.deepcopy(task['source'])
        broken['elements'][0]['y'] = 400
        self.assertIn('inner', quality(task['source'], broken)['support_violations'])

    def test_paint_order_prevents_false_backing_and_cycles(self):
        task = fixture('contrast-layer')
        task['source']['elements'][0]['z_index'] = 100
        self.assertEqual(support_pairs(task['source']), [])
        task = fixture('nested-support-panels')
        outer, inner, text = task['source']['elements']
        inner.update(x=outer['x'], y=outer['y'], width=outer['width'], height=outer['height'])
        for el in [outer, inner, text]:
            el['z_index'] = 0
        self.assertEqual(support_pairs(task['source']), [(1, 2), (0, 1)])

    def test_unrelated_nested_shapes_and_explicit_groups_are_not_merged(self):
        task = fixture('nested-support-panels')
        task['source']['elements'].pop()
        self.assertEqual(support_pairs(task['source']), [])
        task = fixture('nested-support-panels')
        task['source']['elements'][0]['group_id'] = 'explicit-outer'
        self.assertEqual(support_pairs(task['source']), [(1, 2)])

    def test_explicit_groups_and_backgrounds_not_inferred(self):
        task = fixture('contrast-layer')
        task['source']['elements'][1]['group_id'] = 'explicit'
        self.assertEqual(support_pairs(task['source']), [])
        task = fixture('contrast-layer')
        task['source']['elements'][0].update(x=0, y=0, width=600, height=600)
        self.assertEqual(support_pairs(task['source']), [])


if __name__ == '__main__':
    unittest.main()
