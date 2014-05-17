#!/usr/bin/python

# deletefile.py
# A client-side request to delete a file to the server
# Ting Zhao (t.zhao2011@gmail.com)

#==================================================================================================================
# imports
import requests
import argparse
import hashlib

#==================================================================================================================
# main function
def main():

	# parse the command line arguments using argparse module
    parseArg = argparse.ArgumentParser(description = "A client-side request to delete a file to the server")
    parseArg.add_argument('--host', help = "host ip address")
    parseArg.add_argument('--port', type=int, help = "host port")
    parseArg.add_argument('--md5', help = "md5 code to send")
    parseArg.add_argument('--sha1', help = "sha1 code to send")
    args = parseArg.parse_args()
    
    # build the URL from the file content and request data
    url = "http://{0}:{1}/data/{2}/{3}".format(args.host, args.port, args.md5, args.sha1)
    print "Requested file:"
    print "MD5:  {0}\n  SHA1: {1}".format(args.md5, args.sha1)
    r = requests.delete(url)
    print "Result: {0}".format(r.text)

if __name__ == "__main__":
    main()
