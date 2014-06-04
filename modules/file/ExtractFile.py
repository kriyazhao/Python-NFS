#==========================================================================================================================
# import python modules
import web
import json

import FileModel

#==========================================================================================================================
# ExtractFile class for extracting files given md5 and sha1 codes
class ExtractFile:

    self.modelfile = FileModel()
    
    def POST(self):
        web.header('Content-Type','application/json')
        requestCon = json.loads(web.data())
        self.modelfile.setHashCode(requestCon.md5, requestCon.sha1)
        results = self.modelfile.queryFile()
        rows = list(results)
        if len(rows) > 0:
            rows[0].createon = str(rows[0].createon)
            rows[0].updateon = str(rows[0].updateon)
            logging.info("1 file is found: {0}".format(rows[0]))
            return json.dumps(rows[0])
        else:
            return json.dumps([''])