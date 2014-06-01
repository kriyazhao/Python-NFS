import unittest
import requests
import json
import Register

class TestRegister(unittest.TestCase):
    global session
    
    def test_username_empty_fail():
        hashPwd = hashlib.md5("123").hexdigest()
        dataload = json.dumps({"un": "", "pw": hashPwd})
        response = requests.post("/register", dataload)
        self.assertEqual(response.r, 3)
        
    def test_password_empty_fail():
        hashPwd = hashlib.md5("").hexdigest()
        dataload = json.dumps({"un": "123", "pw": hashPwd})
        response = requests.post("/register", dataload)
        self.assertEqual(response.r, 3)
        
    def test_input_valid_success():
        hashPwd = hashlib.md5("abcd").hexdigest()
        dataload = json.dumps({"un": "qwer", "pw": hashPwd})
        response = requests.post("/register", dataload)
        self.assertNotEqual(response.r, 3)

    def test_already_register_fail():
        hashPwd = hashlib.md5("12345").hexdigest()
        dataload = json.dumps({"un": "kriyazhao", "pw": hashPwd})
        response = requests.post("/register", dataload)
        self.assertNotEqual(response.r, 0)
        
    def test_new_register_success():
        hashPwd = hashlib.md5("yygjk").hexdigest()
        dataload = json.dumps({"un": "kriya", "pw": hashPwd})
        response = requests.post("/register", dataload)
        session.logged_in == False
        session.kill()
        self.assertEqual(response.r, 1)
        
    def test_already_login_fail():
        session.logged_in = True
        session.username = "kriyazhao"
        hashPwd = hashlib.md5("yygjk").hexdigest()
        dataload = json.dumps({"un": "kriya", "pw": hashPwd})
        response = requests.post("/register", dataload)
        session.logged_in == False
        session.kill()
        self.assertEqual(response.r, 2)

if __name__ == "__main__":
    unitest.main()
