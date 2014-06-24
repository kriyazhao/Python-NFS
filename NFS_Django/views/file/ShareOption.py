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
from NFS_Django.views.util.UserValidator import UserValidator
from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel
from NFS_Django.views.model.FileActivityLog import FileActivityLog

#==========================================================================================================================
# ShareOption class for setting share options
class ShareOption(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        if "username" in request.session:
            requestCon = json.loads(request.body)
            if "privilege" in requestCon: # anyone can share
                ownerName = requestCon["owner"]
                with FileModel() as filemodel:
                    filemodel.setUsername(ownerName)
                    filemodel.setFileName(requestCon["filename"])
                    rows = filemodel.queryHashCode()
                    filemodel.setUsername(request.session["username"])
                    userID = filemodel.queryHashCode()[0]
                    if rows != None:
                        ownerID = rows[0]
                        fileID = rows[3]
                if rows == None:
                    return HttpResponse("notfound", content_type = "text/plain")
                else:
                    with FileModel() as filemodel: # change file privilege
                        filemodel.setUsername(ownerName)
                        filemodel.setFileName(requestCon["filename"])
                        if requestCon["privilege"] == 11: # anyone can view
                            filemodel.updateShareOption(11)
                        elif requestCon["privilege"] == 12: # anyone can edit
                            filemodel.updateShareOption(12)

                    # write log
                    with FileActivityLog() as activitylog:
                        activitylog.setUserID(userID)
                        activitylog.setFileID(fileID)
                        activitylog.setCurName(requestCon["filename"])
                        activitylog.setOwnerID(ownerID)
                        activitylog.setSharedwithID(0)
                        if requestCon["privilege"] == 11: # anyone can view
                            activitylog.setSharedPrvlg(11)
                        elif requestCon["privilege"] == 12: # anyone can edit
                            activitylog.setSharedPrvlg(12)
                        activitylog.insertShare()

                    return HttpResponse("success", content_type = "text/plain")
            else: # someone can share
                ownerName = requestCon[1]["un"]
                with FileModel() as filemodel:
                    filemodel.setUsername(ownerName)
                    filemodel.setFileName(requestCon[0])
                    rows = filemodel.queryHashCode()
                    ownerID = rows[0]
                    filemodel.setUsername(request.session["username"])
                    userID = filemodel.queryUserID()[0]

                if rows == None:
                    return HttpResponse("notfound", content_type = "text/plain")
                else:
                    with FileModel() as filemodel: # change file privilege
                        filemodel.setUsername(ownerName)
                        filemodel.setFileName(requestCon[0])
                        fileID = filemodel.queryHashCode()[3]

                        if len(requestCon) == 2:
                            filemodel.updateShareOption(0)
                        else:
                            filemodel.updateShareOption(2)
                    if len(requestCon) > 2: # add/update share members, requestCon[1] is the owner
                        sharelist = ()
                        for member in requestCon[2:]: 
                            sharelist = sharelist + (member["un"],)
                            with ShareFileModel() as sharefilemodel:
                                sharefilemodel.setOwner(ownerName)
                                sharefilemodel.setSharedWith(member["un"])
                                sharefilemodel.setFileID(fileID)
                                sharefilemodel.setFileAlias(requestCon[0])
                                sharefilemodel.setPrivilege(member["privilege"])
                                shareRecord = sharefilemodel.queryShareFile()
                                if shareRecord == None:
                                    sharefilemodel.insertShareFile()
                                else:
                                    sharefilemodel.updateShareFile()

                            with FileModel() as filemodel:
                                filemodel.setUsername(member["un"])
                                sharedwithID = filemodel.queryUserID()[0]

                            # write log
                            with FileActivityLog() as activitylog:
                                activitylog.setUserID(userID)
                                activitylog.setFileID(fileID)
                                activitylog.setCurName(requestCon[0])
                                activitylog.setOwnerID(ownerID)
                                activitylog.setSharedwithID(sharedwithID)
                                activitylog.setSharedPrvlg(member["privilege"])
                                activitylog.insertShare()

                        with ShareFileModel() as sharefilemodel: # delete old share members
                            sharefilemodel.setOwner(ownerName)
                            sharefilemodel.setFileID(fileID)
                            desharelist = sharefilemodel.deleteSharedWith(sharelist)

                        for item in desharelist:
                            # write log
                            with FileActivityLog() as activitylog:
                                activitylog.setUserID(userID)
                                activitylog.setFileID(item["fileID"])
                                activitylog.setCurName(requestCon[0])
                                activitylog.setOwnerID(ownerID)
                                activitylog.setSharedwithID(item["sharedwithID"])
                                activitylog.setSharedPrvlg(item["privilege"])
                                activitylog.insertDeletedShare()

                    else:
                        with ShareFileModel() as sharefilemodel: # delete old share members
                            sharefilemodel.setOwner(ownerName)
                            sharefilemodel.setFileID(fileID)
                            desharelist = sharefilemodel.deleteSharedWith_owner()

                        for item in desharelist:
                            # write log
                            with FileActivityLog() as activitylog:
                                activitylog.setUserID(userID)
                                activitylog.setFileID(item["fileID"])
                                activitylog.setCurName(requestCon[0])
                                activitylog.setOwnerID(ownerID)
                                activitylog.setSharedwithID(item["sharedwithID"])
                                activitylog.setSharedPrvlg(item["privilege"])
                                activitylog.insertDeletedShare()

                    return HttpResponse("success", content_type = "text/plain")
        else:
            return HttpResponse("notlogin", content_type = "text/plain")