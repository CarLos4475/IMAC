import json
import tempfile
import unittest
from pathlib import Path
from estado_principal_es import make_plan, freeze_protocol, commit_stage, stage_complete, final_selection, cached_chunk, save_chunk


class MainProtocolTests(unittest.TestCase):
    def test_48_adjustments_and_shared_initial_points(self):
        jobs = make_plan()
        self.assertEqual(len(jobs), 48)
        self.assertEqual(sum(x['cycle'] == 0 for x in jobs), 3)
        for job in jobs:
            if job['cycle'] == 1:
                self.assertEqual(job['parent'], f"r{job['rep']}_M0")
            elif job['cycle'] > 1:
                self.assertIn(f"g{job['cycle']-1}", job['parent'])

    def test_resume_rejects_configuration_or_environment_change(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            root = Path(temp)
            signature = freeze_protocol(root, {'seed': 1}, {'torch': 'x'})
            self.assertEqual(signature, freeze_protocol(root, {'seed': 1}, {'torch': 'x'}))
            with self.assertRaises(ValueError):
                freeze_protocol(root, {'seed': 2}, {'torch': 'x'})
            with self.assertRaises(ValueError):
                freeze_protocol(root, {'seed': 1}, {'torch': 'y'})

    def test_json_roundtrip_does_not_change_tuple_configuration(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            spec = {'alphas': (0.0, 0.5, 1.0)}
            first = freeze_protocol(Path(temp), spec, {'torch': 'x'})
            self.assertEqual(first, freeze_protocol(Path(temp), spec, {'torch': 'x'}))

    def test_incomplete_stage_is_not_skipped_and_corruption_stops_resume(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            root = Path(temp)
            (root/'metrics.json').write_text('{}', encoding='utf-8')
            self.assertFalse(stage_complete(root, 'spec'))
            commit_stage(root, 'spec', ['metrics.json'], {'rep': 0})
            self.assertTrue(stage_complete(root, 'spec'))
            (root/'metrics.json').write_text('{"changed":true}', encoding='utf-8')
            with self.assertRaises(ValueError):
                stage_complete(root, 'spec')

    def test_validation_and_test_stay_separate(self):
        pools = {s: [{'id': f'{s}{i}', 'article': f'{s}{i}', 'text_sha256': f'{s}{i}',
                       'context': [100*j+i], 'target': [100*j+i+2]} for i in range(6)]
                 for j, s in enumerate(('train', 'validation', 'test'))}
        selected = final_selection(pools, (4, 2, 3), 19)
        self.assertEqual([len(selected[s]) for s in pools], [4, 2, 3])
        pools['test'] = []
        with self.assertRaises(ValueError):
            final_selection(pools, (4, 2, 3), 19)

    def test_cross_partition_content_duplicates_rejected(self):
        pools = {s: [{'id': s, 'article': s, 'text_sha256': 'identical',
                       'context': [1], 'target': [2]}] for s in ('train', 'validation', 'test')}
        with self.assertRaises(ValueError):
            final_selection(pools, (1, 1, 1), 9)

    def test_completed_generation_chunk_is_reused_and_detects_corruption(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            path = Path(temp)/'batch.json'
            self.assertIsNone(cached_chunk(path, 'request'))
            save_chunk(path, 'request', [{'id': 'a', 'target_ids': [9]}])
            self.assertEqual(cached_chunk(path, 'request')[0]['target_ids'], [9])
            with self.assertRaises(ValueError):
                cached_chunk(path, 'different-request')
            value = json.loads(path.read_text(encoding='utf-8'))
            value['outputs'][0]['target_ids'] = [10]
            path.write_text(json.dumps(value), encoding='utf-8')
            with self.assertRaises(ValueError):
                cached_chunk(path, 'request')


if __name__ == '__main__':
    unittest.main()
