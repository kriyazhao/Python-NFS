#!/usr/bin/python
#
# -------------------------------------------------------------------------------------------------
# DFS_daemon.py
# Created on: 2014-03-08 22:30:50.00000
# Updated on: 2014-05-28 21:19:34.00000
# Author: Ting Zhao (t.zhao2011@gmail.com)
# Description: A daemon program for a simple Distributed File System. 
#              This is for handling requests (put, get, post and delete) from client to server
# -------------------------------------------------------------------------------------------------

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
