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
# EditUser class handles post request of editting profile
class EditUser(View):

    def get(self, request):
        if "username" in request.session:
            with UserModel() as usermodel:
                usermodel.setUsername(request.session["username"])
                rows = usermodel.queryRegister()
            if rows == None:
                return HttpResponse(json.dumps({'r':"empty"}), content_type="application/json") 
            else:
                return HttpResponse(json.dumps({'r':"success", "un":rows["un"],"fn":rows["fn"],"ln":rows["ln"],"em":rows["em"]}), content_type="application/json") 
        else:
            return HttpResponse(json.dumps({'r':"notlogin"}), content_type="application/json") 

    @method_decorator(csrf_protect)
    def post(self, request):
        validator = UserValidator() # validate input
        encryptpw = EncryptionPassword() # encrypt password
        if "username" in request.session:
            regInfo = json.loads(request.body)
            validator.setPassword(regInfo["newpass"])
            encryptpw.setPassword(regInfo["oldpass"])
            if regInfo["newpass"] == "" or validator.passwordValidate() == True:
                with UserModel() as usermodel:
                    usermodel.setUsername(request.session["username"])
                    salt = usermodel.querySalt()[11]
                    hashPW = encryptpw.encryptPw(salt)[0]
                    usermodel.setPassword(hashPW)
                    rows = usermodel.queryLogin()
                if rows != None:
                    hashList = encryptpw.encryptPw()
                    newoldPW = encryptpw.encryptPw()[0]
                    newSalt = encryptpw.encryptPw()[1]
                    if regInfo["newpass"] == "":
                        newPW = newoldPW 
                    else:
                        encryptpw.setPassword(regInfo["newpass"])
                        newPW = encryptpw.encryptPw(newSalt)[0]
                    with UserModel() as usermodel:
                        usermodel.setUsername(request.session["username"])
                        usermodel.setPassword(newPW)
                        usermodel.setEmail(regInfo["em"])
                        usermodel.setSalt(newSalt)
                        usermodel.setFirstname(regInfo["fn"])
                        usermodel.setLastname(regInfo["ln"])
                        usermodel.updateRegister()
                    return HttpResponse("success", content_type="text/plain") 
                else:
                    return HttpResponse("notcorrect", content_type="text/plain") 
            else:
                return HttpResponse("notvalid", content_type="text/plain") 
        else:
            return HttpResponse("notlogin", content_type="text/plain") 