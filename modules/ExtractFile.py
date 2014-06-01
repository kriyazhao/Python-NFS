#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime

#==========================================================================================================================
# ExtractFile class for extracting files given md5 and sha1 codes
class ExtractFile:
    global myConfig, fileCount, session, db

    def POST(self):
        web.header('Content-Type','application/json')
        requestContent = json.loads(web.data())
        results = db.query("SELECT filename, createon, updateon FROM file WHERE md5code=$MD5 AND sha1code=$SHA1",
                           vars={'MD5':requestContent['md5'], 'SHA1':requestContent['sha1']})
        rows = list(results)
        if len(rows) > 0:
            rows[0]['createon'] = str(rows[0]['createon'])
            rows[0]['updateon'] = str(rows[0]['updateon'])
            logging.info(rows[0])
            return json.dumps(rows[0])
        else:
            return json.dumps([''])
			
