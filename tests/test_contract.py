import copy
import json
import unittest
from pathlib import Path
from evaluation.contract import check_contract

SCHEMA = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.source = {'canvas': {'width': 100, 'height': 100}, 'elements': [
            {'id': 'a', 'type': 'image', 'x': 0, 'y': 0, 'width': 40,
             'height': 20, 'asset_id': 'original.png'}]}

    def codes(self, out):
        return {i['code'] for i in check_contract(self.source, self.source['canvas'], out, SCHEMA)}

    def test_identity(self):
        self.assertEqual(self.codes(copy.deepcopy(self.source)), set())

    def test_duplicate_ids(self):
        out = copy.deepcopy(self.source)
        out['elements'].append(copy.deepcopy(out['elements'][0]))
        self.assertIn('C1', self.codes(out))

    def test_nonfinite(self):
        out = copy.deepcopy(self.source)
        out['elements'][0]['x'] = float('nan')
        self.assertIn('C2', self.codes(out))

    def test_rotated_overflow(self):
        out = copy.deepcopy(self.source)
        out['elements'][0]['rotation'] = 45
        self.assertIn('C3', self.codes(out))

    def test_distortion_and_asset_replacement(self):
        out = copy.deepcopy(self.source)
        out['elements'][0].update(width=50, asset_id='replacement.png')
        self.assertTrue({'C5', 'C6'} <= self.codes(out))

    def test_existing_cover_exception(self):
        self.source['elements'][0]['fit'] = 'cover'
        out = copy.deepcopy(self.source)
        out['elements'][0]['width'] = 50
        self.assertNotIn('C6', self.codes(out))

    def test_schema_and_target(self):
        out = copy.deepcopy(self.source)
        out['canvas']['width'] = 90
        self.assertIn('C2', self.codes(out))
        del out['elements'][0]['asset_id']
        self.assertIn('C2', self.codes(out))

    def test_content_and_nested_styles(self):
        self.source['elements'] = [{'id': 'text', 'type': 'text', 'x': 0, 'y': 0,
            'width': 100, 'height': 50, 'content': 'hello', 'font_family': 'brand',
            'font_size': 12, 'color': 'black', 'style_runs': [{'start': 0, 'end': 2}]}]
        out = copy.deepcopy(self.source)
        out['elements'][0]['content'] = 'changed'
        out['elements'][0]['style_runs'][0]['end'] = 3
        self.assertTrue({'C4', 'policy'} <= self.codes(out))


if __name__ == '__main__':
    unittest.main()
