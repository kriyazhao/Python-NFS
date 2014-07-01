import unittest
import json
import sys, os
sys.path.append("/var/www/fs/NFS_Django/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFS_Django.settings")
from django.test import Client
from django.conf import settings
from django.utils.importlib import import_module

class TestLogin(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()

    def test_login_username_invalid_fail(self):
        response = self.prepare_dataload_and_send_request("kr", "1qaz1qaz!E")
        self.assertEqual(json.loads(response.content)['r'], 3)
   
    def test_login_password_invalid_fail(self):
        response = self.prepare_dataload_and_send_request("kriya", "1qaz1qaz")
        self.assertEqual(json.loads(response.content)['r'], 3)

    def test_login_loggedin_fail(self):
        # create a session for client
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        session = store
        session["username"] = "test.account"
        session.save()
        
        response = self.prepare_dataload_and_send_request("test.account", "#EDC3edc")
        self.assertEqual(json.loads(response.content)['r'], 2)
        self.assertEqual(json.loads(response.content)['un'], "test.account")

    def test_login_incorrect_fail(self):
        response = self.prepare_dataload_and_send_request("test.account", "$RFV4rfv")
        self.assertEqual(json.loads(response.content)['r'], 0)
        
    def test_login_success(self):
        response = self.prepare_dataload_and_send_request("test.account", "#EDC3edc")
        self.assertEqual(json.loads(response.content)['r'], 1)
        self.assertEqual(json.loads(response.content)['un'], "test.account")   
        
    def prepare_dataload_and_send_request(self,un,pw):
        payload = json.dumps({"un":un, "pw":pw})
        return self.request.post("/login/", data = payload, content_type="application/json")

    def tearDown(self):
        del self.request
    
if __name__ == "__main__":
    unittest.main()