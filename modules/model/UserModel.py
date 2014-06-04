import datetime

class UserModel:
    global db

    def __init__(self, un=None, pw=None):
        self.un = un
        self.pw = pw
    
    def setUsername(self, un):
        self.un = un
        
    def setPassword(self, pw):
        self.pw = pw
    
    def queryLogin(self):
        if self.un != None and self.pw != None:
             results = db.query("SELECT * FROM user WHERE username=$username AND badge=$password", 
                                vars={'username':self.un,'password':self.pw})
             return results

    def queryRegister(self):
        if self.un != None:
             results = db.query("SELECT * FROM user WHERE username=$username", 
                                vars={'username':self.un})
             return results

    def insertRegister(self):
        if self.un != None and self.pw != None:
            db.insert("user", username=self.un, badge=self.pw, createon= str(datetime.datetime.now()))
