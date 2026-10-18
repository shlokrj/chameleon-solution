import copy
import tempfile
from pathlib import Path
import unittest
from PIL import Image
from evaluation.delivery import validate_pair
from renderer.converter.convert import render_design_to_png


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.source = {'canvas': {'width': 100, 'height': 60}, 'elements': [
            {'id': 'panel', 'type': 'shape', 'shape_type': 'rectangle',
             'x': 10, 'y': 10, 'width': 80, 'height': 40, 'fill_color': 'rgba(0,0,0,1)'}]}
        self.task = {'source': self.source, 'target_canvas': self.source['canvas']}

    def test_real_pair_passes_and_placeholder_pixels_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            actual, expected = Path(tmp)/'actual.png', Path(tmp)/'expected.png'
            render_design_to_png(self.source, Path('brand_kit/assets'), actual)
            self.assertEqual(validate_pair(self.task, self.source, actual, expected)[0], [])
            Image.new('RGB', (100, 60), 'white').save(actual)
            self.assertEqual(validate_pair(self.task, self.source, actual, expected)[0][0]['code'], 'render')

    def test_invalid_json_is_rejected_before_rendering(self):
        broken = copy.deepcopy(self.source)
        broken['elements'].append(copy.deepcopy(broken['elements'][0]))
        issues, _ = validate_pair(self.task, broken, Path('absent.png'), Path('unused.png'))
        self.assertTrue(issues)

    def test_missing_png_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                validate_pair(self.task, self.source, Path(tmp)/'missing.png', Path(tmp)/'expected.png')
