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
from NFS_Django.views.util.EncryptionPath import EncryptionPath
from NFS_Django.views.util.FileNotepad import FileNotepad 
from NFS_Django.views.util.FileValidator import FileValidator
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel 

#==========================================================================================================================
# ViewFile class for handing get request from the client-side
class ViewFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):

        requestCon = json.loads(request.body)
        if requestCon["owner"] == "self":
            return ViewFile_owner().post(request)
        else:
            return ViewFile_sharer().post(request)

class ViewFile_owner(View):

    @method_decorator(csrf_protect)
    def post(self, request):            
    
        readfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()
        if "username" in request.session:
            requestCon = json.loads(request.body)
            ownerName = request.session["username"]
            with FileModel() as filemodel:
                filemodel.setUsername(ownerName)
                filemodel.setFileName(requestCon["filename"])
                rows = filemodel.queryHashCode()
                if rows != None:
                    fileID = rows[3]
            if rows == None:
                    return HttpResponse("notfound", content_type="text/plain")
            else:
                with FileModel() as filemodel:
                    filemodel.setFileID(fileID)
                    row = filemodel.queryFile_fileID()

                encrypt.setHashCode(row[1], row[2])
                completePath = encrypt.writePath("get")
                filevalidator.setfilePath(completePath)
                if filevalidator.verifyfileContent(row[2]) == False:
                    logging.error("Something is weird about the provided: {0}".format(completePath))
                    return HttpResponse("internalerror", content_type="text/plain")
                else:
                    readfile.setFilepath(completePath)
                    fileContent = readfile.readFile()
                    return HttpResponse(fileContent, content_type="text/plain")
        else:
            return HttpResponse("notlogin", content_type="text/plain")
    
class ViewFile_sharer(View):

    @method_decorator(csrf_protect)
    def post(self, request): 
    
        readfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()
        if "username" in request.session:
            requestCon = json.loads(request.body)
            ownerName = requestCon["owner"]
            with ShareFileModel() as sharefilemodel:
                sharefilemodel.setFileAlias(requestCon["filename"])
                sharefilemodel.setOwner(ownerName)
                sharefilemodel.setSharedWith(request.session["username"])
                rows = sharefilemodel.queryShareFile_fileAlias()
                if rows != None:
                    fileID = rows[1]
            if rows == None:
                return HttpResponse("notfound", content_type="text/plain")
            else:
                with FileModel() as filemodel:
                    filemodel.setFileID(fileID)
                    row = filemodel.queryFile_fileID()
                encrypt.setHashCode(row[1], row[2])
                completePath = encrypt.writePath("get")
                filevalidator.setfilePath(completePath)
                if filevalidator.verifyfileContent(row[2]) == False:
                    logging.error("Something is weird about the provided: {0}".format(completePath))
                    return HttpResponse("internalerror", content_type="text/plain")
                else:
                    readfile.setFilepath(completePath)
                    fileContent = readfile.readFile()
                    return HttpResponse(fileContent, content_type="text/plain")
        else:
            return HttpResponse("notlogin", content_type="text/plain")
