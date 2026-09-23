"""Security regression probes use non-authenticating synthetic markers only."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCANNER = Path(__file__).with_name('validate_publication.py')

class PublicationBoundary(unittest.TestCase):
    def probe(self, name, value, accepted=False):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'scripts').mkdir()
            shutil.copy2(SCANNER, root / 'scripts/validate_publication.py')
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
            result = subprocess.run(['python3', str(root / 'scripts/validate_publication.py')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0 if accepted else 1, result.stdout + result.stderr)
            if not accepted:
                self.assertNotIn(value, result.stdout)

    def test_real_private_key_header_forms(self):
        for prefix in ['', 'RSA ', 'OPENSSH ', 'EC ', 'ENCRYPTED ']:
            with self.subTest(prefix=prefix):
                self.probe('example.txt', '-----BEGIN ' + prefix + 'PRIVATE KEY-----')

    def test_real_environment_names(self):
        for name in ['.env', '.env.production', 'runtime.env']:
            with self.subTest(name=name):
                self.probe(name, 'NON_AUTHENTICATING_FIXTURE=yes')

    def test_temporary_aws_key_marker(self):
        self.probe('example.md', 'AS' + 'IA' + 'X' * 16)

    def test_private_home(self):
        self.probe('example.md', '/ho' + 'me/privateuser/source')

    def test_unapproved_repository(self):
        self.probe('example.md', 'https://github.com/arussellbishop/' + 'nonpublic-fixture')

    def test_dataset(self):
        self.probe('example.csv', 'synthetic,data')

    def test_state(self):
        self.probe('example.tfstate', '{}')

    def test_unapproved_address(self):
        self.probe('example.md', '192.' + '0.2.20')

    def test_approved_cidr_only_in_terraform(self):
        cidr = '10.' + '42.1.0/24'
        self.probe('terraform/example.tf', 'locals { sample = "' + cidr + '" }', True)
        self.probe('example.md', cidr)

    def test_public_repository(self):
        self.probe('example.md', 'https://github.com/arussellbishop/applied-ai-cloud-portfolio', True)

if __name__ == '__main__':
    unittest.main()
