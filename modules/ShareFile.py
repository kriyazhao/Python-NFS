#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# ShareFile class for providing md5 and sha1 to the client
class ShareFile:
    global session, db
    def POST(self):
        web.header('Content-Type','application/json')
        if session.logged_in == True:
            requestCon = json.loads(web.data())
            filename = requestCon['filename']
            results = db.query("SELECT md5code, sha1code FROM file WHERE filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'filename':filename, 'username':session.username})
            rows = list(results)
            if len(rows) > 0:
                return json.dumps({'md5':rows[0]['md5code'],'sha1':rows[0]['sha1code']})
            else:
                return json.dump('notfound')
