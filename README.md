Python-NFS
==========

A simple network file system implemented using jquery/ajax + python + webpy + mySQL. It allows clients to register/login to manage files online by sending HTTP requests to NFS through RESTful API provided by server. Server handles those requests by calling the corresponding function through URL rewrite. 

Clients can extract, add, view, edit, delete, share files. auto sync of any change to the file will be done everytime user finish typing. In terms of file security, file path and file name are encrypted to keep user's confidentiality.
