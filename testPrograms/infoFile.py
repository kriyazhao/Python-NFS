#!/usr/bin/python

# infoFile.py
# A client-side request to get information from the server
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
    parseArg = argparse.ArgumentParser(description = "A client-side request to get information from the server")
    parseArg.add_argument('--host', help = "host ip address")
    parseArg.add_argument('--port', type=int, help = "host port")
    parseArg.add_argument('--inquery', help = "info keyword (e.g. checkfile)")
    args = parseArg.parse_args()

    url = "http://{0}:{1}/info/{2}".format(args.host, args.port, args.inquery)
    headers = {'Content-Type': 'application/octet-stream'}
    r = requests.get(url, headers=headers)
    for item in r.content:
        print "{0} : {1}".format(item, r.content[item])

if __name__ == "__main__":
    main()
