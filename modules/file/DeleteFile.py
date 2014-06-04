#==========================================================================================================================
# import python modules
import web, os
import json

import CheckSession, EncryptionPath, FileNotepad, FileValidator, FileModel

#==========================================================================================================================
# DeleteFile class for handing delete request from the client-side
class DeleteFile:

    self.sess = CheckSession()
    self.modelfile = FileModel()
    self.filevalidator = FileValidator()
    self.encrypt = EncryptionPath()

    def DELETE(self):
        web.header('Content-Type','text/plain')
        if self.sess.getSession() == True:	
            requestCon = json.loads(web.data())
            self.modelfile.setUsername(self.sess.getUsername())
            self.modelfile.setFileName(requestCon.filename)
            results = self.modelfile.queryHashCode()
            rows = list(results)
            if len(rows) == 0:
                return "notfound"
            else:
                self.encrypt.setHashCode(rows[0].md5code, rows[0].sha1code)
                completePath = self.encrypt.writePath("get")
                self.filevalidator.setfilePath(completePath)
                if self.filevalidator.verifyfileContent(rows[0].sha1code) == False:
                    logging.error("Something is weird about the provided: {0}".format(completePath))
                    return "internalerror"
                else:
                    self.modelfile.setHashCode(rows[0].md5code, rows[0].sha1code)
                    self.modelfile.deleteFile()
                    dirpath = self.encrypt.writePath("delete")
                    shutil.rmtree(dirpath)
                    return "success"
            
        else:
            return "notlogin"