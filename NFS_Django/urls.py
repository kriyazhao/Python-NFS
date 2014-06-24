from django.conf.urls import patterns, include, url
from NFS_Django.views.user.CheckStatus import CheckStatus
from NFS_Django.views.user.Login import Login
from NFS_Django.views.user.Logout import Logout
from NFS_Django.views.user.Register import Register
from NFS_Django.views.user.RegisterExist import RegisterExist
from NFS_Django.views.user.EditUser import EditUser
from NFS_Django.views.user.ForgetPassword import * 
from NFS_Django.views.file.ListFile import ListFile
from NFS_Django.views.file.UploadFile import UploadFile
from NFS_Django.views.file.ViewFile import ViewFile
from NFS_Django.views.file.EditFile import EditFile
from NFS_Django.views.file.DeleteFile import DeleteFile
from NFS_Django.views.file.ShareFile import ShareFile
from NFS_Django.views.file.ShareExist import ShareExist
from NFS_Django.views.file.ShareOption import ShareOption
from NFS_Django.views.file.AppendFile import AppendFile
from NFS_Django.views.file.ExtractFile import ExtractFile
from NFS_Django.views.file.RenameFile import RenameFile
from NFS_Django.views.file.RenameExist import RenameExist
from NFS_Django.views.file.CreateExist import CreateExist 
from NFS_Django.views.file.CreateFile import CreateFile
from NFS_Django.views.file.ActivityLog import ActivityLog


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NFS_Django.views.home', name='home'),
    # url(r'^NFS_Django/', include('NFS_Django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^$','NFS_Django.views.index.index'),
	(r'^checklogin/$',CheckStatus.as_view()),
	(r'^register/$',Register.as_view()),
	(r'^registerexist/$',RegisterExist.as_view()),
	(r'^login/$',Login.as_view()),
	(r'^logout/$',Logout.as_view()),
	(r'^edituser/$',EditUser.as_view()),
	(r'^forgetpassword/$',ForgetPassword.as_view()),
	(r'^validatecode/$',ValidateCode.as_view()),
	(r'^resetpassword/$',ResetPassword.as_view()),
	(r'^listfile/$',ListFile.as_view()),
	(r'^uploadfile/$',UploadFile.as_view()),
	(r'^viewfile/$',ViewFile.as_view()),
	(r'^editfile/$',EditFile.as_view()),
	(r'^deletefile/$',DeleteFile.as_view()),
	(r'^sharefile/$',ShareFile.as_view()),
	(r'^shareexist/$',ShareExist.as_view()),
	(r'^shareoption/$',ShareOption.as_view()),
	(r'^appendfile/$',AppendFile.as_view()),
	(r'^extractfile/$',ExtractFile.as_view()),
	(r'^createexist/$',CreateExist.as_view()),
	(r'^createfile/$',CreateFile.as_view()),
	(r'^renamefile/$',RenameFile.as_view()),
	(r'^renameexist/$',RenameExist.as_view()),
	(r'^activitylog/$',ActivityLog.as_view())
)
