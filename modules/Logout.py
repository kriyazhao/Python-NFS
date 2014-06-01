#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# Logout class handles get request of logout
class Logout:
    global session

    def GET(self):
        web.header('Content-Type','application/json')
        if session.logged_in == True:
            session.logged_in = False
            session.kill()
            return json.dumps({'r':'logout'})
