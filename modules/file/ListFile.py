#==========================================================================================================================
# import python modules
import json

import CheckSession, FileModel

class ListFile:

    self.sess = CheckSession() // check session
    self.modelfile = FileModel() // file model

    def GET(self):
        if self.sess.getSession() == True:
            web.header('Content-Type','application/json')
            self.modelfile.setUsername(self.sess.getUsername())
            results = self.modelfile.queryList()
            rows = list(results)
            if len(rows) > 0:
                for row in rows:
                    row.createon = str(row.createon)
                    row.updateon = str(row.updateon)
                return json.dumps(rows)
            else:
                return json.dumps(['empty'])
        else:
            return json.dumps([''])