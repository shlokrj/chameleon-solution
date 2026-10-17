"""Validate profiling units and the schema of generated scaling tasks."""
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
from evaluation.profile import peak_rss_bytes, scaling_task
from evaluation.contract import check_contract


class ProfileTests(unittest.TestCase):
    def test_platform_rss_units(self):
        self.assertEqual(peak_rss_bytes(2048, 'Darwin'), 2048)
        self.assertEqual(peak_rss_bytes(2048, 'Linux'), 2097152)
        self.assertIsNone(peak_rss_bytes(2048, 'Unknown'))

    def test_scaling_sources_are_valid_and_in_bounds(self):
        schema = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())
        for count in [12, 48, 120]:
            source = scaling_task(count, 1200, 300)['source']
            Draft202012Validator(schema).validate(source)
            self.assertEqual(check_contract(source, source['canvas'], source, schema), [])
            self.assertEqual(len(source['elements']), count)
