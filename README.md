Python-NFS
==========

A simple network file system implemented using python. Users can ending HTTP requests to NFS through RESTful API provided by server to add/delete/view/update hashed files stored in the network drive. Server handles those requests by calling the corresponding function through URL rewrite.

The main funtions:

server-only:

- set up configuration
- validate existing files 

client:

- login before manipulating data
- logout after manipulating data
- get infomation about the server
- handle requests of GET, POST, PUT and DELETE
