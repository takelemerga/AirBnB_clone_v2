#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
       distributes an archive to your web servers
Returns False if the file at the path archive_path doesn't exist
"""
import os.path
import time
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import date
env.hosts = ['3.238.125.86', '3.237.33.25']


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


def do_deploy(archive_path):
    """ deploy webstatic"""
    if archive_path:
        """Upload the archive to the /tmp/ directory of the web server"""
        put(archive_path, "/tmp/")
        archive_file = archive_path.split("/")[-1]
        remove_ext = ("/data/web_static/releases/" +
                      archive_file.split(".")[0])
        run("sudo mkdir -p {:s}".format(remove_ext))

        """Uncompress the archive to the folder
        /data/web_static/releases/<archive filename without extension>
        on the web server"""
        run("sudo tar -xzf /tmp/{:s} -C {:s}".format(archive_file, remove_ext))

        """Delete the archive from the web server"""
        run("sudo rm /tmp/{:s}".format(archive_file))
        run("sudo mv {:s}/web_static/* {:s}/".format(remove_ext, remove_ext))
        run("sudo rm -rf {:s}/web_static".format(remove_ext))

        """Delete the symbolic link /data/web_static/current"""
        run('sudo rm -rf /data/web_static/current')

        """Create a new the symbolic link
           /data/web_static/current on the web server, linked to the new
           version of your code
           (/data/web_static/releases/<archive filename without extension>)"""
        run("sudo ln -s {:s} /data/web_static/current".format(remove_ext))
        return True
    else:
        return False


def deploy():
    """deploy"""
    try:
        my_archive_path = do_pack()
        deploythis = do_deploy(my_archive_path)
        return deploythis
    except:
        return False
