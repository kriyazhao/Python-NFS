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
from NFS_Django.views.util.FileValidator import FileValidator 
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel

#==========================================================================================================================
# RenameExist class for checking if file name already exists
class RenameExist(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = FileValidator() # validate input
        if "username" in request.session:
            requestCon = json.loads(request.body)
            if requestCon["owner"] == "self":
                ownerName = request.session["username"]

            else:
                ownerName = requestCon["owner"]
                with ShareFileModel() as sharefilemodel:
                    sharefilemodel.setFileAlias(requestCon['fn'])
                    sharefilemodel.setOwner(ownerName )
                    sharefilemodel.setSharedWith(request.session["username"])
                    sharerows = sharefilemodel.queryShareFile_fileAlias()
            validator.setfileName(requestCon['fn'])
            if validator.verifyfileName() == True:
                with FileModel() as filemodel:
                    filemodel.setFileName(requestCon['fn'])
                    filemodel.setUsername(ownerName)
                    rows = filemodel.queryHashCode()
                if requestCon["owner"] == "self":
                    if rows == None:
                        return HttpResponse(json.dumps(['success']), content_type="application/json")
                    else:
                        return HttpResponse(json.dumps(['exist']), content_type="application/json")
                else:
                    if rows == None and sharerows == None:
                        return HttpResponse(json.dumps(['success']), content_type="application/json")
                    else:
                        return HttpResponse(json.dumps(['exist']), content_type="application/json")
            else:
                return HttpResponse(json.dumps(['notvalid']), content_type="application/json")
        else:
            return HttpResponse(json.dumps(['notlogin']), content_type="application/json")