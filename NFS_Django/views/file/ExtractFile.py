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
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel 
from NFS_Django.views.model.FileActivityLog import FileActivityLog
from NFS_Django.views.util.MD5Validator import MD5Validator

#==========================================================================================================================
# ExtractFile class for extracting files given md5 and sha1 codes
class ExtractFile(View):
    
    def post(self, request):
        if "username" in request.session:
            requestCon = json.loads(request.body)
            md5validator = MD5Validator(requestCon["md5"])
            if md5validator.MD5Validate() == True:
                with FileModel() as filemodel:
                    filemodel.setHashCode(requestCon["md5"], requestCon["sha1"])
                    rows = filemodel.queryFile()
                    fileID = rows["ID"]
                    ownerID = rows["userID"]
                    filemodel.setUserID(ownerID)
                    ownerName = filemodel.queryUsername()[0]
                    filemodel.setUsername(request.session["username"])
                    userID = filemodel.queryUserID()[0]

                if rows == None:
                    return HttpResponse(json.dumps(['notfound']), content_type="application/json")
                else:
                    with ShareFileModel() as sharefilemodel:
                        sharefilemodel.setFileID(rows["ID"])
                        sharefilemodel.setOwner(ownerName)
                        sharefilemodel.setSharedWith(request.session["username"])
                        logging.info(rows["ID"])
                        logging.info(ownerName)
                        logging.info(request.session["username"])
                        sharefile = sharefilemodel.queryShareFile()
                        sharefilemodel.setFileAlias(rows["filename"])
                        if sharefile == None: # not found in the sharefile table
                            if ownerName == request.session["username"]:
                                return HttpResponse(json.dumps(["owner"]), content_type="application/json")
                            if rows["privilege"] == "11" or rows["privilege"] == "12":
                                if rows["privilege"] == "11":
                                    sharefilemodel.setPrivilege(11)
                                    sharefilemodel.insertShareFile()
                                elif rows["privilege"] == "12":
                                    sharefilemodel.setPrivilege(12)
                                    sharefilemodel.insertShareFile()
                                shareDict={}
                                shareDict["fileAlias"] = rows["filename"]
                                shareDict["owner"] = ownerName
                                shareDict["privilege"] = rows["privilege"]

                                #write log
                                with FileActivityLog() as activitylog:
                                    activitylog.setUserID(userID)
                                    activitylog.setFileID(fileID)
                                    activitylog.setCurName(rows["filename"])
                                    activitylog.setOwnerID(ownerID)
                                    activitylog.insertExtract()

                                return HttpResponse(json.dumps([shareDict]), content_type="application/json")
                            elif rows["privilege"] == "2" or rows["privilege"] == "0":
                                return HttpResponse(json.dumps(['restricted']), content_type="application/json")
                        else: # found in the sharefile table
                            if sharefile[6] == 1:
                                sharefilemodel.setPrivilege(sharefile[5])
                                sharefilemodel.updateShareFile()
                                shareDict={}
                                shareDict["fileAlias"] = sharefile[2]
                                shareDict["owner"] = ownerName
                                shareDict["privilege"] = sharefile[5]

                                #write log
                                with FileActivityLog() as activitylog:
                                    activitylog.setUserID(userID)
                                    activitylog.setFileID(fileID)
                                    activitylog.setCurName(rows["filename"])
                                    activitylog.insertExtract()

                                return HttpResponse(json.dumps([shareDict]), content_type="application/json")
                            else:
                                return HttpResponse(json.dumps(['exist']), content_type="application/json")
                    logging.info("1 file is found: {0}".format(sharefile))
            else:
                return HttpResponse(json.dumps(['notvalid']), content_type="application/json")
        else:
            return HttpResponse(json.dumps(['notlogin']), content_type="application/json")
