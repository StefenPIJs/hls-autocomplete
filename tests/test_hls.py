import unittest
import mock
import subprocess
import datetime

from hls_autocomplete.hls import HlsHdfs, WebHdfsLister
from hls_autocomplete.parse import FileStatus

class TestHls(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_nominal_case(self, popen_mock):
        process_mock = mock.MagicMock()
        process_mock.communicate.return_value = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music", None
        process_mock.returncode = 0
        popen_mock.return_value = process_mock

        lister = HlsHdfs()
        self.assertEqual((0, [FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27))]), lister.hls("/Users/simon/"))
        popen_mock.assert_called_once_with(['hdfs', 'dfs', '-ls', '/Users/simon/'], stdout=subprocess.PIPE)

class TestWebHdfsLister(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_get_process(self, popen_mock):
        popen_mock.return_value = "cmd_result"

        lister = WebHdfsLister("server", "simon.dolle@gmail.com")
        self.assertEqual("cmd_result", lister.get_process("/foo/bar"))
        popen_mock.assert_called_once_with(['curl', '--negotiate', '-i', '-L', '-u:simon.dolle@gmail.com', 'server/foo/bar?op=LISTSTATUS'])

    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_nominal_case(self, popen_mock):
            status_list = '''{"FileStatuses": {"FileStatus": [
            {"pathSuffix": "bar", "type": "DIRECTORY", "length": 0, "owner": "simon", "group": "staff",
             "permission": "700", "accessTime": 0, "modificationTime": 1461236412807, "blockSize": 0, "replication": 0},
            {"pathSuffix": "qux", "type": "FILE", "length": 0, "owner": "simon",
             "group": "staff", "permission": "775", "accessTime": 0, "modificationTime": 1473691319065,
             "blockSize": 0, "replication": 0}]}}'''

            process_mock = mock.MagicMock()
            process_mock.communicate.return_value = status_list, None
            process_mock.returncode = 0
            popen_mock.return_value = process_mock

            lister = WebHdfsLister("server", "simon.dolle@gmail.com")
            self.assertEqual(
                (0, [FileStatus("/foo/bar", "drwx------", 0, "simon", "staff", 0, datetime.date(2016, 4, 21), "bar"),
                     FileStatus("/foo/qux", "-rwxrwxr-x", 0, "simon", "staff", 0, datetime.date(2016, 9, 12), "qux")
                ]),
                lister.list_status("/foo"))
            popen_mock.assert_called_once_with(['curl', '--negotiate', '-i', '-L', '-u:simon.dolle@gmail.com', 'server/foo?op=LISTSTATUS'])