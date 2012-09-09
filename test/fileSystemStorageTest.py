import unittest
import time
from datetime import datetime, timedelta
from pyDoubles.framework import empty_spy, when
from storages.filesystemstorage import FileSystemStorage

class FileSystemStorageTest(unittest.TestCase):
    def test_post_id_call_returns_timestamp(self):
        t = datetime(2012, 2, 1, 14, 30,1)
        mock_post = {"pub_date":t}
        f = FileSystemStorage()
        post_id = f._make_post_id(mock_post)
        self.assertEquals(post_id,str(int(time.mktime(t.timetuple()))))

    def test_post_id_gets_set_after_timestamp_is_made_unique(self):
        spyer = empty_spy()
        t = datetime(2012, 2, 1, 14, 30,1)
        next_sec = t + timedelta(1.0/(24*60*60))
        when(spyer.is_valid_post).with_args(str(int(time.mktime(t.timetuple())))).then_return(True)
        when(spyer.is_valid_post).with_args(str(int(time.mktime(next_sec.timetuple())))).then_return(False)
        mock_post = {"pub_date":t}
        f = FileSystemStorage()
        f.is_valid_post = spyer.is_valid_post
        post_id = f._make_post_id(mock_post)
        self.assertEquals(mock_post["pub_date"].second,2)