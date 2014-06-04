#==========================================================================================================================
# import python modules
import web, os
import json

import CheckSession, EncryptionPath, FileNotepad, FileValidator, FileModel

#==========================================================================================================================
# ViewFile class for handing get request from the client-side
class ViewFile:

    self.sess = CheckSession()
    self.readfile = FileNotepad()
    self.filevalidator = FileValidator()
    self.modelfile = FileModel()
    self.encrypt = EncryptionPath()

    def GET(self):
        web.header('Content-Type','text/plain')
        if self.sess.getSession() == True:
            filename = web.input()
            self.modelfile.setUsername(self.sess.getUsername())
            self.modelfile.setFileName(filename)
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
                    self.readfile.setFilepath(completePath)
                    fileContent = self.readfile.readFile()
                    return fileContent
        else:
            return "notlogin" 