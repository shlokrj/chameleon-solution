"""Regression and metamorphic checks for rotated text and source grids."""
import copy
import unittest
from engine.layout import source_grid
from engine.resize import resize_with_diagnostics
from engine.quality import quality
from evaluation.contract import check_contract
from tests.test_relationships import fixture, SCHEMA


class TextLayoutTests(unittest.TestCase):
    def checked(self, task):
        original = copy.deepcopy(task)
        output, diagnostics = resize_with_diagnostics(task['source'], task['target_canvas'])
        self.assertEqual(task, original)
        self.assertEqual(check_contract(task['source'], task['target_canvas'], output, SCHEMA), [])
        self.assertEqual(quality(task['source'], output)['overflow_ids'], [])
        self.assertLessEqual(diagnostics['candidate_count'], 6)
        return output, diagnostics

    def test_rotated_copy_preserves_readable_size_at_multiple_angles(self):
        for angle in [-90, 30, 45, 90, 180, 270]:
            with self.subTest(angle=angle):
                task = fixture('rotated-copy')
                task['source']['elements'][0]['rotation'] = angle
                output, _ = self.checked(task)
                self.assertGreaterEqual(output['elements'][0]['font_size'], 28)

    def test_grid_readability_and_reading_order(self):
        task = fixture('dense-labels')
        output, diagnostics = self.checked(task)
        self.assertTrue(diagnostics['candidates'][diagnostics['selected']]['text_grid'])
        self.assertGreaterEqual(min(e['font_size'] for e in output['elements']), 28)
        positions = [(e['y'], e['x']) for e in output['elements']]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(quality(task['source'], output)['new_overlap'], 0)
        self.assertEqual((output, diagnostics), resize_with_diagnostics(task['source'], task['target_canvas']))

    def test_grid_rename_and_reorder_do_not_change_geometry(self):
        task = fixture('dense-labels')
        expected, _ = self.checked(task)
        for el in task['source']['elements']:
            el['id'] = 'opaque-'+el['id']
        task['source']['elements'].reverse()
        actual, _ = self.checked(task)
        for left, right in zip(expected['elements'], reversed(actual['elements'])):
            for key in ['x', 'y', 'width', 'height', 'font_size']:
                self.assertEqual(left[key], right[key])

    def test_subpixel_grid_offsets_keep_readable_columns(self):
        task = fixture('dense-labels')
        for i, el in enumerate(task['source']['elements']):
            el['y'] += (2-i % 3)*0.25
            el['x'] += (i // 3)*0.25
        output, _ = self.checked(task)
        self.assertGreaterEqual(min(e['font_size'] for e in output['elements']), 28)

    def test_incomplete_or_overlapping_rows_do_not_imply_grid(self):
        for mutation in ['missing', 'overlap', 'misaligned']:
            task = fixture('dense-labels')
            els = task['source']['elements']
            if mutation == 'missing':
                els.pop()
            elif mutation == 'overlap':
                els[0]['width'] = 250
            else:
                els[-1]['x'] += 10
            self.assertIsNone(source_grid([[e] for e in els]))

    def test_small_candidate_budget_keeps_valid_fallback(self):
        task = fixture('dense-labels')
        out, d = resize_with_diagnostics(task['source'], task['target_canvas'], max_candidates=1)
        self.assertEqual(d['candidate_count'], 1)
        self.assertEqual(check_contract(task['source'], task['target_canvas'], out, SCHEMA), [])
