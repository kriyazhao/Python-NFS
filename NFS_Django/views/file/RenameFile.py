#==========================================================================================================================
# import python modules
import logging
logging.basicConfig(level=logging.INFO)
import shutil
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
from NFS_Django.views.model.FileActivityLog import FileActivityLog

#==========================================================================================================================
# Rename class for handing rename request from the client-side
class RenameFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        readfile = FileNotepad()
        writenewfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()

        if "username" in request.session:
            requestCon = json.loads(request.body)
            if requestCon["owner"] == "self":
                ownerName = request.session["username"]
                with FileModel() as filemodel:
                    filemodel.setUsername(ownerName)
                    filemodel.setFileName(requestCon["oldname"])
                    rows = filemodel.queryHashCode()
                    fileID = rows[3]
                    userID = rows[0]
                    ownerID = rows[0]
                    hashMD5 = rows[1]
                    hashSHA1 = rows[2]
            else:
                ownerName = requestCon["owner"]
                with ShareFileModel() as sharefilemodel:
                    sharefilemodel.setFileAlias(requestCon["oldname"])
                    sharefilemodel.setOwner(ownerName)
                    sharefilemodel.setSharedWith(request.session["username"])
                    rows = sharefilemodel.queryShareFile_fileAlias()
                    fileID = rows[1]
                    userID = rows[4]
                    ownerID = rows[3]
            if rows == None:
                return HttpResponse(json.dumps(["notfound"]), content_type="application/json")
            else:
                privilege = ""
                if requestCon["owner"] != "self":
                    with ShareFileModel() as sharefilemodel:
                        sharefilemodel.setFileID(fileID)
                        sharefilemodel.setOwner(ownerName)
                        sharefilemodel.setSharedWith(request.session["username"])
                        privilege = sharefilemodel.queryShareFile()[5]
                    with FileModel() as filemodel:
                        filemodel.setFileID(fileID)
                        result = filemodel.queryFile_fileID()
                        hashMD5 = result[1]
                        hashSHA1 = result[2]
                if privilege == 11 or privilege == 21 or privilege == 12 or privilege == 22:
                    with ShareFileModel() as sharefilemodel:
                        sharefilemodel.setFileID(fileID)
                        sharefilemodel.setOwner(ownerName)
                        sharefilemodel.setSharedWith(request.session["username"])
                        sharefilemodel.setFileAlias(requestCon["newname"])
                        sharefilemodel.setPrivilege(privilege)
                        sharefilemodel.updateShareFile()
                    if privilege == 11 or privilege == 21:
                        # write log
                        with FileActivityLog () as activitylog:
                            activitylog.setUserID(userID)
                            activitylog.setFileID(fileID)
                            activitylog.setCurName(requestCon["newname"]+"/"+requestCon["oldname"])
                            activitylog.setOwnerID(ownerID)
                            activitylog.insertRename()
                        return HttpResponse(json.dumps(["success"]), content_type="application/json")
                if requestCon["owner"] == "self" or privilege == 12 or privilege == 22:
                    encrypt.setHashCode(hashMD5, hashSHA1)
                    completePath = encrypt.writePath("get")
                    dirpath = encrypt.writePath("delete")
                    filevalidator.setfilePath(completePath)
                    if filevalidator.verifyfileContent(hashSHA1) == False:
                        logging.error("Something is weird about the provided: {0}".format(completePath))
                        return HttpResponse(json.dumps(["internalerror"]), content_type="application/json")
                    else:
                        readfile.setFilepath(completePath)
                        fileContent = readfile.readFile()
                        newMD5 = encrypt.creatMD5(requestCon["newname"], fileContent, ownerID)
                        newSHA1 = encrypt.creatSHA1(fileContent)
                        logging.info("newMD5: {0}".format(newMD5))
                        logging.info("newSHA1: {0}".format(newSHA1))
                        newPath = encrypt.writePath("get")
                        filevalidator.setfilePath(newPath)
                        logging.info("newfile: {0}".format(newPath))
                        if filevalidator.verifyfilePath() == False:
                            # write the file if not detected
                            logging.info("Adding a new fileContent at: {0}".format(newPath))
                            writenewfile.setFilepath(newPath)
                            writenewfile.writeNewFile(fileContent)
                            with FileModel() as filemodel:
                                filemodel.setUsername(request.session["username"])
                                filemodel.setFileName(requestCon["newname"])
                                filemodel.setHashCode(newMD5, newSHA1)
                                filemodel.updateFile(requestCon["oldname"])
                            # read the file again and verify it is hashed correctly
                            if filevalidator.verifyfileContent(newSHA1) == True:
                                shutil.rmtree(dirpath)
                                logging.info("Deleting the old fileContent at: {0}".format(completePath))

                                # write log
                                with FileActivityLog () as activitylog:
                                    activitylog.setUserID(userID)
                                    activitylog.setFileID(fileID)
                                    activitylog.setCurName(requestCon["newname"]+"/"+requestCon["oldname"])
                                    activitylog.setOwnerID(ownerID)
                                    activitylog.insertRename()

                                return HttpResponse(json.dumps(["success"]), content_type="application/json")
                            else:
                                logging.error("Something is weird about the provided: {0}".format(newPath))
                                return HttpResponse(json.dumps(["internalerror"]), content_type="application/json")
                        else:
                            return HttpResponse(json.dumps(["exist"]), content_type="application/json")
        else:
            return HttpResponse(json.dumps(["notlogin"]), content_type="application/json")