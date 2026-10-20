import copy
import unittest
from unittest.mock import patch
from engine.resize import resize_with_diagnostics, MAX_CANDIDATES
from engine.quality import hard_issues, regression_reasons
from evaluation.development import tasks
from evaluation.contract import check_contract
import json
from pathlib import Path

SCHEMA = json.loads(Path('chameleon_design_schema_v0.9.json').read_text())


def simple():
    return {'canvas': {'width': 200, 'height': 200}, 'elements': [
        {'id': 'a', 'type': 'text', 'x': 10, 'y': 10, 'width': 150, 'height': 30,
         'content': 'Preserve this text', 'font_family': 'Solstice Sans', 'font_size': 4,
         'color': 'white'}]}


class SelectionTests(unittest.TestCase):
    def test_development_contracts_and_budget(self):
        for task in tasks():
            with self.subTest(case=task['case']):
                source = copy.deepcopy(task['source'])
                out, d = resize_with_diagnostics(source, task['target_canvas'])
                self.assertEqual(check_contract(task['source'], task['target_canvas'], out, SCHEMA), [])
                self.assertEqual(source, task['source'])
                self.assertLessEqual(d['candidate_count'], MAX_CANDIDATES)
                self.assertEqual((out, d), resize_with_diagnostics(source, task['target_canvas']))

    def test_compact_dense_groups_use_available_bottom_space(self):
        task = json.loads(Path('input/chameleon_sample_level3_advanced.json').read_text())
        target = {'width': 300, 'height': 250}
        source = copy.deepcopy(task['source'])
        # Opaque IDs prevent the regression fixture from depending on semantic
        # names. The three short badge labels should retain their scaled size.
        badge_ids = {'badge1_label', 'badge2_label', 'badge3_label'}
        renamed_badges = []
        for i, el in enumerate(source['elements']):
            if el['id'] in badge_ids:
                renamed_badges.append(str(i))
            el['id'] = str(i)
        result, diagnostics = resize_with_diagnostics(source, target)
        elements = {el['id']: el for el in result['elements']}
        for eid in renamed_badges:
            self.assertGreaterEqual(elements[eid]['font_size'], 4.16)
        self.assertEqual(check_contract(source, target, result, SCHEMA), [])
        self.assertLessEqual(diagnostics['candidate_count'], MAX_CANDIDATES)

    def test_bad_candidates_cannot_win(self):
        source = simple()
        invalid = copy.deepcopy(source)
        invalid['elements'][0]['content'] = 'dishonest replacement'
        with patch('engine.resize.build_layout', side_effect=[copy.deepcopy(source), invalid]):
            out, d = resize_with_diagnostics(source, source['canvas'], max_candidates=2)
        self.assertEqual(out, source)
        self.assertEqual(d['selected'], 0)
        self.assertEqual(d['candidates'][1]['status'], 'invalid')

    def test_all_invalid_fails_explicitly(self):
        source = simple()
        invalid = copy.deepcopy(source)
        invalid['elements'][0]['x'] = -100
        with patch('engine.resize.build_layout', return_value=invalid) as build:
            with self.assertRaisesRegex(ValueError, 'No structurally valid'):
                resize_with_diagnostics(source, source['canvas'])
        self.assertEqual(build.call_count, MAX_CANDIDATES)

    def test_duplicate_candidates_are_bounded(self):
        source = simple()
        with patch('engine.resize.build_layout', return_value=source) as build:
            out, d = resize_with_diagnostics(source, source['canvas'], max_candidates=3)
        self.assertEqual(out, source)
        self.assertEqual(build.call_count, 3)
        self.assertEqual([r['status'] for r in d['candidates']], ['eligible', 'duplicate', 'duplicate'])

    def test_candidate_budget_validation(self):
        source = simple()
        for budget in [0, 7, True, 1.5]:
            with self.assertRaises(ValueError):
                resize_with_diagnostics(source, source['canvas'], max_candidates=budget)

    def test_hard_gate_nonfinite_and_image_distortion(self):
        source = simple()
        invalid = copy.deepcopy(source)
        invalid['elements'][0]['x'] = float('nan')
        self.assertTrue(hard_issues(source, source['canvas'], invalid))
        source['elements'] = [{'id': 'im', 'type': 'image', 'asset_id': 'original.png',
                               'x': 0, 'y': 0, 'width': 40, 'height': 20}]
        invalid = copy.deepcopy(source)
        invalid['elements'][0]['width'] = 60
        self.assertTrue(hard_issues(source, source['canvas'], invalid))

    def test_regression_guard_includes_group_labels(self):
        source = simple()
        source['elements'][0]['group_id'] = 'label-unit'
        changed = copy.deepcopy(source)
        changed['elements'][0]['font_size'] *= 0.9
        self.assertTrue(regression_reasons(source, source, changed))


if __name__ == '__main__':
    unittest.main()
