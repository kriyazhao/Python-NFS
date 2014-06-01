#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# ListFile class for getting file list under logged-in user.
class ListFile:
    global session, db

    def GET(self):
        web.header('Content-Type','application/json')
        if session.logged_in == True:
            results = db.query("SELECT filename,createon,updateon FROM file WHERE userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'username':session.username})
            rows = list(results)
            if len(rows) > 0:
                for row in rows:
                    row['createon'] = str(row['createon'])
                    row['updateon'] = str(row['updateon'])
                return json.dumps(rows)
            else:
                return json.dumps(['empty'])
        else:
            return json.dumps([''])
