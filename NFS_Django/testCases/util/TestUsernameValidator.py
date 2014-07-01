import unittest
import requests
import json
import Register
from NFS_Django.views.util.UserValidator import UserValidator

class TestUsernameValidator(unittest.TestCase):

    def setUp(self):
        print "TestUsernameValidator begins now......"
        validator = UserValidator()
    
    def test_username_empty_fail(self):
        validator.setUsername("")
        self.assertTrue(validator.usernameValidator())
        
    def test_username_onlynum_fail(self):
        validator.setUsername("12345")
        self.assertTrue(validator.usernameValidator())

    def test_username_startsnum_fail(self):
        validator.setUsername("12345ting")
        self.assertTrue(validator.usernameValidator())

    def test_username_short_fail(self):
        validator.setUsername("ti")
        self.assertTrue(validator.usernameValidator())
        
    def test_username_valid_success(self):
        validator.setUsername("ting123")
        self.assertTrue(validator.usernameValidator())
  
    def tearDown(self):
        del validator
    
if __name__ == "__main__":
    unitest.main()
