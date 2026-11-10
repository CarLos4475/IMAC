"""Pruebas adicionales del piloto español, sin GPU ni descargas."""
import unittest
from controles_es import normalized_text, article_partition, spanish_candidates, select_spanish_rows, words, lexical_metrics


class SpanishProtocolTests(unittest.TestCase):
    def test_accents_and_enye_are_preserved(self):
        self.assertEqual(normalized_text('  cancio\u0301n\r\nniño  '), 'canción\nniño')
        self.assertEqual(words(normalized_text('Árbol, niño y acción.')), ['árbol', 'niño', 'y', 'acción'])
        self.assertEqual(words('cancio\u0301n y niño'), ['canción', 'y', 'niño'])
        self.assertEqual(lexical_metrics(['cancio\u0301n y niño feliz'], 4),
                         lexical_metrics(['canción y niño feliz'], 4))

    def test_partition_is_stable_and_uses_all_three_folds(self):
        folds = [article_partition(str(i), 42) for i in range(200)]
        self.assertEqual(set(folds), {'train', 'validation', 'test'})
        self.assertEqual(article_partition('15', 42), article_partition('15', 42))

    def test_article_stays_in_one_partition_and_only_one_window(self):
        rows = [{'id': str(i), 'title': f'Título {i}', 'url': 'https://es.wikipedia.org/',
                 'text': 'Texto en español con suficientes palabras.'} for i in range(70)]
        seen_texts = []
        def tokenize(text):
            seen_texts.append(text)
            return list(range(20))
        pools, audit = spanish_candidates(rows, tokenize, 2, 3, seed=42, max_articles=60)
        self.assertEqual(audit['scanned_articles'], 60)
        self.assertLess(len(seen_texts), 60)  # Los artículos de test no se tokenizan.
        all_rows = pools['train'] + pools['validation']
        self.assertEqual(len(all_rows), len({r['article'] for r in all_rows}))
        self.assertFalse(set(r['article'] for r in pools['train']) &
                         set(r['article'] for r in pools['validation']))
        for row in all_rows:
            self.assertEqual(len(row['context']), 2)
            self.assertEqual(len(row['target']), 3)
            self.assertEqual(row['split'], article_partition(row['article'], 42))
            self.assertEqual(row['offset'] % 5, 0)

    def test_short_articles_are_reported_without_padding(self):
        rows = [{'id': str(i), 'title': 'Corto', 'text': 'corto'} for i in range(40)]
        pools, audit = spanish_candidates(rows, lambda t: [1, 2], 2, 3, 42, 40)
        self.assertEqual(pools, {'train': [], 'validation': []})
        self.assertGreater(audit['too_short_articles'], 0)

    def test_duplicate_reference_text_across_folds_is_rejected(self):
        pools = {'train': [{'article': 'a', 'text_sha256': 'same'}],
                 'validation': [{'article': 'b', 'text_sha256': 'same'}]}
        with self.assertRaises(ValueError):
            select_spanish_rows(pools, 1, 1, 42)

    def test_sample_counts_are_exact_and_pool_must_suffice(self):
        pools = {s: [{'article': f'{s}{i}', 'text_sha256': f'{s}{i}'} for i in range(10)]
                 for s in ('train', 'validation')}
        selected = select_spanish_rows(pools, 4, 3, 42)
        self.assertEqual(len(selected['train']), 4)
        self.assertEqual(len(selected['validation']), 3)
        self.assertEqual(selected, select_spanish_rows(pools, 4, 3, 42))
        with self.assertRaises(ValueError):
            select_spanish_rows(pools, 11, 3, 42)


if __name__ == '__main__':
    unittest.main()
