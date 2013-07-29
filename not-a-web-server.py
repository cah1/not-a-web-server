"""

Very simple decorator for SimpleHTTPServer.

Allow specific files to be served, and some special
files to be served with command hooks.

"""

import os
import urlparse
import SimpleHTTPServer
import SocketServer

HOST = "192.168.0.10" 
PORT = 80
SERVED_FILES = './proxy.pac', './wpad.dat'
SERVED_HOOKED_FILES = [{'/tools/sync-proxy-groups-from-google-groups':
                                               '/var/local/bin/syncproxygroups.py', }]               

class decorateSimpleHTTP(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        ParsedPath =  urlparse.urlparse(self.path)
        Path = ParsedPath.path
        if not os.access('.' + os.sep + Path, os.R_OK):
            self.send_response(404)
            return    
                
        if Path in SERVED_FILES:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        elif Path in SERVED_HOOKED_FILES.keys:
            if os.system(SERVED_HOOKED_FILES[Path]) == 0:
                if not os.access('.' + os.sep + Path, os.R_OK):
                    SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                else:
                    self.send_response(500) 
            else:
                self.send_response(500)
        else:
            # File found but not allowed.
            self.send_response(403)

decorator = decorateSimpleHTTP
httpd = SocketServer.TCPServer((HOST, PORT), decorator)
httpd.serve_forever()
