"""Failure-path tests run without Docker, network, root, or production writes."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('receiver', Path(__file__).with_name('deploy.py'))
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)


class DeploymentTests(unittest.TestCase):
    def test_reject_non_main(self):
        with patch.object(receiver, 'api', return_value={'object': {'sha': 'b' * 40}}):
            with self.assertRaises(ValueError):
                receiver.verify_ci('a' * 40)

    def test_reject_failed_ci(self):
        responses = [{'object': {'sha': 'a' * 40}}, {'workflow_runs': [{'head_sha': 'a' * 40, 'conclusion': 'failure'}]}]
        with patch.object(receiver, 'api', side_effect=responses):
            with self.assertRaises(ValueError):
                receiver.verify_ci('a' * 40)

    def test_reject_archive_traversal_and_symlink(self):
        for name, kind in [('repo/site/../../escape.html', tarfile.REGTYPE), ('repo/site/index.html', tarfile.SYMTYPE)]:
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode='w:gz') as archive:
                item = tarfile.TarInfo(name)
                item.type = kind
                archive.addfile(item)
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError):
                    receiver.extract_site(stream.getvalue(), Path(directory))

    def test_rollback_rejects_stale_sha(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            current = base / ('b' * 40)
            current.mkdir()
            (base / 'current').symlink_to(current)
            with patch.object(receiver, 'BASE', base), patch.object(receiver, 'compose') as compose:
                with self.assertRaises(ValueError):
                    receiver.rollback('a' * 40)
                compose.assert_not_called()

    def test_health_failure_restores_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            old = base / 'releases' / 'previous-release'
            old.mkdir(parents=True)
            (base / 'template').mkdir()
            (base / 'current').symlink_to(old)
            with patch.object(receiver, 'BASE', base), patch.object(receiver, 'verify_ci'), patch.object(receiver, 'fetch'), patch.object(receiver, 'extract_site'), patch.object(receiver, 'compose') as compose, patch.object(receiver, 'health', side_effect=[RuntimeError('unhealthy'), None]):
                with self.assertRaisesRegex(RuntimeError, 'unhealthy'):
                    receiver.deploy('a' * 40)
                self.assertEqual((base / 'current').resolve(), old)
                self.assertEqual(compose.call_args.args[0], old)
                self.assertIn('--no-build', compose.call_args.args)


if __name__ == '__main__':
    unittest.main()
