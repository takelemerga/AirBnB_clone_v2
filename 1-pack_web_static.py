#!/usr/bin/python3
"""
All files in the folder web_static must be added to the final archive
All archives must be stored in the folder versions
(your function should create this folder if it doesn't exist)
The name of the archive created must be
web_static_<year><month><day><hour><minute><second>.tgz
The function do_pack must return the archive path
if the archive has been correctly generated
Otherwise, it should return None
"""
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['localhost']


def do_pack():
    """pack files in webstatic"""
    try:
        fpath = "versions/web_static_" + datetime.now().\
                   strftime("%Y%m%d%H%M%S") + ".tgz"
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_$(date +%Y%m%d%H%M%S).tgz\
        web_static")
        return ("web_static packed: {} -> {}".
                format(fpath, os.path.getsize(fpath)))
    except:
        return None
