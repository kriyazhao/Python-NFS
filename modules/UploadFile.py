#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json
import datetime
import EncryptionPath

#==========================================================================================================================
# Upload class for handing uploading request from the client-side
class UploadFile:

    def POST(self):
        global myConfig, fileCount, session, db
        datafile = web.input()
        logging.info(datafile)
        filedir = 'temp/'
        fileName = datafile.Filename
        with open(filedir + fileName, 'w+') as content:
            content.write(datafile.Filedata)

        web.header('Content-Type','text/plain')
        if session.logged_in == True:	
            # get the fileContent data from the client-side
            tempfile = 'temp//'+fileName
            logging.info(tempfile)
            with open(tempfile, 'rb') as myfile:
                fileContent = myfile.read()
            if len(fileContent) > myConfig.getMaxSize():
                # The fileContent is wrong.  Return a 400 bad request error. Log info about the remote in the future.
                logging.warning("fileContent size exceeds the limit!")
                return "exceed"
            # build the hashed path and write the file
            results = db.query("SELECT ID FROM user WHERE username=$username",
                               vars={'username':session.username})
            userid = list(results)[0].ID
            hashMD5 = str(hashlib.md5(fileContent + fileName).hexdigest()) + str(userid)
            hashSHA1 = hashlib.sha1(fileContent).hexdigest()
            completePath = EncryptionPath().writePath(hashMD5, hashSHA1, "put")
            # create the path if not detected
            if not os.path.exists(completePath):
                os.makedirs(completePath)
            completePath += "{0}.obj".format(hashSHA1)
            # write the file if not detected
            if not os.path.isfile(completePath):
                logging.info("Adding a new fileContent at: {0}".format(completePath))
                with open(completePath, 'wb') as data:
                    data.write(fileContent)
                db.insert("file", userID=userid, filename=fileName, md5code=hashMD5, sha1code=hashSHA1, 
                          createon= str(datetime.datetime.now()), updateon= str(datetime.datetime.now()))
            else:
                return "exist"
            # read the file again and verify it is hashed correctly
            verifyResult = EncryptionPath().verifyfileContent(completePath, hashMD5, hashSHA1)
            if verifyResult == True:
                os.remove(tempfile)
                return "success"
            else:
                return web.notfound()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return web.internalerror()
        else:
            return "please login first!"
