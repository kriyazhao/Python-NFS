#==========================================================================================================================
# import python modules
import logging, argparse, ConfigParser
import web, os, platform, ctypes
import hashlib
import shutil
import json

#==========================================================================================================================
# info class for displaying server infomation.
class info:
    global myConfig, fileCount, session
    
    # GET function responds to request.get method from the client-side
    def GET(self, paramStr = None):
        
        path = myConfig.getDataDir()
        # if /info/fileValidator is called, run the fileValidator function.
        if(paramStr == 'validateFiles'):
            fileCount = fileValidator(path)
        info = {'fileCount': fileCount}
        info['free'], info['freeNonSuper'], info['total'] = self.diskSpace(path)
        try:
            info['percFreeNoneSuper'] = 100 * (float(info['freeNonSuper']) / info['total'])
        except ZeroDivisionError:
            info['percFreeNoneSuper'] = 0
        logging.info("Total: {0}\nFree: {1}\nFreeNonSuper: {2}\npercFreeNonSuper: {3}".format(info['total'], info['free'], info['freeNonSuper'], info['percFreeNoneSuper']))
        web.header('Content-Type', 'application/json')
        return json.dumps(info)

    # diskSpace function to get free space and total space information (in megabytes)
    def diskSpace(self, path):
        free = 0
        freeNonSuper = 0
        total = 0
        print "diskSpace({0}): platform = {1}".format(path, platform.system())
        # if the platform is Windows
        if platform.system() == 'Windows':
            free = ctypes.c_ulonglong(0)
            freeNonSuper = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            # "total" here is the total space available to the user, not total space on the disk.
            # the server used for testing the program is a 64-bit system
            ctypes.windll.kernel64.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path),
                                                       ctypes.pointer(freeNonSuper),
                                                       ctypes.pointer(total),
                                                       ctypes.pointer(free))
            return (free.value/1024/1024, freeNonSuper.value/1024/1024, total.value/1024/1024)
        else:
            stat = os.statvfs(path)
            free = stat.f_bfree * stat.f_frsize
            freespfreeNonSuper = stat.f_bavail * stat.f_frsize
            total = stat.f_blocks * stat.f_frsize
            return (free/1024/1024, freeNonSuper/1024/1024, total/1024/1024)
        
