# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

#==========================================================================================================================
# Logout class handles get request of logout
class Logout:
    global session
    def GET(self):
        session.logged_in = False
        session.kill()
        return "logout successfully!"
