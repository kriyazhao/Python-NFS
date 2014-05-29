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
# global variables
global myConfig
global fileCount
global session
#==========================================================================================================================
# nfsConfig class for NFS configurations, which is server-side only
class nfsConfig:
    
    # initialize the configuration class and load configuration from a specified section
    def __init__(self, conFile = None, conSection = None):
        if conFile != None:
            self.fileConfig = conFile
        else:
            self.fileConfig = 'fileConfig.conf'
        if conSection != None:
            self.sectionConfig = conSection
        else:
            self.sectionConfig = 'defaultConfig'
        self.ipaddr = '198.46.132.117'
        self.port = '8080'
        self.datadir = 'data'
        self.maxsize = '25'
        # Load the configuration from the file
        self.configParams = ConfigParser.ConfigParser()
        self.configParams.read(self.fileConfig)
        logging.info("configParams : {0}".format(self.configParams))
        try:
            logging.info("Reading from config file:")
            for key, value in self.configParams.items(self.sectionConfig):
                setattr(self, key, value)
                logging.info("{0} = {1}".format(key, value))
        except OSError as ex:
            logging.error("Failed to read the provided config file: {0}".format(ex))
            logging.error("Please check parameter names and types.")
            
    # create an IP address for the webserver to use
    def getIP(self):
        return web.net.validip("{0}:{1}".format(self.ipaddr, self.port))

    # get the specified directory and convert it to an absolute path
    def getDataDir(self):
        return os.path.abspath(self.datadir)

    # get the maximum size and convert from kb to bytes
    def getMaxSize(self):
        return int(self.maxsize) * 1024

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

#==========================================================================================================================
# Login class handles post request of login
class Login:
    global session, db

    def POST(self):
        web.header('Content-Type','application/json')
        if session.logged_in == False:
            requestContent = json.loads(web.data())
            results = db.query("SELECT * FROM user WHERE username=$username AND badge=$password", 
                               vars={'username':requestContent['un'],'password':requestContent['pw']})
            rows = list(results)
            if len(rows) > 0:
                session.logged_in = True
                session.username = requestContent['un']
                return json.dumps({'r':1,'un':session.username})
            else:
                return json.dumps({'r':0})
        else:
            return json.dumps({'r':2,'un':session.username})

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

#==========================================================================================================================
# EncryptionPath class for writing encrypted path and varify files
class EncryptionPath:
    global myConfig, fileCount, session, db

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, hashMD5, hashSHA1, writeType = "get"): # writeType in "get", "put" and "delete"
        # build the hashed path
        if not (hashMD5 == 0 or hashSHA1 == 0):
            increNum = len(hashMD5) // 2
            while not hashMD5[increNum].isdigit():
                increNum += 1
            completePath = "{0}/".format(myConfig.getDataDir())
            dirpath = "{0}/".format(myConfig.getDataDir())
            dirpath += "{0}".format(hashMD5[0:int(hashMD5[increNum])])
            for i in range(0, len(hashMD5), int(hashMD5[increNum])):
                completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
            if writeType == "put": # only return the directory of the file
                return completePath
            elif writeType == "delete": # only return the first-level directory of the file
                return dirpath
            elif writeType == "get": # return the directory + filename of the file
                completePath += "{0}.obj".format(hashSHA1)
                return completePath
            else:
                raise TypeError("write type cannot be recgnized!")
                return
        else:
            raise ValueError("hash code is empty!")

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, completePath, hashMD5, hashSHA1):
        # verify the fileContent
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return self.NotFoundError()
        else:
            with open(completePath, 'rb') as data:
                fileContent = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # to see if hash is verified
            if mySHA1 == hashSHA1:
                return True
            else:
                return False
            

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
			
#==========================================================================================================================
# index class for redirecting the get request to info class
class index:
    def GET(self):
        render = web.template.render('templates')
        return render.main()

#==========================================================================================================================
# info class for displaying server infomation.
class info:
    global myConfig, fileCount, session
    
    # GET function responds to request.get method from the client-side
    def GET(self, paramStr = None):
        
        path = myConfig.getDataDir()
        # if /info/fileValidator is called, run the fileValidator function.
        if(paramStr == 'validateFiles'):
            fileCount = fileValidator(path)
        info = {'fileCount': fileCount}
        info['free'], info['freeNonSuper'], info['total'] = self.diskSpace(path)
        try:
            info['percFreeNoneSuper'] = 100 * (float(info['freeNonSuper']) / info['total'])
        except ZeroDivisionError:
            info['percFreeNoneSuper'] = 0
        logging.info("Total: {0}\nFree: {1}\nFreeNonSuper: {2}\npercFreeNonSuper: {3}".format(info['total'], info['free'], info['freeNonSuper'], info['percFreeNoneSuper']))
        web.header('Content-Type', 'application/json')
        return json.dumps(info)

    # diskSpace function to get free space and total space information (in megabytes)
    def diskSpace(self, path):
        free = 0
        freeNonSuper = 0
        total = 0
        print "diskSpace({0}): platform = {1}".format(path, platform.system())
        # if the platform is Windows
        if platform.system() == 'Windows':
            free = ctypes.c_ulonglong(0)
            freeNonSuper = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            # "total" here is the total space available to the user, not total space on the disk.
            # the server used for testing the program is a 64-bit system
            ctypes.windll.kernel64.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path),
                                                       ctypes.pointer(freeNonSuper),
                                                       ctypes.pointer(total),
                                                       ctypes.pointer(free))
            return (free.value/1024/1024, freeNonSuper.value/1024/1024, total.value/1024/1024)
        else:
            stat = os.statvfs(path)
            free = stat.f_bfree * stat.f_frsize
            freespfreeNonSuper = stat.f_bavail * stat.f_frsize
            total = stat.f_blocks * stat.f_frsize
            return (free/1024/1024, freeNonSuper/1024/1024, total/1024/1024)
        
