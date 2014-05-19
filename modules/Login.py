#==========================================================================================================================
# Login class handles post request of login
class Login:
    global session
    def POST(self):
        requestContent = json.loads(web.data())
        if requestContent["username"] == "root" and requestContent["password"] == "202cb962ac59075b964b07152d234b70":
            session.logged_in = True
            return "login successfully!"
        else:
            return "login failed!"


