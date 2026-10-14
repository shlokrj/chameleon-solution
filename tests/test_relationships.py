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

    def test_explicit_groups_and_backgrounds_not_inferred(self):
        task = fixture('contrast-layer')
        task['source']['elements'][1]['group_id'] = 'explicit'
        self.assertEqual(support_pairs(task['source']), [])
        task = fixture('contrast-layer')
        task['source']['elements'][0].update(x=0, y=0, width=600, height=600)
        self.assertEqual(support_pairs(task['source']), [])


if __name__ == '__main__':
    unittest.main()
