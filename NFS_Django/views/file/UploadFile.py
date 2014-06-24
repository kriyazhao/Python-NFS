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
from NFS_Django.views.util.EncryptionPath import EncryptionPath
from NFS_Django.views.util.FileNotepad import FileNotepad 
from NFS_Django.views.util.FileValidator import FileValidator
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.FileActivityLog import FileActivityLog 

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
#==========================================================================================================================
# Upload class for handing uploading request from the client-side
class UploadFile(View):
  
    @method_decorator(csrf_protect)
    def post(self, request):
        readfile = FileNotepad()
        writenewfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()

        Filename = request.POST.get("Filename")
        rawData = request.FILES["Filedata"]
        if filevalidator.verifyfileSize(rawData) == False:
            return HttpResponse("exceed", content_type="text/plain")
        else:
            filevalidator.setfileName(Filename)
            if filevalidator.verifyfileName() == False:
                return HttpResponse("namenotvalid", content_type="text/plain")
            else:
                tempFile = self.saveFile(Filename, rawData)
                readfile.setFilepath(tempFile)
                Filedata = readfile.readRawFile()
                Filecontent = readfile.processRawFile(Filedata)
                if "username" in request.session:	
                    with FileModel() as filemodel:
                        filemodel.setUsername(request.session["username"])
                        results = filemodel.queryUserID()
                        userID = results[0]
                        filemodel.setFileName(Filename)
                        rows = filemodel.queryHashCode()
                    if rows != None:
                        os.remove(tempFile)
                        return HttpResponse("exist", content_type="text/plain")

                    hashMD5 = encrypt.creatMD5(Filename, Filecontent, userID)
                    hashSHA1 = encrypt.creatSHA1(Filecontent)
                    completePath = encrypt.writePath("get")
                    filevalidator.setfilePath(completePath)
                    if filevalidator.verifyfilePath() == False:
                        # write the file if not detected
                        logging.info("Adding a new fileContent at: {0}".format(completePath))
                        writenewfile.setFilepath(completePath)
                        writenewfile.writeNewFile(Filecontent)
                        with FileModel() as filemodel:
                            filemodel.setUserID(userID)
                            filemodel.setUsername(request.session["username"])
                            filemodel.setFileName(Filename)
                            filemodel.setHashCode(hashMD5, hashSHA1)
                            filemodel.insertFile()
                            fileID = filemodel.queryHashCode()[3]

                        # write log
                        with FileActivityLog() as activitylog:
                            activitylog.setUserID(userID)
                            activitylog.setFileID(fileID)
                            activitylog.setCurName(Filename)
                            activitylog.setOwnerID(userID)
                            activitylog.insertUpload()

                        # read the file again and verify it is hashed correctly
                        if filevalidator.verifyfileContent(hashSHA1) == True:
                            os.remove(tempFile)
                            return HttpResponse("success", content_type="text/plain")
                        else:
                            os.remove(tempFile)
                            logging.error("Something is weird about the provided: {0}".format(completePath))
                            return HttpResponse("internalerror", content_type="text/plain")
                    else:
                        os.remove(tempFile)
                        return HttpResponse("exist", content_type="text/plain")
                else:
                    os.remove(tempFile)
                    return HttpResponse("notlogin", content_type="text/plain")

    def saveFile(self, name, data):
        with open(settings.MEDIA_ROOT + name,'w+') as myfile:
            for chunk in data.chunks():
                myfile.write(chunk)
        return settings.MEDIA_ROOT + name