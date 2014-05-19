#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

#==========================================================================================================================
# index class for redirecting the get request to info class
class index:
    def GET(self):
        raise web.seeother('/info')
