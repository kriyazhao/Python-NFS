#==========================================================================================================================
# import python modules
import logging
logging.basicConfig(level=logging.INFO)

import json
import datetime
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from NFS_Django.views.util.UserValidator import UserValidator
from NFS_Django.views.model.UserModel import UserModel 

#==========================================================================================================================
# RegisterExist class checks if the username exists
class RegisterExist(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = UserValidator() # validate input
        if "username" not in request.session:
            regInfo = json.loads(request.body)
            validator.setUsername(regInfo["un"])
            if validator.usernameValidate() == True:
                with UserModel() as usermodel:
                    usermodel.setUsername(regInfo["un"])
                    rows = usermodel.queryRegister()
                if rows == None:
                    return HttpResponse("success", content_type="text/plain") # username does not exist
                else:
                    return HttpResponse("exist", content_type="text/plain") # username exists
            else:
                return HttpResponse("notvalid", content_type="text/plain") # username exists
        else:
            return HttpResponse("loggedin", content_type="text/plain") # username does not exist
