#==========================================================================================================================
# import python modules
import logging
logging.basicConfig(level=logging.INFO)
import os
import json
import datetime
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from NFS_Django.views.util.UserValidator import UserValidator
from NFS_Django.views.util.EncryptionPassword import EncryptionPassword
from NFS_Django.views.model.UserModel import UserModel

#==========================================================================================================================
# Register class handles post request of register
class Register(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = UserValidator() # validate input
        encryptpw = EncryptionPassword() # encrypt password
        if "username" not in request.session:
            regInfo = json.loads(request.body)
            validator.setUsername(regInfo["un"])
            validator.setPassword(regInfo["pw"])
            encryptpw.setPassword(regInfo["pw"])
            if validator.usernameValidate() == True and validator.passwordValidate() == True:
                with UserModel() as usermodel:
                    usermodel.setUsername(regInfo["un"])
                    rows = usermodel.queryRegister()
                if rows == None:
                    hashList = encryptpw.encryptPw()
                    hashPW = hashList[0]
                    newSalt = hashList[1]
                    with UserModel() as usermodel:
                        usermodel.setUsername(regInfo["un"])
                        usermodel.setPassword(hashPW)
                        usermodel.setSalt(newSalt)
                        usermodel.setEmail(regInfo["em"])
                        usermodel.setFirstname(regInfo["fn"])
                        usermodel.setLastname(regInfo["ln"])
                        usermodel.insertRegister()
                    request.session["username"] = regInfo["un"]
                    return HttpResponse(json.dumps({'r':"success",'un':request.session["username"]}), content_type="application/json") 
                else:
                    return HttpResponse(json.dumps({'r':"exist"}), content_type="application/json") 
            else:
                return HttpResponse(json.dumps({'r':"notvalid"}), content_type="application/json") 
        else:
            return HttpResponse(json.dumps({'r':"loggedin",'un':request.session["username"]}), content_type="application/json") 