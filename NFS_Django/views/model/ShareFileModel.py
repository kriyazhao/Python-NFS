import datetime
from django.db import connection
from django.db import transaction
import logging
logging.basicConfig(level=logging.INFO)

class ShareFileModel:

    def __init__(self, fileID=None, file_alias=None, owner=None, sharedwith=None, privilege=None):
        self.fileID = fileID
        self.fileAlias = file_alias
        self.owner = owner
        self.sharedwith = sharedwith
        self.privilege = privilege

    def __enter__(self):
        self.cursor = connection.cursor()
        return self
        
    def __exit__(self, type, value, traceback):
        self.cursor.close()
        
    def setFileID(self, fileID):
        self.fileID = fileID
        
    def setFileAlias(self, file_alias):
        self.fileAlias = file_alias

    def setOwner(self, owner):
        self.owner = owner
        
    def setSharedWith(self, sharedwith):
        self.sharedwith = sharedwith
        
    def setPrivilege(self, privilege):
        self.privilege = privilege

    def queryShareFile(self):
        if self.fileID != None and self.owner != None and self.sharedwith != None:
            self.cursor.execute("SELECT * FROM sharefile WHERE fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s) AND sharedwithID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileID, self.owner, self.sharedwith))
            return self.cursor.fetchone()

    def queryShareFile_fileAlias(self):
        if self.fileAlias != None and self.owner != None and self.sharedwith != None:
            self.cursor.execute("SELECT * FROM sharefile WHERE fileAlias=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s) AND sharedwithID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileAlias, self.owner, self.sharedwith))
            return self.cursor.fetchone()
    
    def querySharedList_owner(self):
        if self.owner != None and self.fileID != None:
            self.cursor.execute("SELECT auth_user.username, sharefile.privilege FROM sharefile, auth_user WHERE auth_user.id=sharefile.sharedwithID AND fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s) AND privilege IN (21, 22)", (self.fileID, self.owner))
            results =  self.cursor.fetchall()
            if results == None:
                return results
            else:
                resultslist=[]
                for row in results:
                    recordDict = {}
                    recordDict["sharedwithID"] = row[0]
                    recordDict["privilege"] = str(row[1])
                    resultslist.append(recordDict)
                return resultslist   
         
    def querySharedList(self):
        if self.sharedwith != None:
            self.cursor.execute("SELECT sharefile.fileAlias, auth_user.username, sharefile.privilege FROM sharefile, auth_user WHERE auth_user.id = sharefile.ownerID AND sharefile.sharedwithID=(SELECT id FROM auth_user WHERE username=%s) AND deletedByShared=0", (self.sharedwith))
            results =  self.cursor.fetchall()
            if results == None:
                return results
            else:
                resultslist=[]
                for row in results:
                    recordDict = {}
                    recordDict["filename"] = row[0]
                    recordDict["owner"] = row[1]
                    recordDict["privilege"] = str(row[2])
                    resultslist.append(recordDict)
                return resultslist    
    
    def insertShareFile(self):
        if self.fileID != None and self.owner != None and self.sharedwith != None and self.fileAlias != None and self.privilege != None:
            self.cursor.execute("INSERT INTO sharefile SET fileID=%s, fileAlias=%s, ownerID=(SELECT id FROM auth_user WHERE username=%s), sharedwithID=(SELECT id FROM auth_user WHERE username=%s), privilege=%s", (self.fileID, self.fileAlias, self.owner, self.sharedwith, self.privilege))
            transaction.commit_unless_managed()
            
    def updateShareFile(self):
        if self.fileID != None and self.owner != None and self.sharedwith != None and self.fileAlias != None and self.privilege != None:
            self.cursor.execute("UPDATE sharefile SET fileAlias=%s, privilege=%s, deletedByShared=0 WHERE fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s) AND sharedwithID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileAlias, self.privilege, self.fileID, self.owner, self.sharedwith))
            transaction.commit_unless_managed()

    def deleteSharedFile(self):
        if self.fileID != None and self.owner != None and self.sharedwith != None and self.fileAlias != None:
            self.cursor.execute("UPDATE sharefile SET fileAlias=%s, deletedByShared=1 WHERE fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s) AND sharedwithID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileAlias, self.fileID, self.owner, self.sharedwith))
            transaction.commit_unless_managed()

    def deleteSharedWith(self, sharelist):
        str = ""
        for i in sharelist:
            str += "'"+i+"',"
        liststr = str[:-1]
        if self.fileID != None and self.owner != None:
            self.cursor.execute("SELECT * FROM sharefile WHERE ownerID=(SELECT id FROM auth_user WHERE username=%s) AND fileID=%s AND sharedwithID NOT IN (SELECT id FROM auth_user WHERE username IN (" + liststr + "))", (self.owner, self.fileID))
            results = self.cursor.fetchall()
            resultlist = []
            for item in results:
                resultDict = {}
                resultDict["fileID"] = item[1]
                resultDict["sharedwithID"] = item[4]
                resultDict["privilege"] = item[5]
                resultlist.append(resultDict)

            self.cursor.execute("DELETE FROM sharefile WHERE ownerID=(SELECT id FROM auth_user WHERE username=%s) AND fileID=%s AND sharedwithID NOT IN (SELECT id FROM auth_user WHERE username IN (" + liststr + "))", (self.owner, self.fileID))
            transaction.commit_unless_managed()
            return resultlist

    def deleteSharedWith_owner(self):
        if self.fileID != None and self.owner != None:
            self.cursor.execute("SELECT * FROM sharefile WHERE fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileID, self.owner))
            results = self.cursor.fetchall()
            resultlist = []
            for item in results:
                resultDict = {}
                resultDict["fileID"] = item[1]
                resultDict["sharedwithID"] = item[4]
                resultDict["privilege"] = item[5]
                resultlist.append(resultDict)

            self.cursor.execute("DELETE FROM sharefile WHERE fileID=%s AND ownerID=(SELECT id FROM auth_user WHERE username=%s)", (self.fileID, self.owner))
            transaction.commit_unless_managed()
            return resultlist
