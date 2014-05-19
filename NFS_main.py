#!/usr/bin/python
#
# -------------------------------------------------------------------------------------------------
# DFS_daemon.py
# Created on: 2014-03-08 22:30:50.00000
# Updated on: 2014-05-17 21:19:34.00000
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

# import customized modules
import nfsConfig

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
        self.configParams = ConfigParser.ConfigParser().read(self.fileConfig)
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
# Login class handles post request of login
class Login:
    global session
    def POST(self):
        requestContent = json.loads(web.data())
        if requestContent["username"] == "root" and requestContent["password"] == "202cb962ac59075b964b07152d234b70":
            session.logged_in = True
            return "login successfully!"
        else:
            return "login failed!"

#==========================================================================================================================
# Logout class handles get request of logout
class Logout:
    global session
    def GET(self):
        session.logged_in = False
        session.kill()
        return "logout successfully!"


#==========================================================================================================================
# Data class for acquiring, creating and deleting file fileContents.
class Data:

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, hashMD5, hashSHA1, writeType = "get"): # writeType in "get", "put" and "delete"
        global myConfig, fileCount, session

        # build the hashed path
        increNum = len(hashMD5) // 2
        while not hashMD5[increNum].isdigit():
            increNum += 1
        completePath = "{0}/".format(myConfig.getDataDir())
        dirpath = "{0}/".format(myConfig.getDataDir())
        dirpath += "{0}".format(hashMD5[0:int(hashMD5[increNum])])
        for i in range(0, len(hashMD5), int(hashMD5[increNum])):
            completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
        if writeType == "put":
            return completePath
        elif writeType == "delete":
            return dirpath
        elif writeType == "get":
            completePath += "{0}.obj".format(hashSHA1)
            return completePath
        else:
            raise TypeError("write type cannot be recgnized!")
            return

    # verifyfileContent function verifies if the path can be converted to the hash values
    def verifyfileContent(self, completePath, hashMD5, hashSHA1):
        global myConfig, fileCount, session
   
        # verify the fileContent
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return self.NotFoundError()
        else:
            with open(completePath, 'rb') as data:
                fileContent = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            myMD5 = hashlib.md5(fileContent).hexdigest()
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # to see if hash is verified
            if myMD5 == hashMD5 and mySHA1 == hashSHA1:
                return True
            else:
                return False
            
    # GET function responds to request.get method from the client-side
    def GET(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session
	
	if session.get('logged_in', True):	
            # build the hashed path and read the file
            completePath = self.writePath(hashMD5, hashSHA1, "get")
            # raise error if no such file is found
            verifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
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
            
    # PUT function responds to request.put method from the client-side
    def PUT(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session
		
        # get the fileContent data from the client-side
        fileContent = web.data()
        if len(fileContent) > myConfig.getMaxSize():
            # The fileContent is wrong.  Return a 400 bad request error. Log info about the remote in the future.
            logging.warning("fileContent size exceeds the limit!")
            logging.info("actual fileContent size: {0}".format(len(fileContent)))
            logging.info("config fileContent size: {0}".format(myConfig.getMaxSize()))
            return "fileContent size exceeds the limit!"
        # build the hashed path and write the file
        completePath = self.writePath(hashMD5, hashSHA1, "put")
        # create the path if not detected
        if not os.path.exists(completePath):
            os.makedirs(completePath)
        completePath += "{0}.obj".format(hashSHA1)
        # write the file if not detected
        if not os.path.isfile(completePath):
            logging.info("Adding a new fileContent at: {0}".format(completePath))
            with open(completePath, 'wb') as data:
                data.write(fileContent)
        else:
            logging.info("file already exists: {0}".format(completePath))
            return "file already exists!"
        # read the file again and verify it is hashed correctly
        verifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
        if verifyResult == True:
            fileCount += 1
            return "Successfully add the fileContent!"
        else:
            return self.NotFoundError()
        # return an error if the provided codes doesn't match that of the fileContent
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return self.ServerError()

    # DELETE function responds to request.delete method from the client-side
    def DELETE(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session

        # build the hashed path 
        completePath = self.writePath(hashMD5, hashSHA1)
        # raise error if no such file is found
        vertifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
        if vertifyResult == True:
            dirpath = self.writePath(hashMD5, hashSHA1, "delete")
            shutil.rmtree(dirpath)
            fileCount -= 1
            return "Successfully delete the fileContent!"
        else:
            return self.NotFoundError()
        # return an error if the provided codes doesn't match that of the fileContent
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return self.ServerError()

    # POST function responds to request.post method from the client-side
    def POST(self, hashMD5, hashSHA1):
        global myConfig, fileCount, session

        # build the hashed path
        completePath = self.writePath(hashMD5, hashSHA1)
        # verify fileContent 
        vertifyResult = self.verifyfileContent(completePath, hashMD5, hashSHA1)
        if vertifyResult == True:
            requestCon = web.data()
            requestContent = json.loads(requestCon)
            logging.info("requestContent: {0}".format(requestContent))
            logging.info("type: {0}".format(type(requestContent)))
            if "insert" in requestContent:
                with open(completePath, 'r+') as data:
                    oldfileContent = data.read()
                    logging.info("insert oldfileContent: {0}".format(oldfileContent))
                for i in requestContent["insert"]:
                    newfileContent = oldfileContent[0:int(i[0])] + i[1] + oldfileContent[int(i[0])+1:]
                    logging.info("insert newfileContent: {0}".format(newfileContent))
                    with open(completePath, 'w+') as data:
                        data.write(newfileContent)
            if "modify" in requestContent:
                with open(completePath, 'r+') as data:
                    oldfileContent = data.read()				
                for i in requestContent["modify"]:
                    newfileContent = oldfileContent[0:int(i[0])] + i[2] + oldfileContent[int(i[1])+1:]
                    with open(completePath, 'w+') as data:
                        data.write(newfileContent)
            if "delete" in requestContent:
                with open(completePath, 'r+') as data:
                    oldfileContent = data.read()
                for i in requestContent["delete"]:
                    newfileContent = oldfileContent[0:int(i[0])] + oldfileContent[int(i[1])+1:]
                    with open(completePath, 'w+') as data:
                        data.write(newfileContent)
            logging.info("Successfully update the file!")
            # rewrite hash path and filename for the updated file 
            with open(completePath, 'rb') as data:
                fileContent = data.read()
            myMD5 = hashlib.md5(fileContent).hexdigest()
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            newPath = self.writePath(myMD5, mySHA1, "put")
            if not os.path.exists(newPath):
                os.makedirs(newPath)
            newPath += "{0}.obj".format(hashSHA1)
            if not os.path.isfile(newPath):
                logging.info("Adding a new fileContent at: {0}".format(newPath))
                with open(newPath, 'wb') as result:
                    result.write(fileContent)
            else:
                return "new file already exists!"
            # delete the original path and file
            dirpath = self.writePath(hashMD5, hashSHA1, "delete")
            shutil.rmtree(dirpath)
            logging.info("Deleting the old fileContent at: {0}".format(completePath))
            return fileContent
        else:
            return self.NotFoundError()
        # return an error if the provided codes doesn't match that of the fileContent
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return self.ServerError()
    
    # NotFoundError function handles errors of no files found 
    def NotFoundError():
        return web.notfound("404 Not Found")

    # ServerError function handles errors from the server side 
    def ServerError():
        return web.internalerror("500 Internal Server Error")

#==========================================================================================================================
# index class for redirecting the get request to info class
class index:
    def GET(self):
        raise web.seeother('/info')

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
def fileValidator(self, path):
    global myConfig, fileCount, session

    fileCount = 0
    for root, dir, files in os.walk(path):
        logging.info("validateFiles: root:  {0}".format(root))
        logging.info("validateFiles: dir:   {0}".format(str(dir)))
        logging.info("validateFiles: files: {0}".format(str(files)))
        for currentFile in files:
            validateFile = True
            logging.info("validateFiles: currentFile: {0}".format(currentFile))
            # read the content of the file
            fileContent = open(os.path.abspath("{0}/{1}".format(root, currentFile)), 'rb').read()
            # hash the fileContent
            myMD5 = hashlib.md5(fileContent).hexdigest()
            mySHA1 = hashlib.sha1(fileContent).hexdigest()
            # write the path with a strategy
            increNum = len(myMD5) // 2
            while not myMD5[increNum].isdigit():
                increNum += 1
            currentPath = "{0}/".format(myConfig.getDataDir())
            dirpath = "{0}/".format(myConfig.getDataDir())
            dirpath += "{0}/".format(myMD5[0:int(myMD5[increNum])])
            for i in range(0, len(myMD5), int(myMD5[increNum])):
                currentPath += "{0}/".format(myMD5[i:i+int(myMD5[increNum])])
            # check the filepath
            if os.path.abspath(currentPath) != os.path.abspath(root):
                # The hashed path cannot be matched to that of the original file.
                logging.warning("The file path has been modified!!!")
                logging.info("	root:    {0}".format(os.path.abspath(root)))
                logging.info("	currentPath: {0}".format(os.path.abspath(currentPath)))
                validateFile = False
            # check the filename
            if currentFile != "{0}.obj".format(mySHA1):
                # The hashed filename cannot be matched to that of the original file.
                logging.warning("The file name has been modified!!!")
                logging.info("	currentFile: {0}".format(currentFile))
                logging.info("	mySHA1:  {0}".format(mySHA1))
                validateFile = False
            # increment the fileCount if no modification is detected for the files
            if validateFile == True:
                fileCount += 1
            # delete the files that have been modified by others
            else:
                logging.warning("Deleting the files that has been modified by others!")
                shutil.rmtree(dirpath)
    return fileCount

#==========================================================================================================================
# main function of the program
def main():
    global myConfig, fileCount, session

    # set the current basic config to INFO mode
    logging.basicConfig(level=logging.INFO)

    # parse the command line arguments using argparse module
    parseArg = argparse.ArgumentParser(description = "This is the daemon file of the system.")
    parseArg.add_argument('--fileConfig', help = "Configuration file (e.g. ip, port, datadir)")
    parseArg.add_argument('--sectionConfig', help = "Section in the configuration file to use (e.g. 'defaultConfig' by default)")
    args = parseArg.parse_args()
    logging.info('Input arguments: \n{0}'.format(str(args)))#(fileConfig = 'fileConfig.conf', sectionConfig = 'defaultConfig')

    # pass the config params to nfsConfig function
    myConfig = nfsConfig(args.fileConfig)

    # set up the webserver to handle requests.
    # any url matches the regular expression will be sent to the corresponding class/function for handling
    urls = ('/', 'index',
            '/data/([0-9,a-f,A-F]+)/([0-9,a-f,A-F]+)', 'Data',
            '/login', 'Login',
            '/logout', 'Logout',
            '/info', 'info',
            '/info/(.*)', 'info')
			
    # create a web.application object providing the urls
    app = web.application(urls, globals())
    # set up session
    web.config.debug = False
    session = web.session.Session(app, web.session.DiskStore('session'))    
    # check the number of available fileContents if there is any in the data directory
    fileCount = fileValidator(myConfig.getDataDir())
    logging.info('The data directory is: {0}'.format(myConfig.getDataDir()))
    logging.info('The number of files is: {0}'.format(fileCount))
    
    # run the webserver
    web.httpserver.runsimple(app.wsgifunc(), myConfig.getIP())

if __name__ == "__main__":
    main()
