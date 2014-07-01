import unittest
import json
import sys
sys.path.append("/var/www/fs/NFS_Django/")
from NFS_Django.views.util.UserValidator import UserValidator

class TestFirstnameValidator(unittest.TestCase):

    def setUp(self): 
        print self._testMethodName + " begins now......"
        self.validator = UserValidator()
    
    def test_firstname_empty_fail(self):
        self.validator.setFirstName("")
        self.assertFalse(self.validator.firstnameValidate())
        
    def test_firstname_num_fail(self):
        self.validator.setFirstName("12345")
        self.assertFalse(self.validator.firstnameValidate())

    def test_firstname_long_fail(self):
        self.validator.setFirstName("fseffrssfsfesfsdfsefsdffefdfsfefsdfe")
        self.assertFalse(self.validator.firstnameValidate())
        
    def test_firstname_valid_success(self):
        self.validator.setFirstName("ting")
        self.assertTrue(self.validator.firstnameValidate())
  
    def tearDown(self):
        del self.validator
    
if __name__ == "__main__":
    unittest.main()