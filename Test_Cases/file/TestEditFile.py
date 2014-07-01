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

class TestEditFile(unittest.TestCase):

    def setUp(self):
        print self._testMethodName + " begins now......"
        self.request = Client()
        if self._testMethodName == "test_editfile_ownerself_filenotfound_fail" or self._testMethodName == "test_editfile_ownerself_success" or self._testMethodName == "test_editfile_ownernotself_filenotfound_fail" or self._testMethodName == "test_editfile_ownernotself_success":
            # create a session for client
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
            engine = import_module(settings.SESSION_ENGINE)
            store = engine.SessionStore()
            store.save()
            self.request.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
            session = store
            session["username"] = "test.account"
            session.save()

    def test_editfile_ownerself_notlogin_fail(self):
        response = self.prepare_dataload_and_send_request("Me", "testData.txt", "The content is changed by unit test!")
        self.assertEqual(response.content, "notlogin")

    def test_editfile_ownerself_filenotfound_fail(self):
        response = self.prepare_dataload_and_send_request("Me", "testData_notfound.txt", "The content is changed by unit test!")
        self.assertEqual(response.content, "notfound")
        
    def test_editfile_ownerself_success(self):
        newContent = "The content is changed by unit test!" + "".join(random.choice(string.lowercase+string.uppercase+string.digits) for x in range(20))
        response = self.prepare_dataload_and_send_request("Me", "testData.txt", newContent)
        self.assertEqual(response.content, "success")
        
    def test_editfile_ownernotself_notlogin_fail(self):
        response = self.prepare_dataload_and_send_request("kriyazhao", "proposal.txt", "proposals: problems: enxr proc crash, timing issue. unexpected error (e.g., False, PoA2 is not synchronized peer, Couldn't find command 'cfgmgr_show_ltrace -v' in output: 'ipc/gl/config/startup) 1.web app:	 - 2 continous failures probabilty very low - if unexpected result found,rerun - statitic data about why certain have crashed. 2.some code can be committed . <div><br></div><div>The content is changed by unit test!</div>")
        self.assertEqual(response.content, "notlogin")

    def test_editfile_ownernotself_filenotfound_fail(self):
        response = self.prepare_dataload_and_send_request("kriyazhao", "proposal_notfound.txt", "proposals: problems: enxr proc crash, timing issue. unexpected error (e.g., False, PoA2 is not synchronized peer, Couldn't find command 'cfgmgr_show_ltrace -v' in output: 'ipc/gl/config/startup) 1.web app:	 - 2 continous failures probabilty very low - if unexpected result found,rerun - statitic data about why certain have crashed. 2.some code can be committed . <div><br></div><div>The content is changed by unit test!</div>")
        self.assertEqual(response.content, "notfound")

    def test_editfile_ownernotself_success(self):
        newContent = "proposals: problems: enxr proc crash, timing issue. unexpected error (e.g., False, PoA2 is not synchronized peer, Couldn't find command 'cfgmgr_show_ltrace -v' in output: 'ipc/gl/config/startup) 1.web app:	 - 2 continous failures probabilty very low - if unexpected result found,rerun - statitic data about why certain have crashed. 2.some code can be committed . <div><br></div><div>The content is changed by unit test!" + "".join(random.choice(string.lowercase+string.uppercase+string.digits) for x in range(20)) + "</div>"
        response = self.prepare_dataload_and_send_request("kriyazhao", "proposal.txt", newContent)
        self.assertEqual(response.content, "success")
        
    def prepare_dataload_and_send_request(self,owner,fn, content):
        payload = json.dumps({"owner":owner, "filename":fn, "content":content})
        return self.request.post("/editfile/", data = payload, content_type="application/json")

    def tearDown(self):
        del self.request
    
if __name__ == "__main__":
    unittest.main()
    
"""
test_editfile_ownernotself_filenotfound_fail begins now......
.test_editfile_ownernotself_notlogin_fail begins now......
.test_editfile_ownernotself_success begins now......
INFO:root:newMD5: 411926c4576dbc2db6e60b061acc534b1
INFO:root:newSHA1: b5aba57ecf95f38d1cfa633a1fd6a8dcb60a4c46
INFO:root:Adding a new fileContent at: /var/www/fs/NFS_Django/NFS_Django/data/411926/c4576d/bc2db6/e60b06/1acc53/4b1/b5aba57ecf95f38d1cfa633a1fd6a8dcb60a4c46.obj
INFO:root:Deleting the old fileContent at: /var/www/fs/NFS_Django/NFS_Django/data/c8e1/fe04/4114/8fb7/446c/1480/81f8/74f9/1/a58cf40ef70f7c2dd628a3a2fe9d566bcaa48485.obj
.test_editfile_ownerself_filenotfound_fail begins now......
.test_editfile_ownerself_notlogin_fail begins now......
.test_editfile_ownerself_success begins now......
INFO:root:newMD5: 319dc84898006e4d7ea421e574c5d0ce11
INFO:root:newSHA1: 6deb069b7563a9ed3e7520c05e2f8f0a96c0236c
INFO:root:Adding a new fileContent at: /var/www/fs/NFS_Django/NFS_Django/data/319d/c848/9800/6e4d/7ea4/21e5/74c5/d0ce/11/6deb069b7563a9ed3e7520c05e2f8f0a96c0236c.obj
INFO:root:Deleting the old fileContent at: /var/www/fs/NFS_Django/NFS_Django/data/e6/a0/39/86/eb/fe/fa/7f/ad/fb/24/9b/7a/00/2a/85/11/d88ef1e6922964de7f8b127d639b0b75f1d66864.obj
.
----------------------------------------------------------------------
Ran 6 tests in 0.085s

OK

"""