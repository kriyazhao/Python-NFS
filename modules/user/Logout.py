import CheckSession, UserValidator, EncryptionPassword, UserModel

#==========================================================================================================================
# Logout class handles get request of logout
class Logout:

    self.sess = CheckSession() // check session

    def GET(self):
        web.header('Content-Type','application/json')
        if self.sess.getSession() == True:
            self.sess.setSession(False)
            self.sess.killSession()
            return json.dumps({'r':'1'}) // successfully logout
        else:
            return json.dumps({'r':'0'}) // already logout
            