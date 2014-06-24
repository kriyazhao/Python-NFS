
class UploadifyMiddleware(object):

    def process_request(self, request):
        if (request.method == 'POST') and (request.path == '/uploadfile/') and \
                request.COOKIES.has_key('csrftoken'):
            request.META["HTTP_X_CSRFTOKEN"] = request.COOKIES['csrftoken']

