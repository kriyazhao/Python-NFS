import datetime
from django.db import connection
from django.db import transaction

class FileActivityLog:

    def __init__(self, userID=None, fileID=None, curName=None, ownerID=None, sharedwithID=None, sharedPrvlg=None, action=None):
        self.userID = userID
        self.fileID = fileID
        self.curName = curName
        self.sharedwithID = sharedwithID
        self.sharedPrvlg = sharedPrvlg

    def __enter__(self):
        self.cursor = connection.cursor()
        return self
 
    def __exit__(self, type, value, traceback):
        self.cursor.close()
        
    def setUserID(self, userID):
        self.userID = userID
        
    def setFileID(self, fileID):
        self.fileID = fileID
        
    def setCurName(self, curName):
        self.curName = curName        
        
    def setOwnerID(self, ownerID):
        self.ownerID = ownerID
        
    def setSharedwithID(self, sharedwithID):
        self.sharedwithID = sharedwithID

    def setSharedPrvlg(self, sharedPrvlg):
        self.sharedPrvlg = sharedPrvlg              

    def insertUpload(self):
        if self.userID != None and self.fileID != None and self.curName != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='upload'", (self.userID, self.fileID, self.curName, self.userID))
            transaction.commit_unless_managed()

    def insertCreate(self):
        if self.userID != None and self.fileID != None and self.curName != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='create'", (self.userID, self.fileID, self.curName, self.userID))
            transaction.commit_unless_managed()
            
    def insertEdit(self):
        if self.userID != None and self.fileID != None and self.curName != None and self.ownerID != None:
            self.cursor.execute("SELECT actionDate FROM activity_log WHERE userID=%s AND fileID=%s AND curName=%s AND ownerID=%s AND action='edit' ORDER BY actionDate DESC", (self.userID, self.fileID, self.curName, self.ownerID))
            rows = self.cursor.fetchone()
            if rows ==None:
                self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='edit'", (self.userID, self.fileID, self.curName, self.ownerID))
            else:
                timeDiff = datetime.timedelta(hours=2)
                if timeDiff > (datetime.datetime.now() - rows[0]):
                    self.cursor.execute("UPDATE activity_log SET actionDate=now() WHERE userID=%s AND fileID=%s AND curName=%s AND ownerID=%s AND action='edit' ORDER BY actionDate DESC LIMIT 1", (self.userID, self.fileID, self.curName, self.ownerID))
                else:    
                    self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='edit'", (self.userID, self.fileID, self.curName, self.ownerID))
            transaction.commit_unless_managed()
            
    def insertDelete(self):
        if self.userID != None and self.fileID != None and self.curName != None and self.ownerID != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='delete'", (self.userID, self.fileID, self.curName, self.ownerID))
            transaction.commit_unless_managed()
            
    def insertRename(self):
        if self.userID != None and self.fileID != None and self.curName != None and self.ownerID != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='rename'", (self.userID, self.fileID, self.curName, self.ownerID))
            transaction.commit_unless_managed() 

    def insertExtract(self):
        if self.userID != None and self.fileID != None and self.curName != None and self.ownerID != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, curName=%s, ownerID=%s, action='extract'", (self.userID, self.fileID, self.curName, self.ownerID))
            transaction.commit_unless_managed() 
   
    def insertShare(self):
        if self.userID != None and self.fileID != None and self.ownerID != None and self.curName != None and self.sharedwithID != None and self.sharedPrvlg != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, ownerID=%s, curName=%s, sharedwithID=%s, privilege=%s, action='share'", (self.userID, self.fileID, self.ownerID, self.curName, self.sharedwithID, self.sharedPrvlg))
            transaction.commit_unless_managed()   

    def insertDeletedShare(self):
        if self.userID != None and self.fileID != None  and self.ownerID != None and self.curName != None and self.sharedwithID != None and self.sharedPrvlg != None:
            self.cursor.execute("INSERT INTO activity_log SET userID=%s, fileID=%s, ownerID=%s, curName=%s, sharedwithID=%s, privilege=%s, action='de-share'", (self.userID, self.fileID, self.ownerID, self.curName, self.sharedwithID, self.sharedPrvlg))
            transaction.commit_unless_managed()   

    def queryLog(self, type):
        if self.userID != None:
            if type == 1:
                self.cursor.execute("SELECT * FROM activity_log WHERE userID=%s OR sharedwithID=%s OR ownerID=%s GROUP BY ID ORDER BY actionDate DESC LIMIT 3",(self.userID, self.userID, self.userID))
            elif type == 2:
                self.cursor.execute("SELECT * FROM activity_log WHERE userID=%s OR sharedwithID=%s OR ownerID=%s GROUP BY ID ORDER BY actionDate DESC",(self.userID, self.userID, self.userID))
            results = self.cursor.fetchall()
            return results