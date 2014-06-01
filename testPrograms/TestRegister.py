import unittest
import requests
import json
import Register

class TestRegister(unittest.TestCase):
    global session
    
    def test_username_empty_fail(self):
        response = self.prepare_dataload_and_send_request("","123")
        self.assertEqual(response.r, 3)
        
    def test_password_empty_fail(self):
        response = self.prepare_dataload_and_send_request("123","")
        self.assertEqual(response.r, 3)
        
    def test_input_valid_success(self):
        response = self.prepare_dataload_and_send_request("qwer","abcd")
        self.assertNotEqual(response.r, 3)

    def test_already_register_fail(self):
        response = self.prepare_dataload_and_send_request("kriyazhao","12345")
        self.assertNotEqual(response.r, 0)
        
    def test_new_register_success(self):
        response = self.prepare_dataload_and_send_request("kriya","yygjk")
        session.logged_in == False
        session.kill()
        self.assertEqual(response.r, 1)
        
    def test_new_register_success_return_username(self):
        response = self.prepare_dataload_and_send_request("kriya","yygjk")
        session.logged_in == False
        session.kill()
        self.assertEqual(response.username, "kriya")    
    
    def test_already_login_fail(self):
        session.logged_in = True
        session.username = "kriyazhao"
        response = self.prepare_dataload_and_send_request("kriya","yygjk")
        session.logged_in == False
        session.kill()
        self.assertEqual(response.r, 2)

    def test_already_login_fail_return_username(self):
        session.logged_in = True
        session.username = "kriyazhao"
        response = self.prepare_dataload_and_send_request("kriya","yygjk")
        session.logged_in == False
        session.kill()
        self.assertEqual(response.username, "kriyazhao")

    def prepare_dataload_and_send_request(self,un,pw):
        hashPwd = hashlib.md5(pw).hexdigest()
        dataload = json.dumps({"un": un, "pw": hashPwd})
        return requests.post("/register", dataload)
    
if __name__ == "__main__":
    unitest.main()
