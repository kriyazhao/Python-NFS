#!/usr/bin/python
#
# -------------------------------------------------------------------------------------------------
# DFS_daemon.py
# Created on: 2014-03-08 22:30:50.00000
# Updated on: 2014-05-05 21:19:34.00000
# Author: Ting Zhao (t.zhao2011@gmail.com)
# Description: A daemon program for a simple Distributed File System. 
#              This is for handling requests (put, get, post and delete) from client to server
# -------------------------------------------------------------------------------------------------

#==========================================================================================================================
# imports
import logging
import argparse
import ConfigParser
import hashlib
import shutil
import web
import os
import platform
import json
import ctypes # in case the platform is windows

#==========================================================================================================================
# global variables
myConfig = None
numChunks = 0

#==========================================================================================================================
# nfsConfig class for NFS configurations, which is server-side only
class nfsConfig:
    
    # initialize the configuration class
    def __init__(self, conFile = None):
        self.fileConfig = 'fileConfig.conf'
        self.sectionConfig = 'defaultConfig'
        self.ipaddr = '198.46.132.117'
        self.port = '8080'
        self.datadir = 'data'
        self.maxsize = '25'
        if conFile != None:
            self.fileConfig = conFile
        # Load the configuration from the file
        self.tmpConfig = ConfigParser.ConfigParser()
        self.tmpConfig.read(self.fileConfig)

    # load the configuration from the specified section
    def load(self, conSection = None):
        if conSection != None:
            self.sectionConfig = conSection
        try:
            logging.info("Reading from config file:")
            for key, value in self.tmpConfig.items(self.sectionConfig):
                setattr(self, key, value)
                logging.info("	{0} = {1}".format(key, value))
        except OSError as ex:
            logging.error("Failed to read the provided config file: {0}".format(ex))
			
    # create an IP address for the webserver to use
    def getIP(self):
        return web.net.validip("{0}:{1}".format(self.ipaddr, self.port))

    # get the maximum size and convert from kb to bytes
    def getMaxSize(self):
        return int(self.maxsize) * 1024

    # get the specified directory and convert it to an absolute path
    def getDataDir(self):
        return os.path.abspath(self.datadir)

#==========================================================================================================================
# A function to check the status of chunks in the dataDir to see if they've been changed and return the number of chunks
def checkChunks(path):
    chunkCount = 0
    for root, dir, files in os.walk(path):
        logging.info("checkChunks: root:  {0}".format(root))
        logging.info("checkChunks: dir:   {0}".format(str(dir)))
        logging.info("checkChunks: files: {0}".format(str(files)))
        for currentFile in files:
            checkChunk = True
            logging.info("checkChunks: currentFile: {0}".format(currentFile))
            # read the content of the file as a chunk
            chunk = open(os.path.abspath("{0}/{1}".format(root, currentFile)), 'rb').read()
            # hash the chunk
            myMD5 = hashlib.md5(chunk).hexdigest()
            mySHA1 = hactypesshlib.sha1(chunk).hexdigest()
            # write the path
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
                # The hashed path cannot be matched to the original file.
                logging.warning("The file has been modified!!!")
                logging.info("	root:    {0}".format(os.path.abspath(root)))
                loggingctypes.info("	currentPath: {0}".format(os.path.abspath(currentPath)))
                checkChunk = False
            # check the filename
            if currentFile != ("{0}.obj".format(mySHA1)):
                # The hashed filename cannot be matched to the original file.
                logging.warning("The file has been modified!!!")
                logging.info("	currentFile: {0}".format(currentFile))
                logging.info("	mySHA1:  {0}".format(mySHA1))
                checkChunk = False
            # increment the chunkCount if no modification is detected for the files
            if checkChunk == True:
                chunkCount += 1
            # delete the files that have been modified by others
            else:
                logging.warning("Deleting the files that has been modified by others!")
                shutil.rmtree(dirpath)
    return chunkCount

#==========================================================================================================================
# index class for redirecting the get request to info class
class index:
    def GET(self):
        raise web.seeother('/info')

