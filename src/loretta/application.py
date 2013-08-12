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
from config import YamlFileConfig

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
        loader = YamlFileConfig()
        self.config = loader.load_from_file(filepath)
        
    def load_extensions(self):
        for ext in self.config.get('extensions'):
            module_name = ext.get_value('module')
            module = __import__(module_name)
            class_name = ext.get_value('classname', EXTENSION_CLASS_NAME)
            class_ = getattr(module, class_name)
            instance = class_(self, ext)
            self.extensions[] = instance
            if (ext.get_value('autoload', True):
                instance.load()
            
    def start_server(self):
        pool = Pool(self.config.get_value('server.maxConnections', 100))
        self.server = pywsgi.WSGIServer(('', \
                             self.config.get_value('server.port', 8080)), \
                             self._init_request, \
                             spawn=pool)
        self.server.serve_forever()
        
    def _init_request(environ, start_response):
        pass
        
            
            
        
        
