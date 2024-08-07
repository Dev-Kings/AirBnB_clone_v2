#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""

from fabric.api import run, put, env
import os


env.hosts = ['54.196.29.210', '54.87.217.94']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']
env.output_prefix = False  # Enable verbose output


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
        run('mkdir -p /data/web_static/current')

        # Extract archive and update contents
        run("tar -xzf {} -C /data/web_static/releases/{}/".format(
            remote_path, file_name_no_ext))
        mv_arg1 = "mv /data/web_static/releases/{}/web_static/*"
        mv_arg2 = "/data/web_static/releases/{}/"
        mv_args = mv_arg1 + " " + mv_arg2
        run(mv_args.format(file_name_no_ext, file_name_no_ext))

        # Clean up
        run("rm {}".format(remote_path))
        run("rm -rf /data/web_static/releases/{}/web_static".
            format(file_name_no_ext)
            )
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(file_name_no_ext)
            )
        print("New version deployed!")

        return True

    except Exception as e:
        print(e)
        return False
