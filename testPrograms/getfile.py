#!/usr/bin/python

# getfile.py
# A client-side request to get a file to the server
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
    parseArg = argparse.ArgumentParser(description = "A client-side request to get a file to the server")
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
    url2 = "http://{0}:{1}/data/{2}/{3}".format(args.host, args.port, args.md5, args.sha1)
    print "Requested file:"
    print "MD5:  {0}\n  SHA1: {1}".format(args.md5, args.sha1)
    r = requests.get(url2)
    file = r.content
	
	# logout
    url3 = "http://{0}:{1}/logout".format(args.host, args.port)
    o = requests.get(url3)
    print o.text

if __name__ == "__main__":
    main()
