#==========================================================================================================================
# import python modules
import json
import datetime
import logging
logging.basicConfig(level=logging.INFO)

from django.views.generic import View
from django.http import HttpResponse

from NFS_Django.views.model.FileModel import FileModel
from NFS_Django.views.model.ShareFileModel import ShareFileModel
from NFS_Django.views.model.FileActivityLog import FileActivityLog

class ActivityLog(View):

    def get(self, request):
        if "username" in request.session:
            viewType = int(request.GET.get("type"))
            with FileModel() as filemodel:
                filemodel.setUsername(request.session["username"])
                userID = filemodel.queryUserID()[0]
            with FileActivityLog() as activitylog:
                activitylog.setUserID(userID)
                rows = activitylog.queryLog(viewType)
            logging.info(rows)
            resultlist = []
            for item in rows:
                resultDict = {}
                resultDict["action"] = item[7]
                resultDict["curName"] = item[3]

                todayTime = datetime.datetime.today()
                todayMid = datetime.datetime(todayTime.year, todayTime.month, todayTime.day, 0,0,0)
                timeDiff1 = datetime.timedelta(days=1)
                if item[8]  > todayMid:
                    resultDict["date"] = "Today " + str(item[8])[11:16]
                elif todayMid > item[8] and (todayMid - item[8]) < timeDiff1:
                    resultDict["date"] = "Yest " + str(item[8])[11:16]
                elif (todayMid - item[8]) > timeDiff1:
                    resultDict["date"] = str(item[8])[5:10]

                if item[1] == userID: # owner 
                    if item[5] != None:
                        with FileModel() as filemodel:
                            if item[5] == 0:
                                sharedName = "Anyone"
                            elif item[5] == userID:
                                sharedName = "You"
                            else:
                                filemodel.setUserID(item[5])
                                sharedName = filemodel.queryUsername()[0]
                        resultDict["sharedwithID"] = sharedName 
                        if item[6] in [11,21]:
                            resultDict["privilege"] = "can view"
                        elif item[6] in [12,22]:
                            resultDict["privilege"] = "can edit/view"
                else:
                    with FileModel() as filemodel:
                        filemodel.setUserID(item[1])
                        userName = filemodel.queryUsername()[0]
                        resultDict["notself"] = userName
                        if item[5] != None:
                            if item[5] == 0:
                                sharedName = "Anyone"
                            else:
                                filemodel.setUserID(item[5])
                                sharedName = filemodel.queryUsername()[0]
                            resultDict["sharedwithID"] = sharedName 
                            if item[6] in [11,21]:
                                resultDict["privilege"] = "can view"
                            elif item[6] in [12,22]:
                                resultDict["privilege"] = "can edit/view"
                resultlist.append(resultDict)

            return HttpResponse(json.dumps(resultlist), content_type = "application/json")
        else:
            return HttpResponse(json.dumps(["notlogin"]), content_type = "application/json")