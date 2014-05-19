#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

#==========================================================================================================================
# ErrorHandler class to handle web errors
class ErrorHandler:

    # NotFoundError function handles errors of no files found 
    def BadRequestError():
        return web.badrequest("400 Bad Request") 
    
    # NotFoundError function handles errors of no files found 
    def NotFoundError():
        return web.notfound("404 Not Found")

    # ServerError function handles errors from the server side 
    def ServerError():
        return web.internalerror("500 Internal Server Error")
