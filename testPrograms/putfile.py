#!/usr/bin/python

# putfile.py
# A client-side request to put a file to the server
# Ting Zhao (t.zhao2011@gmail.com)

#==================================================================================================================
# imports
import requests
import urllib2
import argparse
import hashlib
import json

#==================================================================================================================
# main function
def main():
    
    # parse the command line arguments using argparse module
    parseArg = argparse.ArgumentParser(description = "A client-side request to put a file to the server")
    parseArg.add_argument('--host', help = "host ip address")
    parseArg.add_argument('--port', type=int, help = "host port")
    parseArg.add_argument('--filename', help = "file to send")
    parseArg.add_argument('--username', help = "username to send")
    parseArg.add_argument('--password', help = "password code to send")	
    args = parseArg.parse_args()

    # login first
    url1 = "http://{0}:{1}/login".format(args.host, args.port)
    hashPwd = hashlib.md5(args.password).hexdigest()
    payload = json.dumps({"username":args.username, "password":hashPwd})
    s = requests.post(url1, data = payload)	
    print s.text
	
    # build the URL from the file content and request data
    file = open(args.filename, 'rb').read()
    hashMD5 = hashlib.md5(file).hexdigest()
    hashSHA1 = hashlib.sha1(file).hexdigest()
	    url2 = "http://{0}:{1}/data/{2}/{3}".format(args.host, args.port, hashMD5, hashSHA1)
    headers = {'Content-Type': 'application/octet-stream'}
    print "MD5:  {0}\nSHA1: {1}".format(hashMD5, hashSHA1)
    r = requests.put(url2, data=file, headers=headers)
    print r.text
	
    #logout
    url3 = "http://{0}:{1}/logout".format(args.host, args.port)
    o = requests.get(url3)
    print o.text
if __name__ == "__main__":
    main()
