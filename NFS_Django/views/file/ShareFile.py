#==========================================================================================================================
# import python modules
import os
import json
import logging
logging.basicConfig(level=logging.INFO)
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel 

#==========================================================================================================================
# ShareFile class for providing md5 and sha1 to the client
class ShareFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        if "username" in request.session:
            requestCon = json.loads(request.body)
            if requestCon["owner"] == "self":
                owner = request.session["username"]
            else:
                owner = requestCon["owner"]
            with FileModel() as filemodel:
                filemodel.setUsername(owner)
                filemodel.setFileName(requestCon["filename"])
                rows = filemodel.queryHashCode()
            if rows == None:
                return HttpResponse(json.dumps('notfound'), content_type="application/json")
            else:
                with ShareFileModel() as sharefilemodel:
                    sharefilemodel.setOwner(owner)
                    sharefilemodel.setFileID(rows[3])
                    list = sharefilemodel.querySharedList_owner()
                    logging.info("List:" + str(list))
                dumpInfo = [{'md5':rows[1],'sha1':rows[2], 'owner':owner, 'privilege': rows[4]}]
                for item in list:
                    dumpInfo.append(item)
                return HttpResponse(json.dumps(dumpInfo), content_type="application/json")
        else:
                return HttpResponse(json.dumps('notlogin'), content_type="application/json")
                