import json
import logging
logging.basicConfig(level=logging.INFO)
from django.http import HttpResponse
from django.views.generic import View

#==========================================================================================================================
# Logout class handles get request of logout
class Logout(View):

    def get(self,request):
        if "username" in request.session:
            del request.session["username"]
            logging.info("successfully logout")
            return HttpResponse(json.dumps({'r':'1'}), content_type="application/json") # successfully logout
        else:
            return HttpResponse(json.dumps({'r':'0'}), content_type="application/json") # already logout
            