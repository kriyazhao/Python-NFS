#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# Login class handles post request of login
class Login:
    global session, db

    def POST(self):
        web.header('Content-Type','application/json')
        if session.logged_in == False:
            requestContent = json.loads(web.data())
            results = db.query("SELECT * FROM user WHERE username=$username AND badge=$password", 
                               vars={'username':requestContent['un'],'password':requestContent['pw']})
            rows = list(results)
            if len(rows) > 0:
                session.logged_in = True
                session.username = requestContent['un']
                return json.dumps({'r':1,'un':session.username})
            else:
                return json.dumps({'r':0})
        else:
            return json.dumps({'r':2,'un':session.username})
