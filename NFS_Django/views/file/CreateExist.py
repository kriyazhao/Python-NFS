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

#==========================================================================================================================
# CreateExist class for checking if file name already exists
class CreateExist(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = FileValidator() # validate input
        if "username" in request.session:
            requestCon = json.loads(request.body)
            validator.setfileName(requestCon['fn'])
            if validator.verifyfileName() == True:
                with FileModel() as filemodel:
                    filemodel.setFileName(requestCon['fn'])
                    filemodel.setUsername(request.session["username"])
                    rows = filemodel.queryHashCode()
                if rows == None:
                    return HttpResponse(json.dumps(['success']), content_type="application/json")
                else:
                    return HttpResponse(json.dumps(['exist']), content_type="application/json")
            else:
                return HttpResponse(json.dumps(['notvalid']), content_type="application/json")
        else:
            return HttpResponse(json.dumps(['notlogin']), content_type="application/json")