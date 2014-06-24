#==========================================================================================================================
# import python modules
import json
import logging
logging.basicConfig(level=logging.INFO)

from django.http import HttpResponse
from django.views.generic import View
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel

class ListFile(View):

    def get(self, request):
        if "username" in request.session:
            with FileModel() as filemodel: # query my list
                filemodel.setUsername(request.session["username"])
                mylist = filemodel.queryList()
                logging.info(request.session["username"] + "'s My List: " + str(mylist))
            
            with ShareFileModel() as sharefilemodel: # query shared list
                sharefilemodel.setSharedWith(request.session["username"])
                sharedlist = sharefilemodel.querySharedList()
                logging.info(request.session["username"] + "'s Shared List: " + str(sharedlist))
            if mylist != None or sharedlist != None:
                return HttpResponse(json.dumps([mylist,sharedlist]), content_type="application/json")
            else:
                return HttpResponse(json.dumps(['empty']), content_type="application/json")
        else:
            return HttpResponse(json.dumps(['empty']), content_type="application/json")
