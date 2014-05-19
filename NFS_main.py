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
import index
import info
import Login
import Logout
import Data
import fileValidator
import ErrorHandler

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
