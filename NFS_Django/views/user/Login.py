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
from NFS_Django.views.util.EncryptionPassword import EncryptionPassword
from NFS_Django.views.util.UserValidator import UserValidator
from NFS_Django.views.model.UserModel import UserModel
#==========================================================================================================================
# Login class handles post request of login


class Login(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        validator = UserValidator() # validate input
        encryptpw = EncryptionPassword() # encrypt password
        if "username" not in request.session:
            regInfo = json.loads(request.body)
            logging.info(regInfo)
            validator.setUsername(regInfo['un'])
            validator.setPassword(regInfo['pw'])
            encryptpw.setPassword(regInfo['pw'])         
            if validator.usernameValidate() == True and validator.passwordValidate() == True:
                with UserModel() as usermodel:
                    usermodel.setUsername(regInfo['un'])
                    salt = usermodel.querySalt()[11]
                    hashPW = encryptpw.encryptPw(salt)[0]
                    usermodel.setPassword(hashPW)
                    rows = usermodel.queryLogin()
                    logging.info(rows)
                    if rows != None:
                        usermodel.updateLoginDate()
                if rows != None:
                    request.session["username"] = regInfo['un']
                    return HttpResponse(json.dumps({'r':1,'un':request.session["username"]}), content_type="application/json") # successfully login
                else:
                    return HttpResponse(json.dumps({'r':0}), content_type="application/json") # incorrect username/password
            else:
                return HttpResponse(json.dumps({'r':3}), content_type="application/json")# username/password not validated
        else:
            return HttpResponse(json.dumps({'r':2,'un':request.session["username"]}), content_type="application/json") # already login