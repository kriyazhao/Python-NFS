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
from NFS_Django.views.util.EncryptionPath import EncryptionPath
from NFS_Django.views.util.FileNotepad import FileNotepad
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.FileActivityLog import FileActivityLog

#==========================================================================================================================
# CreateFile class for creating files
class CreateFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):

        readfile = FileNotepad()
        writenewfile = FileNotepad()
        encrypt = EncryptionPath()
        validator = FileValidator() # validate input

        if "username" in request.session:
            requestCon = json.loads(request.body)
            validator.setfileName(requestCon['fn'])
            if validator.verifyfileName() == True:
                with FileModel() as filemodel:
                    filemodel.setUsername(request.session["username"])
                    userID = filemodel.queryUserID()[0]
                hashMD5 = encrypt.creatMD5(requestCon['fn'], "", userID)
                hashSHA1 = encrypt.creatSHA1("")
                completePath = encrypt.writePath("get")
                validator.setfilePath(completePath)
                if validator.verifyfilePath() == False:
                    # write the file if not detected
                    logging.info("Adding a new fileContent at: {0}".format(completePath))
                    writenewfile.setFilepath(completePath)
                    writenewfile.writeNewFile("")
                    with FileModel() as filemodel:
                        filemodel.setUsername(request.session["username"])
                        filemodel.setFileName(requestCon['fn'])
                        filemodel.setUserID(userID)
                        filemodel.setHashCode(hashMD5, hashSHA1)
                        filemodel.insertFile()
                        newRow = filemodel.queryFile()
                        fileID = newRow["ID"]

                    # write log
                    with FileActivityLog() as activitylog:
                        activitylog.setUserID(newRow["userID"])
                        activitylog.setFileID(fileID)
                        activitylog.setCurName(requestCon['fn'])
                        activitylog.insertCreate()

                    return HttpResponse(json.dumps(newRow), content_type="application/json")
                else:
                    return HttpResponse(json.dumps('exist'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('notvalid'), content_type="application/json")
        else:
            return HttpResponse(json.dumps('notlogin'), content_type="application/json")