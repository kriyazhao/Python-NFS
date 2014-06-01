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
# Data class for adding, viewing, editing and deleting files
class Data:
    global myConfig, fileCount, session, db

    # GET function responds to get method from the client-side
    def GET(self):
        web.header('Content-Type','text/plain')
        if session.logged_in == True:
            filename = web.input()
            logging.info(filename)
            logging.info(session.username)
            results = db.query("SELECT md5code,sha1code FROM file WHERE filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'username':session.username, 'filename':filename['filename']})
            rows = list(results)
            hashMD5, hashSHA1 = 0,0
            if len(rows) > 0:
                hashMD5, hashSHA1 = rows[0]['md5code'],rows[0]['sha1code']
            # build the hashed path and read the file
            completePath = EncryptionPath().writePath(hashMD5, hashSHA1)
            logging.info(completePath)
            # raise error if no such file is found
            verifyResult = EncryptionPath().verifyfileContent(completePath, hashMD5, hashSHA1)
            logging.info("{0},{1}".format(hashMD5, hashSHA1))
            if verifyResult == True:
                with open(completePath, 'rb') as data:
                    fileContent = data.read()
                return fileContent
    	    else:
                return self.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return self.ServerError()
        else:
            return "please login first!" 

    # DELETE function responds to delete method from the client-side
    def DELETE(self):
        web.header('Content-Type','text/plain')
        if session.logged_in == True:	
            requestCon = web.data()
            requestContent = json.loads(requestCon)
            results = db.query("SELECT md5code,sha1code FROM file WHERE filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'username':session.username, 'filename':requestContent['filename']})
            rows = list(results)
            hashMD5, hashSHA1 = 0, 0
            if len(rows) > 0:
                hashMD5, hashSHA1 = rows[0]['md5code'], rows[0]['sha1code']
            # build the hashed path 
            completePath = EncryptionPath().writePath(hashMD5, hashSHA1)
            vertifyResult = EncryptionPath().verifyfileContent(completePath, hashMD5, hashSHA1)
            if vertifyResult == True:
                dirpath = EncryptionPath().writePath(hashMD5, hashSHA1, "delete")
                db.delete('file', where="filename=$filename AND md5code=$hashMD5 AND sha1code=$hashSHA1 AND userID=(SELECT ID FROM user WHERE username=$username)",
                          vars={'filename':requestContent['filename'],'hashMD5':hashMD5,'hashSHA1':hashSHA1,'username':session.username})
                shutil.rmtree(dirpath)
                return "success"
            else:
                return self.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return self.ServerError()
        else:
            return "please login first!"

    # POST function responds to post method from the client-side
    def POST(self):
        web.header('Content-Type','text/plain')
        if session.logged_in == True:
            requestCon = web.data()
            requestContent = json.loads(requestCon)
            results = db.query("SELECT userID,md5code,sha1code FROM file WHERE filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)",
                               vars={'username':session.username, 'filename':requestContent['filename']})
            rows = list(results)
            logging.info(rows)
            hashMD5, hashSHA1 = 0,0
            if len(rows) > 0:
                hashMD5, hashSHA1 = rows[0]['md5code'], rows[0]['sha1code']
            # build the hashed path
            completePath = EncryptionPath().writePath(hashMD5, hashSHA1)
            # verify fileContent 
            vertifyResult = EncryptionPath().verifyfileContent(completePath, hashMD5, hashSHA1)
            if vertifyResult == True:
                newcontent = str(requestContent['content']) + str(requestContent['filename'])
                newMD5 = str(hashlib.md5(newcontent).hexdigest()) + str(rows[0]['userID'])
                newSHA1 = hashlib.sha1(requestContent['content']).hexdigest()
                logging.info("newMD5: {0}".format(newMD5))
                logging.info("newSHA1: {0}".format(newSHA1))
                # rewrite hash path and filename for the updated file 
                newPath = EncryptionPath().writePath(newMD5, newSHA1, "put")
                if not os.path.exists(newPath):
                    os.makedirs(newPath)
                newPath += "{0}.obj".format(newSHA1)
                if not os.path.isfile(newPath):
                    logging.info("Adding a new fileContent at: {0}".format(newPath))
                    with open(newPath, 'wb') as result:
                        result.write(requestContent['content'])
                    db.update("file", where="filename=$filename AND userID=(SELECT ID FROM user WHERE username=$username)", 
                              md5code=newMD5, sha1code=newSHA1, updateon=str(datetime.datetime.now()), 
                              vars={'username':session.username, 'filename':requestContent['filename']})
                    logging.info("Successfully update the file!")
                else:
                    return "exist"
                # delete the original path and file
                dirpath = EncryptionPath().writePath(hashMD5, hashSHA1, "delete")
                shutil.rmtree(dirpath)
                logging.info("Deleting the old fileContent at: {0}".format(completePath))
                return "success"
            else:
                return self.NotFoundError()
            # return an error if the provided codes doesn't match that of the fileContent
            logging.error("Something is weird about the provided: {0}".format(completePath))
            return self.ServerError()
        else:
            return "please login first!"

    # NotFoundError function handles errors of no files found 
    def NotFoundError(self):
        return web.notfound("404 Not Found")

    # ServerError function handles errors from the server side 
    def ServerError(self):
        return web.internalerror("500 Internal Server Error")
