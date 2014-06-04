#==========================================================================================================================
# import python modules
import web
import json

import CheckSession, FileValidator, FileModel

#==========================================================================================================================
# ShareFile class for providing md5 and sha1 to the client
class ShareFile:

    self.sess = CheckSession()
    self.modelfile = FileModel()
    self.filevalidator = FileValidator()

    def POST(self):
        web.header('Content-Type','application/json')
        if self.sess.getSession() == True:
            requestCon = json.loads(web.data())
            self.filevalidator.setfileName(requestCon.filename)
            if self.filevalidator.verifyfileName() == True:
                self.modelfile.setUsername(self.sess.getUsername())
                self.modelfile.setFileName(requestCon.filename)
                results = self.modelfile.queryHashCode()
                rows = list(results)
                if len(rows) > 0:
                    return json.dumps({'md5':rows[0].md5code,'sha1':rows[0].sha1code})
                else:
                    return json.dump('notfound')
            else:
                return json.dump('notvalid'')
        else:
            return json.dump('notlogin'')