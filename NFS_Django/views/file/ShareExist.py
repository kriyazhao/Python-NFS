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
from NFS_Django.views.util.UserValidator import UserValidator

from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.UserModel import UserModel

#==========================================================================================================================
# ShareFile class for providing md5 and sha1 to the client
class ShareExist(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = UserValidator() # validate input
        if "username" in request.session:
            requestCon = json.loads(request.body)
            validator.setUsername(requestCon['un'])
            if validator.usernameValidate() == True:
                with UserModel() as usermodel:
                    usermodel.setUsername(requestCon['un'])
                    rows = usermodel.queryRegister()
                if rows == None:
                    return HttpResponse(json.dumps('notfound'), content_type="application/json")
                else:
                    return HttpResponse(json.dumps('success'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('notvalid'), content_type="application/json")
        else:
            return HttpResponse(json.dumps('notlogin'), content_type="application/json")