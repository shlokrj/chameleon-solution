"""Exact overlap-score preservation and candidate-local geometry lifetime."""
import copy
import random
import unittest
from unittest.mock import patch
from engine.layout import bounds
from engine.quality import overlap, quality


def design():
    rng = random.Random(431)
    return {'canvas': {'width': 600, 'height': 600}, 'elements': [
        dict(id=str(i), type='text', content='', font_family='Solstice Sans', font_size=12,
             x=rng.uniform(100, 300), y=rng.uniform(100, 300),
             width=0 if i == 0 else rng.uniform(20, 140), height=rng.uniform(10, 90),
             rotation=rng.choice([-90, -35, 0, 45, 90]),
             **({'group_id': 'pair'} if i in [1, 2] else {})) for i in range(16)]}


def original_collision_score(source, output):
    originals = {e['id']: e for e in source['elements']}
    score = 0.0
    for i, a in enumerate(output['elements']):
        for b in output['elements'][i+1:]:
            if a.get('group_id') is not None and a.get('group_id') == b.get('group_id'):
                continue
            score += max(0, overlap(a, b)-overlap(originals[a['id']], originals[b['id']])-0.01)
    return score


class QualityTests(unittest.TestCase):
    def test_exact_scores_across_rotations_degenerate_boxes_and_groups(self):
        source = design()
        output = copy.deepcopy(source)
        for iteration in range(4):
            for i, el in enumerate(output['elements']):
                el['x'] += i * 3
                el['width'] *= 0.9
            self.assertEqual(quality(source, output)['new_overlap'], original_collision_score(source, output))

    def test_bounds_work_is_linear_per_quality_evaluation(self):
        source = design()
        with patch('engine.quality.bounds', wraps=bounds) as measured:
            quality(source, source)
        self.assertEqual(measured.call_count, 2 * len(source['elements']))

    def test_repeated_candidate_mutations_do_not_reuse_stale_bounds(self):
        source = design()
        untouched = copy.deepcopy(source)
        output = copy.deepcopy(source)
        self.assertEqual(quality(source, output)['new_overlap'], 0)
        for el in output['elements']:
            el.update(x=200, y=200)
        expected = original_collision_score(source, output)
        self.assertGreater(expected, 0)
        self.assertEqual(quality(source, output)['new_overlap'], expected)
        self.assertEqual(quality(source, source)['new_overlap'], 0)
        self.assertEqual(source, untouched)
