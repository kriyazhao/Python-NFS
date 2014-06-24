import logging
logging.basicConfig(level=logging.INFO)

import datetime
from django.db import connection
from django.db import transaction

class UserModel:

    def __init__(self, un=None, pw=None, fn=None, lw=None, em=None):
        self.un = un
        self.pw = pw


    def __enter__(self):
        self.cursor = connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()

    def setUsername(self, un):
        self.un = un

    def setFirstname(self, fn):
        self.firstn = fn

    def setLastname(self, ln):
        self.lastn = ln   

    def setPassword(self, pw):
        self.pw = pw

    def setEmail(self, em):
        self.em = em
        
    def setSalt(self, st):
        self.st = st

    def queryLogin(self):
        if self.un != None and self.pw != None:
             self.cursor.execute("SELECT username FROM auth_user WHERE username=%s AND password=%s", (self.un, self.pw))
             results = self.cursor.fetchone()
             return results

    def updateLoginDate(self):
        if self.un != None and self.pw != None:
             self.cursor.execute("UPDATE auth_user SET last_login=%s WHERE username=%s AND password=%s", (str(datetime.datetime.now()), self.un, self.pw))
             transaction.commit_unless_managed()

    def queryRegister(self):
        if self.un != None:
             self.cursor.execute("SELECT * FROM auth_user WHERE username=%s", (self.un))
             result = self.cursor.fetchone()
             if result == None:
                 return None
             else:
                 regDict = {}
                 regDict["un"] = result[4]
                 regDict["fn"] = result[5]
                 regDict["ln"] = result[6]
                 regDict["em"] = result[7]
                 return regDict

    def insertRegister(self):
        if self.un != None and self.pw != None and self.firstn != None and self.lastn != None and self.em != None and self.st != None:
            self.cursor.execute("INSERT INTO auth_user (username, password, first_name, last_name, date_joined, last_login, email, salt) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                               (self.un, self.pw, self.firstn, self.lastn, str(datetime.datetime.now()), str(datetime.datetime.now()), self.em, self.st))
            transaction.commit_unless_managed()

    def updateRegister(self):
        if self.un != None and self.pw != None and self.firstn != None and self.lastn != None and self.em != None and self.st != None:
            self.cursor.execute("UPDATE auth_user SET first_name=%s, last_name=%s, password=%s, email=%s, salt=%s WHERE username=%s", (self.firstn, self.lastn, self.pw, self.em, self.un, self.st))
            transaction.commit_unless_managed()
            
             
    def queryForgetPassword(self):
        if self.un != None and self.em != None:
            self.cursor.execute("SELECT * FROM auth_user WHERE username=%s AND email=%s", (self.un, self.em))
            return self.cursor.fetchone()
            
    def updateValidate(self, validate):
        if self.un != None and self.em != None:
            self.cursor.execute("UPDATE auth_user SET validate=%s WHERE username=%s AND email=%s", (validate, self.un, self.em))
            transaction.commit_unless_managed()

    def querySalt(self):
        if self.un != None:
            self.cursor.execute("SELECT * FROM auth_user WHERE username=%s", (self.un))
            return self.cursor.fetchone()
            
    def updateSalt(self, salt):
        if self.un != None:
            self.cursor.execute("UPDATE auth_user SET salt=%s WHERE username=%s", (salt, self.un))
            transaction.commit_unless_managed()
            
    def resetPassword(self, password):
        if self.un != None:
            self.cursor.execute("UPDATE auth_user SET password=%s WHERE username=%s", (password, self.un))
            transaction.commit_unless_managed()