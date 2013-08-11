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
            if (self.value is not dict):
                self.value[first_level] = {}
            if (not len(next_level)):
                self.value[first_level] = value
                return
            self.get(next_level).set_value(next_level, value)
        except:
            return
        
class YamlFileConfig:
    def load_from_file(filepath):
        pass

class IniFileConfig:
    def load_from_file(filepath):
        pass
        
class XmlFileConfig:
    def load_from_file(filepath):
        pass
        
