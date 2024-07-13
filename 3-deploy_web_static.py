#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""

from fabric.api import run, put, env, local
from datetime import datetime
import os

env.hosts = ['54.196.29.210', '54.87.217.94']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']
env.output_prefix = False  # Enable verbose output


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if not os.path.exists("versions"):
        os.makedirs("versions")
    result = local("tar -cvzf {} web_static".format(file))
    if result.failed:
        return None
    return file


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers, and deploys it.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    remote_path = "/tmp/{}".format(file_name)

    try:
        # Upload archive to /tmp/ directory of the web server
        put(archive_path, remote_path)

        # Create necesary directories
        run("mkdir -p /data/web_static/releases/{}/".format(file_name_no_ext))

        # Extract archive and update contents
        run("tar -xzf {} -C /data/web_static/releases/{}/".format(
            remote_path, file_name_no_ext))
        run("rm {}".format(remote_path))
        mv_arg1 = "mv /data/web_static/releases/{}/web_static/*"
        mv_arg2 = "/data/web_static/releases/{}/"
        mv_args = mv_arg1 + " " + mv_arg2
        run(mv_args.format(file_name_no_ext, file_name_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static".
            format(file_name_no_ext)
            )

        # Clean up
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(file_name_no_ext)
            )
        print("New version deployed!")

        return True

    except Exception as e:
        print("Error occured: {}".format(e))
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
