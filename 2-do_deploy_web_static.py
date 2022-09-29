#!/usr/bin/python3
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['3.238.125.86', '3.237.33.25']


def do_deploy(archive_path):
    """deploy webstatic"""
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
