import unittest
import json
import sys, os
sys.path.append("/var/www/fs/NFS_Django/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFS_Django.settings")
from django.test import Client
from django.conf import settings
from django.utils.importlib import import_module

class TestRegister(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()

    def test_register_loggedin_fail(self):
        # create a session for client
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        session = store
        session["username"] = "test.account"
        session.save()
        
        response = self.prepare_dataload_and_send_request("testAccount", "$RFV4rfv", "test", "account", "test.account@test.ca")
        self.assertEqual(json.loads(response.content)['r'], "loggedin")
        self.assertEqual(json.loads(response.content)['un'], "test.account")
   
    def test_register_input_invalid_fail(self):
        response = self.prepare_dataload_and_send_request("", "1qaz1qaz", "fste", "asfef", "efs@gsce.ca")
        self.assertEqual(json.loads(response.content)['r'], "notvalid")

    def test_register_usernameused_fail(self):
        response = self.prepare_dataload_and_send_request("kriyazhao", "$RFV4rfv", "fste", "asfef", "test.account2@test.ca")
        self.assertEqual(json.loads(response.content)['r'], "usernameexist")

    def test_register_emailused_fail(self):
        response = self.prepare_dataload_and_send_request("kriyazhao1", "$RFV4rfv", "fste", "asfef", "t.zhao2011@gmail.com")
        self.assertEqual(json.loads(response.content)['r'], "emailexist")
        
    def test_register_success(self):
        response = self.prepare_dataload_and_send_request("test.account2", "$RFV4rfv", "test", "account", "test.account2@test.ca")
        self.assertEqual(json.loads(response.content)['r'], "success")
        self.assertEqual(json.loads(response.content)['un'], "test.account2")   
        
    def prepare_dataload_and_send_request(self,un,pw,fn,ln,em):
        payload = json.dumps({"un":un, "pw":pw, "fn":fn, "ln":ln, "em":em})
        return self.request.post("/register/", data = payload, content_type="application/json")

    def tearDown(self):
        del self.request
    
if __name__ == "__main__":
    unittest.main()
    
