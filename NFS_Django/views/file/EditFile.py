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
from NFS_Django.views.model.FileActivityLog import FileActivityLog

#==========================================================================================================================
# EditFile class for handing post request from the client-side
class EditFile(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        readfile = FileNotepad()
        writenewfile = FileNotepad()
        filevalidator = FileValidator()
        encrypt = EncryptionPath()

        if "username" in request.session:
            requestCon = json.loads(request.body)
            if requestCon["owner"] == "Yourself":
                ownerName = request.session["username"]
            else:
                ownerName = requestCon["owner"]

            with FileModel() as filemodel:
                filemodel.setUsername(ownerName)
                filemodel.setFileName(requestCon["filename"])
                rows = filemodel.queryHashCode()
                fileID  = rows[3]
                ownerID  = rows[0]
                filemodel.setUsername(request.session["username"])
                userID = filemodel.queryUserID()[0]
            if rows == None:
                return HttpResponse("notfound", content_type="text/plain")
            else:
                encrypt.setHashCode(rows[1], rows[2])
                completePath = encrypt.writePath("get")
                dirpath = encrypt.writePath("delete")
                filevalidator.setfilePath(completePath)
                if filevalidator.verifyfileContent(rows[2]) == False:
                    logging.error("Something is weird about the provided: {0}".format(completePath))
                    return HttpResponse("internalerror", content_type="text/plain")
                else:
                    newMD5 = encrypt.creatMD5(requestCon["filename"], requestCon["content"], rows[0])
                    newSHA1 = encrypt.creatSHA1(requestCon["content"])
                    logging.info("newMD5: {0}".format(newMD5))
                    logging.info("newSHA1: {0}".format(newSHA1))
                    newPath = encrypt.writePath("get")
                    filevalidator.setfilePath(newPath)
                    if filevalidator.verifyfilePath() == False:
                        # write the file if not detected
                        logging.info("Adding a new fileContent at: {0}".format(newPath))
                        writenewfile.setFilepath(newPath)
                        writenewfile.writeNewFile(requestCon["content"])
                        with FileModel() as filemodel:
                            filemodel.setUsername(ownerName)
                            filemodel.setFileName(requestCon["filename"])
                            filemodel.setHashCode(newMD5, newSHA1)
                            filemodel.updateFile()

                        # read the file again and verify it is hashed correctly
                        if filevalidator.verifyfileContent(newSHA1) == True:
                            shutil.rmtree(dirpath)
                            logging.info("Deleting the old fileContent at: {0}".format(completePath))

                            # write log
                            with FileActivityLog() as activitylog:
                                activitylog.setUserID(userID)
                                activitylog.setFileID(fileID)
                                activitylog.setCurName(requestCon["filename"])
                                activitylog.setOwnerID(ownerID)
                                activitylog.insertEdit()

                            return HttpResponse("success", content_type="text/plain")
                        else:
                            logging.error("Something is weird about the provided: {0}".format(newPath))
                            return HttpResponse("internalerror", content_type="text/plain")
                    else:
                        return HttpResponse("exist", content_type="text/plain")
        else:
            return HttpResponse("notlogin", content_type="text/plain")