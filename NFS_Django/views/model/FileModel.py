import datetime
from django.db import connection
from django.db import transaction
import logging
logging.basicConfig(level=logging.INFO)

class FileModel:

    def __init__(self, un=None, ui=None, fi=None, fn=None, md5=None, sha1=None):
        self.un = un
        self.ui = ui
        self.fi = fi
        self.fn = fn
        self.md5 = md5
        self.sha1 = sha1

    def __enter__(self):
        self.cursor = connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()

    def setUsername(self, un):
        self.un = str(un)
    
    def setUserID(self, ui):
        self.ui = str(ui)

    def setFileID(self, fi):
        self.fi = str(fi)
    
    def setFileName(self, fn):
        self.fn = str(fn)
    
    def setHashCode(self, md5, sha1):
        self.md5 = str(md5)
        self.sha1 = str(sha1)
    
    def queryList(self):
        if self.un != None:
             self.cursor.execute("SELECT filename,createon,updateon FROM file WHERE userID=(SELECT ID FROM auth_user WHERE username=%s)", (self.un))
             results =  self.cursor.fetchall()
             if results == None:
                 return results
             else:
                 resultslist=[]
                 for row in results:
                     recordDict = {}
                     recordDict["filename"] = row[0]
                     recordDict["createon"] = str(row[1])[:19]
                     recordDict["updateon"] = str(row[2])
                     resultslist.append(recordDict)
                 return resultslist

    def queryUsername(self):
        if self.ui != None:
            self.cursor.execute("SELECT username FROM auth_user WHERE id=%s", (self.ui))
            return self.cursor.fetchone()

    def queryUserID(self):
        if self.un != None:
            self.cursor.execute("SELECT id FROM auth_user WHERE username=%s", (self.un))
            return self.cursor.fetchone()
    
    def insertFile(self):
        if self.ui != None and self.fn != None and self.md5 != None and self.sha1 != None:
            self.cursor.execute("INSERT INTO file (userID, filename, md5code, sha1code, createon, updateon) VALUES(%s, %s, %s, %s, %s, %s)", 
                                     (self.ui, self.fn, self.md5, self.sha1, str(datetime.datetime.now()), str(datetime.datetime.now())))
            transaction.commit_unless_managed()

    def queryHashCode(self):
        if self.un != None and self.fn != None:
            self.cursor.execute("SELECT userID, md5code, sha1code, ID, privilege FROM file WHERE filename=%s AND userID=(SELECT ID FROM auth_user WHERE username=%s)", (self.fn, self.un))
            return self.cursor.fetchone()

    def queryAllHash(self):
        results = db.query("SELECT md5code, sha1code FROM file")
        return results

    def queryFile_fileID(self):
        if self.fi != None:
            self.cursor.execute("SELECT filename, md5code, sha1code, userID FROM file WHERE ID=%s", (self.fi))
            return self.cursor.fetchone()

    def queryFile(self):
        if self.md5 != None and self.sha1 != None:
            self.cursor.execute("SELECT filename, createon, updateon, privilege, userID, ID FROM file WHERE md5code=%s AND sha1code=%s", (self.md5, self.sha1))
            row = self.cursor.fetchone()
            recordDict = {}
            recordDict["filename"] = row[0]
            recordDict["createon"] = str(row[1])[:19]
            recordDict["updateon"] = str(row[2])
            recordDict["privilege"] = str(row[3])
            recordDict["userID"] = str(row[4])
            recordDict["ID"] = str(row[5])
            return recordDict

    def deleteFile(self):
        if self.un != None and self.fn != None and self.md5 != None and self.sha1 != None:
            self.cursor.execute("DELETE FROM file WHERE filename=%s AND md5code=%s AND sha1code=%s AND userID=(SELECT id FROM auth_user WHERE username=%s)", 
                                    (self.fn, self.md5, self.sha1, self.un))
            transaction.commit_unless_managed()

    def updateFile(self, oldName = None):
        if self.un != None and self.fn != None and self.md5 != None and self.sha1 != None:
            if oldName == None:
                self.cursor.execute("UPDATE file INNER JOIN auth_user ON file.userID = auth_user.id SET md5code=%s, sha1code=%s, updateon=%s WHERE filename=%s", 
                                   (self.md5, self.sha1, str(datetime.datetime.now())[:19], self.fn))
            else:
                self.cursor.execute("UPDATE file INNER JOIN auth_user ON file.userID = auth_user.id SET filename=%s, md5code=%s, sha1code=%s, updateon=%s WHERE filename=%s", 
                                   (self.fn, self.md5, self.sha1, str(datetime.datetime.now())[:19], oldName))
            transaction.commit_unless_managed()

    def updateShareOption(self, privilege):
        if self.un != None and self.fn != None:
            self.cursor.execute("UPDATE file SET privilege=%s WHERE userID=(SELECT id FROM auth_user WHERE username=%s) AND filename=%s", (privilege, self.un, self.fn))
            transaction.commit_unless_managed()