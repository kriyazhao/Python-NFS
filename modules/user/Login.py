#==========================================================================================================================
# import python modules
import logging
import web, os
import json
import datetime

import CheckSession, UserValidator, EncryptionPassword, UserModel

#==========================================================================================================================
# Login class handles post request of login
class Login:

    self.sess = CheckSession() // check session
    self.validator = UserValidator() // validate input
    self.encryptpw = EncryptionPassword() // encrypt password
    self.modeluser = UserModel() // user model

    def POST(self):
        if self.sess.getSession == False:
            web.header('Content-Type','application/json')
            regInfo = json.loads(web.data())
            self.validator.setUsername(regInfo.un)
            self.validator.setPassword(regInfo.pw)
            self.encryptpw = setPassword(regInfo.pw)
            if self.validator.usernameValidate() == True and self.validator.passwordValidate() == True:
                hashPW = self.encryptpw.encryptPw()
                self.modeluser.setUsername(regInfo.un)
                self.modeluser.setPassword(hashPW)
                results = self.modeluser.queryLogin()
                rows = list(results)
                if len(rows) > 0:
                    self.sess.setSession(True)
                    self.sess.setUsername(regInfo.un)
                    return json.dumps({'r':1,'un':session.username}) // successfully login
                else:
                    return json.dumps({'r':0}) // incorrect username/password
            else:
                return json.dumps({'r':3})// username/password not validated
        else:
            return json.dumps({'r':2,'un':session.username}) // already login