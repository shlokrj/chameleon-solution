import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from engine.main import render_to_png


class EntrypointTests(unittest.TestCase):
    def test_missing_renderer_fails_without_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'output.png'
            with patch.dict('sys.modules', {'renderer.converter.convert': None}):
                with self.assertRaises(ImportError):
                    render_to_png({}, Path('brand_kit/assets'), output)
            self.assertFalse(output.exists())

    def test_renderer_failure_propagates(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'output.png'
            with patch('renderer.converter.convert.render_design_to_png', side_effect=ImportError('backend unavailable')):
                with self.assertRaisesRegex(ImportError, 'backend unavailable'):
                    render_to_png({}, Path('brand_kit/assets'), output)
            self.assertFalse(output.exists())
