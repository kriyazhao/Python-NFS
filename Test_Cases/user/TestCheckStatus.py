import unittest
import json
import sys, os
sys.path.append("/var/www/fs/NFS_Django/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFS_Django.settings")
from django.test import Client
from django.conf import settings
from django.utils.importlib import import_module

class TestCheckStatus(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()
        
    def test_CheckStatus_notlogin_success(self):
        response = self.request.get("/checklogin/")
        self.assertEqual(json.loads(response.content)['r'], 0)
        
    def test_CheckStatus_loggedin_success(self):
        # create a session for client
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        session = store
        session["username"] = "test.account"
        session.save()
        
        response = self.request.get("/checklogin/")
        self.assertEqual(json.loads(response.content)['r'], 1)
        self.assertEqual(json.loads(response.content)['un'], "test.account")

    def tearDown(self):
        del self.request
        
if __name__ == "__main__":
    unittest.main()