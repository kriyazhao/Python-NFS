#==========================================================================================================================
# import python modules
import logging
logging.basicConfig(level=logging.INFO)

import json
import datetime
import os
import hashlib
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from NFS_Django.views.util.EncryptionPassword import EncryptionPassword
from NFS_Django.views.util.UserValidator import UserValidator
from NFS_Django.views.model.UserModel import UserModel
from django.core.mail import send_mail

class ForgetPassword(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        requestCon = json.loads(request.body)
        uservalidator = UserValidator()
        uservalidator.setUsername(requestCon["un"])
        if uservalidator.usernameValidate() == True:
            with UserModel() as usermodel:
                usermodel.setUsername(requestCon["un"])
                usermodel.setEmail(requestCon["em"])
                rows = usermodel.queryForgetPassword()
            if rows == None:
                return HttpResponse("notfound", content_type="text/plain")
            else:
                newSalt = hashlib.md5(os.urandom(32)).hexdigest()
                try:
                    send_mail('Reset password for your NFS account', 'Hello '+requestCon["un"]+',\n \nPlease copy the following code to reset password:\n \n'+newSalt+'\n \nThanks,\nNFS', 't.zhao2011@gmail.com',[requestCon["em"]], fail_silently=False)
                    with UserModel() as usermodel:
                        usermodel.setUsername(requestCon["un"])
                        usermodel.setEmail(requestCon["em"])
                        usermodel.updateValidate(newSalt)
                    return HttpResponse("success", content_type="text/plain")
                except SMTPException:
                    return HttpResponse("fail", content_type="text/plain")
        else:
            return HttpResponse("notvalid", content_type="text/plain")


class ValidateCode(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        requestCon = json.loads(request.body)
        uservalidator = UserValidator()
        uservalidator.setUsername(requestCon["un"])
        with UserModel() as usermodel:
            usermodel.setUsername(requestCon["un"])
            usermodel.setEmail(requestCon["em"])
            rows = usermodel.queryForgetPassword()
        if requestCon["code"] == rows[12]:
            return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("fail", content_type="text/plain")



class ResetPassword(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        requestCon = json.loads(request.body)
        uservalidator = UserValidator()
        uservalidator.setPassword(requestCon["pw"])
        encryptpw = EncryptionPassword()
        encryptpw.setPassword(requestCon["pw"])
        hashList = encryptpw.encryptPw()
        newPass = hashList[0]
        newSalt = hashList[1]
        if uservalidator.passwordValidate() == True:
            with UserModel() as usermodel:
                usermodel.setUsername(requestCon["un"])
                usermodel.updateSalt(newSalt)
                usermodel.resetPassword(newPass)
                return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("notvalid", content_type="text/plain")
                                    