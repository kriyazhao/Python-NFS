#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# CheckLogin class checks if already logged in
class CheckLogin:
    global session
    def GET(self):
        web.header('Content-Type','application/json')
        if session.logged_in == False:
            return json.dumps({'r':0})
        else:
            return json.dumps({'r':1,'un':session.username})
