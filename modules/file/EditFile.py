#==========================================================================================================================
# import python modules
import web, os
import json
import shutil

import CheckSession, EncryptionPath, FileNotepad, FileValidator, FileModel

#==========================================================================================================================
# EditFile class for handing post request from the client-side
class EditFile:

    self.sess = CheckSession()
    self.readfile = FileNotepad()
    self.filevalidator = FileValidator()
    self.modelfile = FileModel()
    self.encrypt = EncryptionPath()

    def POST(self):
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
                dirpath = self.encrypt.writePath("delete")
                self.filevalidator.setfilePath(completePath)
                if self.filevalidator.verifyfileContent(rows[0].sha1code) == False:
                    logging.error("Something is weird about the provided: {0}".format(completePath))
                    return web.internalerror()
                else:
                    newMD5 = self.encrypt.creatMD5(requestCon.filename, requestCon.content, rows[0].userID)
                    newSHA1 = self.encrypt.creatSHA1(requestCon.content)
                    logging.info("newMD5: {0}".format(newMD5))
                    logging.info("newSHA1: {0}".format(newSHA1))
                    newPath = self.encrypt.writePath("get")
                    self.filevalidator.setfilePath(newPath)
                    if self.filevalidator.verifyfilePath() == False:
                        # write the file if not detected
                        logging.info("Adding a new fileContent at: {0}".format(newPath))
                        self.writenewfile.setFilepath(newPath)
                        self.writenewfile.writeNewFile(requestCon.content)
                        self.modelfile.setHashCode(newMD5, newSHA1)
                        self.modelfile.updateFile()
                        # read the file again and verify it is hashed correctly
                        if self.filevalidator.verifyfileContent(newSHA1) == True:
                            shutil.rmtree(dirpath)
                            logging.info("Deleting the old fileContent at: {0}".format(completePath))
                            return "success"
                        else:
                            logging.error("Something is weird about the provided: {0}".format(newPath))
                            return "internalerror"
                    else:
                        return "exist"
        else:
            return "notlogin"