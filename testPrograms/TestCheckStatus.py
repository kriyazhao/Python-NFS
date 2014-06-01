import unittest
import requests
import json
import CheckLogin

class TestCheckStatus(unittest.TestCase):
    global session
    
    def test_login_fail(self):
        session.logged_in = False
        response = requests.get("/checklogin")
        self.assertEqual(response.r, 0)
        
    def test_login_success(self):
        session.logged_in = True
        session.username = "kriyazhao"
        response = requests.get("/checklogin")
        session.logged_in = False
        session.kill()
        self.assertEqual(response.r, 1)
    
    def test_login_success_return_username(self):
        session.logged_in = True
        session.username = "kriyazhao"
        response = requests.get("/checklogin")
        session.logged_in = False
        session.kill()
        self.assertEqual(response.username, "kriyazhao")
    
if __name__ == "__main__":
    unitest.main()
