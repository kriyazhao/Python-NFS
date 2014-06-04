import datetime

class FileModel:
    global db

    def __init__(self, un=None, ui=None, fn=None, md5=None, sha1=None):
        self.un = un
        self.ui = ui
        self.fn = fn
        self.md5 = md5
        self.sha1 = sha1
    
    def setUsername(self, un):
        self.un = un
    
    def setUserID(self, ui)
        self.ui = ui
    
    def setFileName(self, fn):
        self.fn = fn
    
    def setHashCode(self, md5, sha1):
        self.md5 = md5
        self.sha1 = sha1
    
    def queryList(self):
        if self.un != None:
             results = db.query("SELECT filename,createon,updateon FROM file WHERE userID=(SELECT ID FROM user WHERE username=$username)",
                                vars={'username':self.un})
             return results
    
    def queryUserID(self):
        if self.un != None:
            results = db.query("SELECT ID FROM user WHERE username=$username",
                               vars={'username':self.un})
            return results
    
    def insertFile(self):
        if self.ui != None and self.fn != None and self.md5 != None and self.sha1 != None:
            db.insert("file", filename=self.fn, md5code=self.md5, sha1code=self.sha1, userID=self.ui, 
                      createon= str(datetime.datetime.now()), updateon= str(datetime.datetime.now()))

    def queryHashCode(self):
        if self.un != None and self.fn != None:
            results = db.query("SELECT userID, md5code, sha1code FROM file WHERE filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'filename':self.fn, 'username':self.un})
            return results

    def queryFile(self):
        if self.md5 != None and self.sha1 != None:
            results = db.query("SELECT filename, createon, updateon FROM file WHERE md5code=$MD5 AND sha1code=$SHA1",
                               vars={'MD5':self.md5, 'SHA1':self.sha1})
            return results

    def deleteFile(self):
        if self.un != None and self.fn != None and self.md5 != None and self.sha1 != None:
            db.delete('file', where="filename=$filename AND md5code=$hashMD5 AND sha1code=$hashSHA1 AND userID=(SELECT ID FROM user WHERE username=$username)",
                      vars={'filename':self.fn,'hashMD5':self.md5,'hashSHA1':self.sha1,'username':self.un})

    def updateFile(self):
        if self.un != None and self.fn != None and self.md5 != None and self.sha1 != None:
            db.update("file", where="filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)", 
                              md5code=self.md5, sha1code=self.sha1, updateon=str(datetime.datetime.now()), 
                              vars={'username':self.un, 'filename':self.fn})