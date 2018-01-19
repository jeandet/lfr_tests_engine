#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2016, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

import os
import configparser

CONFIG_DIR = os.path.expanduser('~') + '/.lfrcompliance/'
CONFIG_FILE = CONFIG_DIR + 'lfrcompliance.ini'

if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)
if not os.path.exists(CONFIG_FILE):
    open(CONFIG_FILE, "w").close()

_config = configparser.ConfigParser()
_config.sections()
_config.read(CONFIG_FILE)


def save_conf():
    configfile = open(CONFIG_FILE, 'wt')
    _config.write(configfile)


def get_value(section, key):
    if not _config.has_section(section):
        _config.add_section(section)
    return _config[section].get(key)


def set_value(section, key, value):
    if not _config.has_section(section):
        _config.add_section(section)
    _config[section][key] = value
    save_conf()


def has_key(section, key):
    if not _config.has_section(section):
        return False
    if _config[section].get(key) is None:
        return False
    return True
