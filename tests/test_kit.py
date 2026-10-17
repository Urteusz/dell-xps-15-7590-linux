import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


setup = module('setup', 'setup.py')
login = module('login', 'fix-login.py')


class KitTests(unittest.TestCase):
    def test_reject_other_distribution_model_arch(self):
        good = {'ID': 'fedora', 'VERSION_ID': '43'}
        for info, model, arch in [({'ID': 'ubuntu'}, 'XPS 15 7590', 'x86_64'),
                                  (good, 'XPS 15 9570', 'x86_64'),
                                  (good, 'XPS 15 7590', 'aarch64')]:
            with self.assertRaises(ValueError):
                setup.validate_host(info, model, arch)

    def test_dry_run_never_executes(self):
        with patch.object(setup.subprocess, 'run') as run:
            setup.execute(['sudo', 'dnf', 'install', 'kernel'], False)
            run.assert_not_called()

    def test_bundle_rejects_modified_missing_and_added_rpms(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            rpm = path / 'test.rpm'
            rpm.write_bytes(b'test')
            data = {'fedora_release': '43', 'arch': 'x86_64', 'sha256': setup.bundle_hashes(path)}
            (path / 'bundle.json').write_text(json.dumps(data))
            self.assertEqual(setup.check_bundle(path), [str(rpm)])
            rpm.write_bytes(b'changed')
            with self.assertRaises(ValueError):
                setup.check_bundle(path)
            rpm.unlink()
            with self.assertRaises(ValueError):
                setup.check_bundle(path)
            rpm.write_bytes(b'test')
            (path / 'extra.rpm').write_bytes(b'extra')
            with self.assertRaises(ValueError):
                setup.check_bundle(path)

    def test_pam_changes_only_fingerprint_line(self):
        original = ('auth sufficient pam_fprintd.so\n'
                    'auth substack password-auth\n'
                    'account include password-auth\n'
                    'session required pam_selinux.so open\n')
        updated = login.patched(original)
        self.assertIn('timeout=8 max-tries=1', updated)
        self.assertEqual(original.splitlines()[1:], updated.splitlines()[1:])
        self.assertEqual(login.patched(updated), updated)
        self.assertNotIn('pam_fprintd.so', login.patched(original, 'password'))

    def test_unexpected_pam_fails_closed(self):
        for text in ['auth sufficient pam_unix.so\n',
                     'auth sufficient pam_fprintd.so\n',
                     'auth sufficient pam_fprintd.so\nauth sufficient pam_fprintd.so\nauth substack password-auth\n']:
            with self.assertRaises(ValueError):
                login.patched(text)


if __name__ == '__main__':
    unittest.main()