#==========================================================================================================================
# info class for displaying server infomation.
class info:

    # GET function responds to request.get method from the client-side
    def GET(self, paramStr = None):
        global myConfig, numChunks
        
        path = myConfig.getDataDir()
        # if /info/checkchunks is called, run the checkChunks function.
        if(paramStr == 'checkchunks'):
            numChunks = checkChunks(path)
        info = {'numChunks': numChunks}
        info['free'], info['freeNonSuper'], info['total'] = self.diskSpace(path)
        try:
            info['percFreeNoneSuper'] = 100 * (float(info['freeNonSuper']) / info['total'])
        except ZeroDivisionError:
            info['percFreeNoneSuper'] = 0
        logging.info("Total: {0}\nFree: {1}\nFreeNonSuper: {2}\npercFreeNonSuper: {3}".format(info['total'], info['free'], info['freeNonSuper'], info['percFreeNoneSuper']))
        web.header('Content-Type', 'application/json')
        return json.dumps(info)

    # diskSpace function to get free space and total space information (in megabytes)
    def diskSpace(path):
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
# Data class for acquiring, creating and deleting file chunks.
class Data:
    
    # GET function responds to request.get method from the client-side
    def GET(self, hashMD5, hashSHA1):
        global myConfig
		
        # build the hashed path and read the file
        completePath = "{0}/".format(myConfig.getDataDir())
        increNum = len(hashMD5) // 2
        while not hashMD5[increNum].isdigit():
            increNum += 1
        for i in range(0, len(hashMD5), int(hashMD5[increNum])):
            completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
        completePath += "{0}.obj".format(hashSHA1)
        # raise error if no such file is found
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return web.notfound()
        else:
            with open(completePath, 'rb') as data:
                chunk = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            myMD5 = hashlib.md5(chunk).hexdigest()
            mySHA1 = hashlib.sha1(chunk).hexdigest()
            # verify the chunk
            if myMD5 == hashMD5 and mySHA1 == hashSHA1:
                web.header("Content-Type", "application/octet-stream")
                return chunk
        # return an error if the provided codes doesn't match that of the chunk
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return web.internalerror()
    
    # PUT function responds to request.put method from the client-side
    def PUT(self, hashMD5, hashSHA1):
        global myConfig, numChunks
		
        # get the chunk data from the client-side
        chunk = web.data()
        if len(chunk) > myConfig.getMaxSize():
            # The chunk is wrong.  Return a 400 bad request error. Log info about the remote in the future.
            logging.warning("Chunk size exceeds the limit!")
            logging.info("actual chunk size: {0}".format(len(chunk)))
            logging.info("config chunk size: {0}".format(myConfig.getMaxSize()))
            return "Chunk size exceeds the limit!"
        # build the hashed path and write the file
        completePath = self.writePath(hashMD5, hashSHA1, "put")
        # create the path if not detected
        if not os.path.exists(completePath):
            os.makedirs(completePath)
        completePath += "{0}.obj".format(hashSHA1)
        # write the file if not detected
        if not os.path.isfile(completePath):
            logging.info("Adding a new chunk at: {0}".format(completePath))
            with open(completePath, 'wb') as data:
                data.write(chunk)
        # read the file again and verify it is hashed correctly
        verifyResult = self.verifyChunk(completePath, hashMD5, hashSHA1)
        if verifyResult == True:
            numChunks += 1
            return "Successfully add the chunk!"
        # return an error if the provided codes doesn't match that of the chunk
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return web.internalerror()

    # DELETE function responds to request.delete method from the client-side
    def DELETE(self, hashMD5, hashSHA1):
        global myConfig, numChunks
        # build the hashed path 
        completePath = self.writePath(hashMD5, hashSHA1)
        # raise error if no such file is found
        vertifyResult = self.verifyChunk(completePath, hashMD5, hashSHA1)
        if vertifyResult == True:
            dirpath = self.writePath(hashMD5, hashSHA1, "delete")
            shutil.rmtree(dirpath)
            numChunks -= 1
            return "Successfully delete the chunk!"
        # return an error if the provided codes doesn't match that of the chunk
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return web.internalerror()

    # POST function responds to request.post method from the client-side
    def POST(self, hashMD5, hashSHA1):
        global myConfig, numChunks
        # build the hashed path
        completePath = self.writePath(hashMD5, hashSHA1)
        # verify chunk 
        vertifyResult = self.verifyChunk(completePath, hashMD5, hashSHA1)
        if vertifyResult == True:
            requestCon = web.data()
            requestContent = json.loads(requestCon)
            logging.info("requestContent: {0}".format(requestContent))
            logging.info("type: {0}".format(type(requestContent)))
            if "insert" in requestContent:
                with open(completePath, 'r+') as data:
                    oldChunk = data.read()
                    logging.info("insert oldChunk: {0}".format(oldChunk))
                for i in requestContent["insert"]:
                    newChunk = oldChunk[0:int(i[0])] + i[1] + oldChunk[int(i[0])+1:]
                    logging.info("insert newChunk: {0}".format(newChunk))
                    with open(completePath, 'w+') as data:
                        data.write(newChunk)
            if "modify" in requestContent:
                with open(completePath, 'r+') as data:
                    oldChunk = data.read()				
                for i in requestContent["modify"]:
                    newChunk = oldChunk[0:int(i[0])] + i[2] + oldChunk[int(i[1])+1:]
                    with open(completePath, 'w+') as data:
                        data.write(newChunk)
            if "delete" in requestContent:
                with open(completePath, 'r+') as data:
                    oldChunk = data.read()
                for i in requestContent["delete"]:
                    newChunk = oldChunk[0:int(i[0])] + oldChunk[int(i[1])+1:]
                    with open(completePath, 'w+') as data:
                        data.write(newChunk)
            logging.info("Successfully update the file!")
            # rewrite hash path and filename for the updated file 
            with open(completePath, 'rb') as data:
                chunk = data.read()
            myMD5 = hashlib.md5(chunk).hexdigest()
            mySHA1 = hashlib.sha1(chunk).hexdigest()
            newPath = self.writePath(myMD5, mySHA1, "put")
            if not os.path.exists(newPath):
                os.makedirs(newPath)
            newPath += "{0}.obj".format(hashSHA1)
            if not os.path.isfile(newPath):
                logging.info("Adding a new chunk at: {0}".format(newPath))
                with open(newPath, 'wb') as result:
                    result.write(chunk)
            # delete the original path and file
            dirpath = self.writePath(hashMD5, hashSHA1, "delete")
            shutil.rmtree(dirpath)
            logging.info("Deleting the old chunk at: {0}".format(completePath))
            return chunk
        # return an error if the provided codes doesn't match that of the chunk
        logging.error("Something is weird about the provided: {0}".format(completePath))
        return web.internalerror()

    # writePath function writes the file path with hashMd5 and hashSHA1
    def writePath(self, hashMD5, hashSHA1, type = "get"): # type in "get", "put" and "delete"
        global myConfig
        # build the hashed path
        increNum = len(hashMD5) // 2
        while not hashMD5[increNum].isdigit():
            increNum += 1
        completePath = "{0}/".format(myConfig.getDataDir())
        dirpath = "{0}/".format(myConfig.getDataDir())
        dirpath += "{0}".format(hashMD5[0:int(hashMD5[increNum])])
        for i in range(0, len(hashMD5), int(hashMD5[increNum])):
            completePath += "{0}/".format(hashMD5[i:i+int(hashMD5[increNum])])
        if type == "put":
            return completePath
        elif type == "delete":
            return dirpath
        else:
            completePath += "{0}.obj".format(hashSHA1)
            return completePath

    # verifyChunk function verifies if the path can be converted to the hash values
    def verifyChunk(self, completePath, hashMD5, hashSHA1):
        # verify the chunk
        if not os.path.isfile(completePath):
            logging.info("File not found: {0}".format(completePath))
            return web.notfound()
        else:
            with open(completePath, 'rb') as data:
                chunk = data.read()
            # convert the hashed path and filename to hexadecimal numbers
            myMD5 = hashlib.md5(chunk).hexdigest()
            mySHA1 = hashlib.sha1(chunk).hexdigest()
            # delete the file if hash is verified
            if myMD5 == hashMD5 and mySHA1 == hashSHA1:
                return True
            else:
                return False

