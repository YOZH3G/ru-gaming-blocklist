import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_priority_profiles as updater


class BackendRefreshTests(unittest.TestCase):
    def test_complete_and_incomplete_snapshots(self):
        for name, hosts in [('mortal_kombat_1', updater.MK1_RESOLVE_HOSTS),
                            ('mortal_kombat_11', updater.MK11_RESOLVE_HOSTS)]:
            for mode in ('complete', 'partial', 'empty', 'private', 'failed'):
                with self.subTest(game=name, mode=mode), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / 'games').mkdir()
                    filename = 'MortalKombat1.txt' if name.endswith('_1') else 'MortalKombat11.txt'
                    path = root / 'games' / filename
                    original = 'previous.example.com\n8.8.4.4/32\n'
                    path.write_text(original)
                    def resolve(host, *args, **kwargs):
                        if mode == 'failed' or (mode == 'partial' and host == sorted(hosts)[0]):
                            raise socket.gaierror('temporary resolver failure')
                        if mode == 'empty':
                            return []
                        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '',
                                 ('10.0.0.1' if mode == 'private' else '8.8.8.8', 443))]
                    with patch.object(updater, 'ROOT', root), patch.object(updater.socket, 'getaddrinfo', side_effect=resolve):
                        if mode == 'complete':
                            getattr(updater, 'update_' + name)()
                            self.assertIn('8.8.8.8/32', path.read_text())
                            self.assertNotIn('8.8.4.4/32', path.read_text())
                        else:
                            with self.assertRaises(RuntimeError):
                                getattr(updater, 'update_' + name)()
                            self.assertEqual(original, path.read_text())


if __name__ == '__main__':
    unittest.main()
