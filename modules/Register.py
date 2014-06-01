#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# Login class handles post request of register
class Register:
    global session, db

    def POST(self):
        web.header('Content-Type','application/json')
        requestContent = json.loads(web.data())
        logging.info('username: ' + requestContent['un'])
        logging.info('hashpw: ' + requestContent['pw'])
        if requestContent['un'] == "" or requestContent['pw'] == "d41d8cd98f00b204e9800998ecf8427e":
            if session.logged_in == False:
                results = db.query("SELECT * FROM user WHERE username=$username", 
                          vars={'username':requestContent['un']})
                rows = list(results)
                if len(rows) == 0:
                    db.insert("user", username=requestContent['un'], badge=requestContent['pw'], createon= str(datetime.datetime.now()))
                    session.logged_in = True
                    session.username = requestContent['un']
                    return json.dumps({'r':1,'un':session.username})
                else:
                    return json.dumps({'r':0})
            else:
                return json.dumps({'r':2,'un':session.username})
        else:
            return json.dumps({'r':3})
