
import unittest

from packaging.version import Version

from pypipackagemanagement.pypiversionmanagement import _capture_versions, _max_version, bump_dev_version,\
    get_latest_version


class TestPyPiVersionManagement(unittest.TestCase):

    def setUp(self):
        self._captured_versions = _capture_versions("opencmiss.utils")

    def test_version_capture(self):
        self.assertGreater(len(self._captured_versions), 0)
        self.assertIn(Version("0.1.8"), self._captured_versions)

    def test_max_version(self):
        max_version = _max_version(self._captured_versions)
        self.assertEqual(max_version, Version("0.1.8"))

    def test_increment_dev(self):
        bumped_version_1 = bump_dev_version(Version("0.1.8"))
        self.assertEqual(bumped_version_1, Version("0.1.8.dev0"))
        bumped_version_2 = bump_dev_version(Version("0.1.7a2"))
        self.assertEqual(bumped_version_2, Version("0.1.7a2.dev0"))
        bumped_version_3 = bump_dev_version(Version("0.1.6b5"))
        self.assertEqual(bumped_version_3, Version("0.1.6b5.dev0"))
        bumped_version_4 = bump_dev_version(Version("0.1.5rc1"))
        self.assertEqual(bumped_version_4, Version("0.1.5rc1.dev0"))
        bumped_version_5 = bump_dev_version(Version("0.1.4a2.post3"))
        self.assertEqual(bumped_version_5, Version("0.1.4a2.post3.dev0"))
        bumped_version_6 = bump_dev_version(Version("0.1.3a2.dev0"))
        self.assertEqual(bumped_version_6, Version("0.1.3a2.dev1"))
        bumped_version_7 = bump_dev_version(Version("0.1.2a2.post5.dev5"))
        self.assertEqual(bumped_version_7, Version("0.1.2a2.post5.dev6"))
        bumped_version_8 = bump_dev_version(Version("0.1.8.dev3"))
        self.assertEqual(4, bumped_version_8.dev)

    def test_latest_versions(self):
        self.assertEqual(Version("0.1.8"), get_latest_version("opencmiss.utils"))
        self.assertEqual(Version("0.0.0"), get_latest_version("opencmiss.zinc"))
