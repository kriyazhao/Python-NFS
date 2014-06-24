#==========================================================================================================================
# import python modules
from django.http import HttpResponse
from django.views.generic import View
import json
#==========================================================================================================================
# CheckStatus class check user's login status
class CheckStatus(View):

    def get(self, request):
        if "username" not in request.session:
            request.META["CSRF_COOKIE_USED"] = True    
            return HttpResponse(json.dumps({'r':0}), content_type="application/json")
        else:
            request.META["CSRF_COOKIE_USED"] = True    
            return HttpResponse(json.dumps({'r':1,'un':request.session["username"]}), content_type="application/json")
