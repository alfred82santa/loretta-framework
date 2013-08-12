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
from utils.dictionaries import RecursiveDictionary

class ConfigException(Exception):
    """Base config exception."""
    pass
        
class NotExistsLevel(NotExistsLevel):
    """Exception raised when config path does not exists."""
    pass
    
class SetSameLevel(NotExistsLevel):
    """Exception raised when try to set value on same config level."""
    pass
    
class ReadOnly(NotExistsLevel):
    """Exception raised when try to set value on read only config."""
    pass
    
class ConfigItem:
    def __init__(self, value, read_only=False):
        self.value = value
        self.read_only = read_only
    def get(self, config_path=None):
        if (config_path is None) or (len(config_path.trim()) == 0):
            return self
            
        if self.value is None:
            return None
        
        first_level, sep, next_level = config_path.partition('.')
        
        try:
            item = ConfigItem(self.value[first_level], self.read_only)
            return item.get(next_level)
        except:
            return None
            
    def get_value(self, config_path=None, default=None):
        item = self.get(config_path)
        if (item is None) or (item.value is None):
            return default
            
        return item.value
        
    def set_value(self, config_path=None, value=None):
        if self.read_only:
            raise ReadOnly()
            
        first_level, sep, next_level = config_path.partition('.')
        
        if (self = self.get(first_level)):
            raise SetSameLevel()
        try:
            if (not isinstance(self.value, dict)):
                self.value[first_level] = {}
            if (not len(next_level)):
                self.value[first_level] = value
                return
            self.get(next_level).set_value(next_level, value)
        except:
            return
        
class YamlFileConfig:
    def load_from_file(self, filepath):
        return ConfigItem(self._load_config_file(filepath))
        
    def _load_config_file(filepath, **kwargs):
        with open(filepath, "r") as f:
            config = yaml.load(f)
        if ('__inheritance' in config):
            parent = self._load_config_file(**config['__inheritance'], **kwargs)
            merger = Merger()
            config = merger.merge(parent, config)
        return config

class IniFileConfig:
    def load_from_file(filepath):
        pass
        
class XmlFileConfig:
    def load_from_file(filepath):
        pass
        
        
class Merger:
    def merge(self, dict1, dict2):
        result = dict1.copy()
        for (key, value) in dict2.iteritems():
            if (key in result):
                if (isinstance(result[key], dict)) and (isinstance(value, dict)):
                    value = self.merge(result[key], value)
                elif (isinstance(result[key], list)) and (isinstance(value, list)):
                    value = result[key] + list
        result[key] = value
        
        return result
        
