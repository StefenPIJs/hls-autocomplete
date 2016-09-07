import unittest

from hls_complete import complete

class TestSplitPath(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals(["user", "s.dolle", "Music"], complete.split_path("/user/s.dolle/Music"))
        self.assertEquals(["user", "s.dolle", "Music"], complete.split_path("/user/s.dolle/Music/"))

class TestAppendSlash(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/user/s.dolle/Music/", complete.append_slash("/user/s.dolle/Music", True))
        self.assertEquals("/user/s.dolle/Music", complete.append_slash("/user/s.dolle/Music", False))
