import unittest
import json
import sys
sys.path.append("/var/www/fs/NFS_Django/")
from NFS_Django.views.util.UserValidator import UserValidator

class TestLastnameValidator(unittest.TestCase):

    def setUp(self): 
        print self._testMethodName + " begins now......"
        self.validator = UserValidator()
    
    def test_lastname_empty_fail(self):
        self.validator.setLastName("")
        self.assertFalse(self.validator.lastnameValidate())
        
    def test_lastname_num_fail(self):
        self.validator.setLastName("12345")
        self.assertFalse(self.validator.lastnameValidate())

    def test_lastname_long_fail(self):
        self.validator.setLastName("SDFESDFSFESDFEFSSGRGRGDFSDRADAAFFSGDRGERG")
        self.assertFalse(self.validator.lastnameValidate())
        
    def test_lastname_valid_success(self):
        self.validator.setLastName("Zhao")
        self.assertTrue(self.validator.lastnameValidate())
  
    def tearDown(self):
        del self.validator
    
if __name__ == "__main__":
    unittest.main()