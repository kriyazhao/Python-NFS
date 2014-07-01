import unittest
import json
import sys
sys.path.append("/var/www/fs/NFS_Django/")
from NFS_Django.views.util.UserValidator import UserValidator

class TestEmailValidator(unittest.TestCase):

    def setUp(self): 
        print self._testMethodName + " begins now......"
        self.validator = UserValidator()
    
    def test_email_empty_fail(self):
        self.validator.setEmail("")
        self.assertFalse(self.validator.emailValidate())
        
    def test_email_noatsymbol_fail(self):
        self.validator.setEmail("12345com")
        self.assertFalse(self.validator.emailValidate())

    def test_email_invalidsymbol_fail(self):
        self.validator.setEmail("ting123#@gm.com")
        self.assertFalse(self.validator.emailValidate())
    
    def test_email_invalidpostfix_fail(self):
        self.validator.setEmail("ting123@gm.commm")
        self.assertFalse(self.validator.emailValidate())
        
    def test_email_valid_success(self):
        self.validator.setEmail("t.zhao2011@gmail.com")
        self.assertTrue(self.validator.emailValidate())
  
    def tearDown(self):
        del self.validator
    
if __name__ == "__main__":
    unittest.main()