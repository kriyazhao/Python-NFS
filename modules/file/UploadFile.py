#==========================================================================================================================
# import python modules
import web, os
import json

import CheckSession, EncryptionPath, FileNotepad, FileValidator, FileModel

#==========================================================================================================================
# Upload class for handing uploading request from the client-side
class UploadFile:
    global myConfig, fileCount
    
    self.sess = CheckSession()
    self.writenewfile = FileNotepad()
    self.filevalidator = FileValidator()
    self.modelfile = FileModel()
    self.encrypt = EncryptionPath()

    def POST(self):
        datafile = web.input()
        logging.info(datafile)
        tempFile = 'temp/' + datafile.Filename
        if self.filevalidator.verifyfileSize(datafile.Filedata) == False:
            return "exceed"
        else:
            self.filevalidator.setfilePath(tempFile)
            if self.filevalidator.verifyfileName() == False:
                return "notvalid"
            else:
                self.writenewfile.setFilepath(tempFile)
                self.writenewfile.writeNewFile(datafile.Filedata)
                web.header('Content-Type','text/plain')
                if self.sess.getSession() == True:	
                    self.modelfile.setUsername(self.sess.getUsername())
                    results = self.modelfile.queryUserID()
                    userid = list(results)[0].ID
                    hashMD5 = self.encrypt.creatMD5(datafile.Filename, datafile.Filedata, userid)
                    hashSHA1 = self.encrypt.creatSHA1(datafile.Filedata)
                    completePath = self.encrypt.writePath("get")
                    self.filevalidator.setfilePath(completePath)
                    if self.filevalidator.verifyfilePath() == False:
                        # write the file if not detected
                        logging.info("Adding a new fileContent at: {0}".format(completePath))
                        self.writenewfile.setFilepath(completePath)
                        self.writenewfile.writeNewFile(datafile.Filedata)
                        self.modelfile.setUserID(userid)
                        self.modelfile.setFileName(datafile.Filename)
                        self.modelfile.setHashCode(hashMD5, hashSHA1)
                        self.modelfile.insertFile()
                        # read the file again and verify it is hashed correctly
                        if self.filevalidator.verifyfileContent(hashSHA1) == True:
                            os.remove(tempFile)
                            return "success"
                        else:
                            logging.error("Something is weird about the provided: {0}".format(completePath))
                            return "internalerror"
                    else:
                        return "exist"
                else:
                    return "notlogin"