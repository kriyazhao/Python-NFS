import unittest
import json
import sys, os
sys.path.append("/var/www/fs/NFS_Django/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFS_Django.settings")
from django.test import Client
from django.conf import settings
from django.utils.importlib import import_module

class TestViewFile(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()
        if self._testMethodName == "test_viewfile_ownerself_filenotfound_fail" or self._testMethodName == "test_viewfile_ownerself_success" or self._testMethodName == "test_viewfile_ownernotself_filenotfound_fail" or self._testMethodName == "test_viewfile_ownernotself_success":
            # create a session for client
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
            engine = import_module(settings.SESSION_ENGINE)
            store = engine.SessionStore()
            store.save()
            self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
            session = store
            session["username"] = "test.account"
            session.save()

    def test_viewfile_ownerself_notlogin_fail(self):
        response = self.prepare_dataload_and_send_request("self", "testData.txt")
        self.assertEqual(response.content, "notloggin")

    def test_viewfile_ownerself_filenotfound_fail(self):
        response = self.prepare_dataload_and_send_request("self", "testData_notfound.txt")
        self.assertEqual(response.content, "notfound")
        
    def test_viewfile_ownerself_success(self):
        response = self.prepare_dataload_and_send_request("self", "testData.txt")
        self.assertEqual(response.content, "this is a test file containing all the information that is needed houhouhou")
        
    def test_viewfile_ownernotself_notlogin_fail(self):
        response = self.prepare_dataload_and_send_request("qyin7", "testData - YouBet.txt")
        self.assertEqual(response.content, "notloggin")

    def test_viewfile_ownernotself_filenotfound_fail(self):
        response = self.prepare_dataload_and_send_request("qyin7", "testData.txt")
        self.assertEqual(response.content, "notfound")

    def test_viewfile_ownernotself_success(self):
        response = self.prepare_dataload_and_send_request("qyin7", "testData - YouBet.txt")
        self.assertEqual(response.content, "this is a test file containing all the information that is needed<div><br></div><div>oh really</div>")
        
    def prepare_dataload_and_send_request(self,owner,fn):
        payload = json.dumps({"owner":owner, "filename":fn})
        return self.request.post("/viewfile/", data = payload, content_type="application/json")

    def tearDown(self):
        del self.request
    
if __name__ == "__main__":
    unittest.main()
    
"""

test_viewfile_ownernotself_filenotfound_fail begins now......
test_viewfile_ownernotself_filenotfound_fail is assigning session!
.test_viewfile_ownernotself_notlogin_fail begins now......
.test_viewfile_ownernotself_success begins now......
test_viewfile_ownernotself_success is assigning session!
.test_viewfile_ownerself_filenotfound_fail begins now......
test_viewfile_ownerself_filenotfound_fail is assigning session!
.test_viewfile_ownerself_notlogin_fail begins now......
.test_viewfile_ownerself_success begins now......
test_viewfile_ownerself_success is assigning session!
.

----------------------------------------------------------------------
Ran 6 tests in 0.061s

OK

"""