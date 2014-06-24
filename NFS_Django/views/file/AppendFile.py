#==========================================================================================================================
# import python modules
import logging
logging.basicConfig(level=logging.INFO)
import shutil
import json
import datetime
import pdb
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
# append class for handing copying file request from the client-side
class AppendFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        logging.info("Appending file...")
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
                    filemodel.setFileName(requestCon["filename"])
                    rows = filemodel.queryHashCode()
                    userid = filemodel.queryUserID()[0]
                    fileID = rows[3]

            else:
                ownerName = requestCon["owner"]
                with ShareFileModel() as sharefilemodel:
                    sharefilemodel.setFileAlias(requestCon["filename"])
                    sharefilemodel.setOwner(ownerName)
                    sharefilemodel.setSharedWith(request.session["username"])
                    fileID = sharefilemodel.queryShareFile_fileAlias()[1]

                with FileModel() as filemodel:
                    filemodel.setFileID(fileID)
                    rows = filemodel.queryFile_fileID()
                    filemodel.setUsername(request.session["username"])
                    userid = filemodel.queryUserID()[0]

            encrypt.setHashCode(rows[1], rows[2])
            completePath = encrypt.writePath("get")
            filevalidator.setfilePath(completePath)
            if filevalidator.verifyfileContent(rows[2]) == False:
                logging.error("Something is weird about the provided: {0}".format(completePath))
                return HttpResponse(json.dumps(["internalerror"]), content_type="application/json")
            else:
                readfile.setFilepath(completePath)
                fileContent = readfile.readFile()
                count = 1
                newName = requestCon["filename"]
                while rows != None:
                    with FileModel() as filemodel:
                        filemodel.setUsername(request.session["username"])
                        newName = requestCon["filename"][:-4] + " - Copy (" + str(count) + ").txt"
                        filemodel.setFileName(newName)
                        rows = filemodel.queryHashCode()
                    count += 1
                newMD5 = encrypt.creatMD5(newName, fileContent, userid)
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
                        filemodel.setFileName(newName)
                        filemodel.setUserID(userid)
                        filemodel.setHashCode(newMD5, newSHA1)
                        filemodel.insertFile()
                        newfileID = filemodel.queryFile()["ID"]

                    # write log
                    with FileActivityLog() as activitylog:
                        activitylog.setUserID(userid)
                        activitylog.setFileID(newfileID)
                        activitylog.setCurName(newName)
                        activitylog.insertCreate()

                    return HttpResponse(json.dumps(["success"]), content_type="application/json")
                else:
                    return HttpResponse(json.dumps(["exist"]), content_type="application/json")
        else:
            return HttpResponse(json.dumps(["notlogin"]), content_type="application/json")