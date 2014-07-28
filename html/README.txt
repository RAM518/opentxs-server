to run the Admin Panel with python functionality, go to the directory
where the html/ admin folder resides, in the command terminal type:

chmod +x python_service.py
python ./python_service.py 8000 

This will serve ONLY to localhost, by calling this script.
then open a browser to: localhost:8000/index.html
to view the admin panel interface. Change port number if you wish.
allow scripts on localhost for javascript functionality

You can also serve to the WEB, by simply calling
python -m SimpleHTTPServer 8080
to serve on port 8080 for example.

(dependency)
cd js/
wget http://code.jquery.com/jquery-2.1.0.min.js


