import unittest
import string
import random
import json
import sys, os
sys.path.append("/var/www/fs/NFS_Django/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFS_Django.settings")
from django.test import Client
from django.conf import settings
from django.utils.importlib import import_module

class TestExtractFile(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()
        if self._testMethodName != "test_extractfile_notlogin_fail":
            # create a session for client
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
            engine = import_module(settings.SESSION_ENGINE)
            store = engine.SessionStore()
            store.save()
            self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
            session = store
            session["username"] = "test.account"
            session.save()

    def test_extractfile_notlogin_fail(self):
        response = self.prepare_dataload_and_send_request("4c48c39477f0328235c598f8ab3219c13", "476c1f4586dc4df2e52fd10083aa6d17e9474266")
        self.assertEqual(json.loads(response.content)[0], "notlogin")

    def test_extractfile_notvalid_fail(self):
        response = self.prepare_dataload_and_send_request("4c48c39477f0328235c598f8a", "476c1f4586dc4df2e52fd10083aa6d17e9474266")
        self.assertEqual(json.loads(response.content)[0], "notvalid")
        
    def test_extractfile_notfound_fail(self):
        response = self.prepare_dataload_and_send_request("4c48c39477f0328235c598f8ab3219c12", "476c1f4586dc4df2e52fd10083aa6d17e9474266")
        self.assertEqual(json.loads(response.content)[0], "notfound")
        
    def test_extractfile_existsharelist_success(self):
        response = self.prepare_dataload_and_send_request("c8e1fe0441148fb7446c148081f874f91", "a58cf40ef70f7c2dd628a3a2fe9d566bcaa48485")
        self.assertEqual(json.loads(response.content)[0], "exist")

    def test_extractfile_owneroffile_success(self):
        response = self.prepare_dataload_and_send_request("8d8da8fa9824d7489bb82a9186c5d48d11", "f84314178232a94b588d327550e5c774dac4a80d")
        self.assertEqual(json.loads(response.content)[0], "owner")

    def test_extractfile_noprivilege_fail(self):
        response = self.prepare_dataload_and_send_request("bf9ef2d11172b9eeca5da3e048827d871", "ca4c5f9dae45f9fd945f052770fd64ff91670a5c")
        self.assertEqual(json.loads(response.content)[0], "restricted")

    def test_extractfile_anyone_success(self):
        response = self.prepare_dataload_and_send_request("dc5e00662b2550473d959a26ceb19c601", "c845b4d3d58b2630cf9a0f41c3b3998d31550e96")
        self.assertEqual(json.loads(response.content)[0], {u'owner': u'kriyazhao', u'privilege': u'11', u'fileAlias': u'2012_ExtractByMask_Batch.py'})
        
    def prepare_dataload_and_send_request(self,md5,sha1):
        payload = json.dumps({"md5":md5, "sha1":sha1})
        return self.request.post("/extractfile/", data = payload, content_type="application/json")

    def tearDown(self):
        del self.request
    
if __name__ == "__main__":
    unittest.main()

"""
test_extractfile_anyone_success begins now......
.test_extractfile_existsharelist_success begins now......
.test_extractfile_noprivilege_fail begins now......
.test_extractfile_notfound_fail begins now......
.test_extractfile_notlogin_fail begins now......
.test_extractfile_notvalid_fail begins now......
.test_extractfile_owneroffile_success begins now......
.
----------------------------------------------------------------------
Ran 7 tests in 0.061s

OK

"""