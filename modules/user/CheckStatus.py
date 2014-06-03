#==========================================================================================================================
# import python modules
import web,
import json

import CheckSession

#==========================================================================================================================
# CheckStatus class check user's login status
class CheckStatus:
	
	self.sess = CheckSession()
	
    def GET(self):
        web.header('Content-Type','application/json')
        if self.sess.getSession() == False:
            return json.dumps({'r':0})
        else:
            return json.dumps({'r':1,'un':self.sess.getUsername()})