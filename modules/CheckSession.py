
#==========================================================================================================================
# CheckSession class handles session
class CheckSession:
    global session
    
    getSession(self):
        return session.logged_in

    setSession(self, bool):
        session.logged_in = bool

    killSession(self):
        session.kill()

    getUsername(self):
        return session.username

    setUsername(self,name):
        session.username = name
    
