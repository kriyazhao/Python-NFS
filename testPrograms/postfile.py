#!/usr/bin/python

# postfile.py
# A client-side request to post update of a file to the server
# Ting Zhao (t.zhao2011@gmail.com)

#==================================================================================================================
# imports
import requests
import argparse
import hashlib
import json

#==================================================================================================================
# main function
def main():

    # parse the command line arguments using argparse module
    parseArg = argparse.ArgumentParser(description = "A client-side request to post update of a file to the server")
    parseArg.add_argument('--host', help = "host ip address")
    parseArg.add_argument('--port', type=int, help = "host port")
    parseArg.add_argument('--md5', help = "md5 code to send")
    parseArg.add_argument('--sha1', help = "sha1 code to send")
    parseArg.add_argument('--username', help = "username to send")
    parseArg.add_argument('--password', help = "password code to send")	
    args = parseArg.parse_args()

    # login
    url1 = "http://{0}:{1}/login".format(args.host, args.port)
    hashPwd = hashlib.md5(args.password).hexdigest()
    payload = json.dumps({"username":args.username, "password":hashPwd})
    s = requests.post(url1, data = payload)	
    print s.text
	
    # build the URL from the file content and request data
    url = "http://{0}:{1}/data/{2}/{3}".format(args.host, args.port, args.md5, args.sha1)
    print "Requested file:"
    print "MD5:  {0}\n  SHA1: {1}".format(args.md5, args.sha1)
    
    myData = json.dumps({"insert":[[2, "ohYES"]], "delete": [[10, 15]], "modify": [[4,7, "ohNO"]]})
    r = requests.post(url, data = myData)
    file = r.content
    hashMD5 = hashlib.md5(file).hexdigest()
    hashSHA1 = hashlib.sha1(file).hexdigest()
    print "Returned file with the new MD5 and SHA1"
    print "MD5:  {0}\n  SHA1: {1}".format(hashMD5, hashSHA1)
    print file

    # logout
    url3 = "http://{0}:{1}/logout".format(args.host, args.port)
    o = requests.get(url3)
    print o.text
	
if __name__ == "__main__":
    main()