#==========================================================================================================================
# notFound and internalError functions are to handle errors
def notFound():
    return web.notfound("404 Not Found")

def internalError():
    return web.internalerror("500 Internal Server Error")

#==========================================================================================================================
# main function of the daemon program
def main():
    global myConfig, numChunks

    # set the current basic config to INFO mode
    logging.basicConfig(level=logging.INFO)

    # parse the command line arguments using argparse module
    argparser = argparse.ArgumentParser(description = "This is the daemon file of the system.")
    argparser.add_argument('--fileConfig', help = "Configuration file (e.g. ip, port, datadir)")
    argparser.add_argument('--sectionConfig', help = "Section in the configuration file to use (e.g. 'defaultConfig' by default)")
    args = argparser.parse_args()
    logging.info('Input arguments: \n	%s' % (str(args)))#(fileConfig = 'fileConfig.conf', sectionConfig = 'defaultConfig')

    # pass the config params to nfsConfig function
    myConfig = nfsConfig(args.fileConfig)
    myConfig.load(args.sectionConfig)

    # set up the webserver to handle requests.
    # any url matches the regular expression will be sent to the corresponding class/function for handling
    urls = ('/', 'index',
            '/data/([0-9,a-f,A-F]+)/([0-9,a-f,A-F]+)', 'Data',
            '/info', 'info',
            '/info/(.*)', 'info')
			
    # create a web.application object providing the urls
    app = web.application(urls, globals())
    app.notfound = notFound # in case the app.notfound is called, notFound() function will work
    app.internalerror = internalError # in case the app.internalerror is called, internalError() function will work
    
    # check the number of available chunks if there is any in the data directory
    numChunks = checkChunks(myConfig.getDataDir())
    logging.info('The data directory is: {0}'.format(myConfig.getDataDir()))
    logging.info('The number of chunks is: {0}'.format(numChunks))
    
    # run the webserver
    web.httpserver.runsimple(app.wsgifunc(), myConfig.getIP())

if __name__ == "__main__":
    main()
