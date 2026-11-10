"""Controles offline: ejecutar con python -m unittest discover -s Experimentos -v."""
import unittest
from controles import articles, windows, labelled, mix_targets, stable_seed, lexical_metrics


class ProtocolTests(unittest.TestCase):
    def test_article_boundaries_and_subheadings(self):
        rows = [' = One = \n', 'alpha', ' == Sub == \n', 'beta', ' = Two = \n', 'gamma']
        docs = articles(rows)
        self.assertEqual(len(docs), 2)
        self.assertIn('beta', docs[0]['text'])
        self.assertNotIn('gamma', docs[0]['text'])
        self.assertNotIn('One', docs[0]['text'])

    def test_no_cross_article_or_overlapping_windows(self):
        docs = [{'article': 'a', 'tokens': list(range(13))},
                {'article': 'b', 'tokens': list(range(100, 105))}]
        blocks = windows(docs, 2, 3, 'train')
        self.assertEqual([x['offset'] for x in blocks], [0, 5, 0])
        self.assertEqual(blocks[1]['context'] + blocks[1]['target'], list(range(5, 10)))
        self.assertEqual(blocks[2]['target'], [102, 103, 104])
        self.assertEqual(len({x['id'] for x in blocks}), 3)

    def test_context_and_padding_are_not_training_targets(self):
        ids, mask, labels = labelled([8, 9], [10, 11, 12], pad_id=1, length=7)
        self.assertEqual(ids, [8, 9, 10, 11, 12, 1, 1])
        self.assertEqual(mask, [1, 1, 1, 1, 1, 0, 0])
        self.assertEqual(labels, [-100, -100, 10, 11, 12, -100, -100])

    def test_mixture_is_exact_and_keeps_human_context(self):
        human = [{'id': str(i), 'context': [i], 'target': [7, 7, 7, 7]} for i in range(4)]
        synthetic = [[9, 9, 9, 9] for _ in human]
        out = mix_targets(human, synthetic, .5, 42)
        self.assertEqual(sum(x['synthetic'] for x in out), 2)
        self.assertEqual(sum(x['target'].count(9) for x in out), 8)
        self.assertEqual([x['context'] for x in out], [[i] for i in range(4)])
        self.assertEqual(human[0]['target'], [7, 7, 7, 7])
        with self.assertRaises(ValueError):
            mix_targets(human, [[9]] * 4, 1, 42)
        with self.assertRaises(ValueError):
            mix_targets(human, synthetic, .3, 42)

    def test_seeds_stable_and_namespaces_separate(self):
        self.assertEqual(stable_seed(42, 'train', 1), stable_seed(42, 'train', 1))
        self.assertNotEqual(stable_seed(42, 'train', 1), stable_seed(42, 'eval', 1))

    def test_lexical_metrics_do_not_cross_text_boundaries(self):
        m = lexical_metrics(['A b a b a b', 'c d c d c d'], 6)
        self.assertAlmostEqual(m['distinct_2'], 4 / 10)
        self.assertAlmostEqual(m['repeat_4_mean'], 1 / 3)
        self.assertEqual(m['short_texts'], 0)

    def test_short_texts_are_not_silently_dropped(self):
        m = lexical_metrics(['a b c d', 'a'], 4)
        self.assertEqual(m['short_texts'], 1)
        self.assertIsNone(m['distinct_2'])
        self.assertIsNone(m['repeat_4_mean'])


if __name__ == '__main__':
    unittest.main()
