# This file is part of Loretta Framework.  Loretta Framework is free software: 
# you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Loretta Framework Team Members

import yaml;
from gevent import pywsgi

EXTENSION_CLASS_NAME = "Extension"

class LorettaApplication():
    config_file = ""
    resources = []
    middlewares = []
    routes = []
    extensions = []
    
    def __init__(self, config_file=None):
    
        if (config_file is not None):
            self.config_file = config_file
            
        self.load_config(self.config_file)
        
        self.load_extensions()
        self.start_server()
        
        
    def load_config(self, filepath):
        stream = open(filepath, "r")
        self.config = yaml.load(stream)
        stream.close()
        
    def load_extensions(self):
        for ext in self.config['extensions']:
            module_name = ext['module']
            module = __import__(module_name)
            class_ = getattr(module, EXTENSION_CLASS_NAME)
            instance = class_(self, ext)
            self.extensions[] = instance
            if (ext['autoload']):
                instance.load()
            
    def start_server(self):
        pool = Pool(10000)
        self.server = pywsgi.WSGIServer(('', 8080), self._init_request, spawn=pool)
        self.server.serve_forever()
        
    def _init_request(environ, start_response):
        pass
        
            
            
        
        