#==========================================================================================================================
# A function to check the status of current files in the dataDir to see if they've been changed and return the number of files
def fileValidator(path):
    global myConfig, fileCount, session, db

    fileCount = 0
    results = db.query("SELECT md5code,sha1code FROM file")
    rows = list(results)
    for row in rows:
        validateFile = True
        myMD5 = row['md5code']
        mySHA1 = row['sha1code']
        # write the path with a strategy
        increNum = len(myMD5) // 2
        while not myMD5[increNum].isdigit():
            increNum += 1
        currentPath = "{0}/".format(myConfig.getDataDir())
        for i in range(0, len(myMD5), int(myMD5[increNum])):
            currentPath += "{0}/".format(myMD5[i:i+int(myMD5[increNum])])
            # check the filepath
        if not os.path.exists(os.path.abspath(currentPath)):
            # The hashed path cannot be matched to that of the original file.
            logging.warning("The file path has been modified!!!")
            logging.info("	currentPath: {0}".format(os.path.abspath(currentPath)))
            validateFile = False
        # check the filename
        currentFile = currentPath + "{0}.obj".format(mySHA1)
        if not os.path.exists(os.path.abspath(currentFile)):
            # The hashed filename cannot be matched to that of the original file.
            logging.warning("The file name has been modified!!!")
            logging.info("	currentFile: {0}".format(currentFile))
            validateFile = False
        # increment the fileCount if no modification is detected for the files
        if validateFile == True:
            fileCount += 1
        # delete the files that have been modified by others
        else:
            db.update("file", where="md5code=$myMD5 AND sha1code=$mySHA1", abnormality=1,
                      vars={'myMD5':myMD5, 'mySHA1':mySHA1})
    return fileCount

#==========================================================================================================================
# main function of the program
def main():
    global myConfig, fileCount, session, db

    # set the current basic config to INFO mode
    logging.basicConfig(level=logging.INFO)

    # parse the command line arguments using argparse module
    parseArg = argparse.ArgumentParser(description = "This is the daemon file of the system.")
    parseArg.add_argument('--fileConfig', help = "Configuration file (e.g. ip, port, datadir)")
    parseArg.add_argument('--sectionConfig', help = "Section in the configuration file to use (e.g. 'defaultConfig' by default)")
    args = parseArg.parse_args()
    logging.info('Input arguments: \n{0}'.format(str(args)))#(fileConfig = 'fileConfig.conf', sectionConfig = 'defaultConfig')

    # pass the config params to nfsConfig function
    myConfig = nfsConfig(args.fileConfig, args.sectionConfig)

    # set up the webserver to handle requests.
    # any url matches the regular expression will be sent to the corresponding class/function for handling
    urls = ('/main', 'index',
            '/register','Register',
            '/data/([0-9,a-f,A-F]+)/([0-9,a-f,A-F]+)', 'Data',
            '/login', 'Login',
            '/checklogin','CheckLogin',
            '/logout', 'Logout',
            '/listfile', 'ListFile',
            '/uploadfile','UploadFile',
            '/manipulatefile', 'Data',
            '/sharefile', 'ShareFile',
            '/extractfile','ExtractFile',
            '/info', 'info',
            '/info/(.*)', 'info')
			
    # create a web.application object providing the urls
    app = web.application(urls, globals())
    # set up session
    web.config.debug = False
    session = web.session.Session(app, web.session.DiskStore('session'), initializer={'logged_in':False,'username':''})     # check the number of available fileContents if there is any in the data directory
    db = web.database(dbn='mysql', db='FileSystem', user='root', pw='12345')
    fileCount = fileValidator(myConfig.getDataDir())
    logging.info('The data directory is: {0}'.format(myConfig.getDataDir()))
    logging.info('The number of files is: {0}'.format(fileCount))
    # run the webserver
    web.httpserver.runsimple(app.wsgifunc(), myConfig.getIP())

if __name__ == "__main__":
    main()
