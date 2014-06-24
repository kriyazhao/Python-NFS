#==========================================================================================================================
# import python modules
import os
import json
import shutil
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
from NFS_Django.views.model.ShareFileModel import ShareFileModel
from NFS_Django.views.model.FileActivityLog import FileActivityLog

#==========================================================================================================================
# DeleteFile class for handing delete request from the client-side
class DeleteFile(View):

    @method_decorator(csrf_protect)
    def delete(self, request):
        readfile = FileNotepad()
        writenewfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()

        if "username" in request.session:	
            requestCon = json.loads(request.body)
            if requestCon["owner"] == "self": # the owner asks to delete the file
                ownerName = request.session["username"]
                with FileModel() as filemodel:
                    filemodel.setUsername(ownerName)
                    filemodel.setFileName(requestCon["filename"])
                    rows = filemodel.queryHashCode()
                    if rows != None:
                        fileID = rows[3]
                        userID = rows[0]
                if rows == None:
                    return HttpResponse("notfound", content_type="text/plain")
                else:
                    with ShareFileModel() as sharefilemodel:
                        sharefilemodel.setFileID(fileID)
                        sharefilemodel.setOwner(ownerName)
                        desharelist = sharefilemodel.deleteSharedWith_owner()

                    for item in desharelist:
                        # write log
                        with FileActivityLog() as activitylog:
                            activitylog.setUserID(userID)
                            activitylog.setFileID(item["fileID"])
                            activitylog.setCurName(requestCon["filename"])
                            activitylog.setOwnerID(userID)
                            activitylog.setSharedwithID(item["sharedwithID"])
                            activitylog.setSharedPrvlg(item["privilege"])
                            activitylog.insertDeletedShare()

                    encrypt.setHashCode(rows[1], rows[2])
                    completePath = encrypt.writePath("get")
                    filevalidator.setfilePath(completePath)
                    if filevalidator.verifyfileContent(rows[2]) == False:
                        logging.error("Something is weird about the provided: {0}".format(completePath))
                        return HttpResponse("internalerror", content_type="text/plain")
                    else:
                        with FileModel() as filemodel:
                            filemodel.setUsername(ownerName)
                            filemodel.setFileName(requestCon["filename"])
                            filemodel.setHashCode(rows[1], rows[2])
                            filemodel.deleteFile()
                        dirpath = encrypt.writePath("delete")
                        shutil.rmtree(dirpath)

                        # write log
                        with FileActivityLog() as activitylog:
                            activitylog.setUserID(userID)
                            activitylog.setFileID(fileID)
                            activitylog.setCurName(requestCon["filename"])
                            activitylog.setOwnerID(userID)
                            activitylog.insertDelete()

                        return HttpResponse("success", content_type="text/plain")  
            else:
                ownerName = requestCon["owner"]

                with ShareFileModel() as sharefilemodel:
                    sharefilemodel.setFileAlias(requestCon["filename"])
                    sharefilemodel.setOwner(ownerName)
                    sharefilemodel.setSharedWith(request.session["username"])
                    row = sharefilemodel.queryShareFile_fileAlias()
                    if row != None:
                        fileID = row[1]
                        userID = row[4]
                        ownerID = row[3]
                if row == None:
                    return HttpResponse("notfound", content_type="text/plain")
                else:
                    with FileModel() as filemodel:
                        filemodel.setUsername(ownerName)
                        filemodel.setFileName(requestCon["filename"])
                        rows = filemodel.queryHashCode()

                    with ShareFileModel() as sharefilemodel:
                        sharefilemodel.setFileID(fileID)
                        sharefilemodel.setOwner(ownerName)
                        sharefilemodel.setSharedWith(request.session["username"])
                        privilege = sharefilemodel.queryShareFile()[5]

                        if privilege == 11 or privilege == 21:
                            sharefilemodel.setFileAlias(requestCon["filename"])
                            desharelist = sharefilemodel.deleteSharedFile()
                        elif privilege == 12 or privilege == 22:
                            desharelist = sharefilemodel.deleteSharedWith_owner()

                            for item in desharelist:
                                # write log
                                with FileActivityLog() as activitylog:
                                    activitylog.setUserID(userID)
                                    activitylog.setFileID(item["fileID"])
                                    activitylog.setCurName(requestCon["filename"])
                                    activitylog.setOwnerID(ownerID)
                                    activitylog.setSharedwithID(item["sharedwithID"])
                                    activitylog.setSharedPrvlg(item["privilege"])
                                    activitylog.insertDeletedShare()

                    if privilege == 12 or privilege == 22:
                        encrypt.setHashCode(rows[1], rows[2])
                        completePath = encrypt.writePath("get")
                        filevalidator.setfilePath(completePath)
                        if filevalidator.verifyfileContent(rows[2]) == False:
                            logging.error("Something is weird about the provided: {0}".format(completePath))
                            return HttpResponse("internalerror", content_type="text/plain")
                        else:
                            with FileModel() as filemodel:
                                filemodel.setUsername(ownerName)
                                filemodel.setFileName(requestCon["filename"])
                                filemodel.setHashCode(rows[1], rows[2])
                                filemodel.deleteFile()
                            dirpath = encrypt.writePath("delete")
                            shutil.rmtree(dirpath)

                    # write log
                    with FileActivityLog() as activitylog:
                        activitylog.setUserID(userID)
                        activitylog.setFileID(fileID)
                        activitylog.setCurName(requestCon["filename"])
                        if privilege == 11 or privilege == 21: 
                            activitylog.setOwnerID(userID)
                        if privilege == 12 or privilege == 22: 
                            activitylog.setOwnerID(ownerID)
                        activitylog.insertDelete()

                    return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("notlogin", content_type="text/plain")