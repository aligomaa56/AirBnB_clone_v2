#!/usr/bin/python3
"""Fabric script that Generates a .tgz archive"""
from fabric.api import *
from datetime import datetime
import os
from fabric.contrib.files import exists


env.hosts = ['54.84.254.93', '34.229.71.191']
env.user = 'ubuntu'


def do_pack():
    '''Packs the contents of the web_static folder into a .tgz archive'''
    now = datetime.now()
    datetime_format = '%Y%m%d%H%M%S'
    formatted_time = now.strftime(datetime_format)
    archive_path = 'versions/web_static_{}.tgz'.format(formatted_time)

    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static'.format(
        archive_path), capture=True)

    if result.failed:
        print('Failed to pack web_static')
        return None

    archive_size = os.path.getsize(archive_path)
    print('web_static packed: {} -> {}Bytes'.format(archive_path,
                                                    archive_size))
    return archive_path


def do_deploy(archive_path):
    '''Deploy archive to web server'''
    if not archive_path:
        return False

    if not os.path.exists(archive_path):
        print('Archive path does not exist:', archive_path)
        return False

    file_name = os.path.basename(archive_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    target_path = '/data/web_static/releases/{}'.format(file_name_no_ext)

    # Upload the archive to the remote server
    put(archive_path, '/tmp/', use_sudo=True)

    # Create the target directory
    if not exists(target_path):
        sudo('mkdir -p {}'.format(target_path))

    # Extract the archive into the target directory
    with cd(target_path):
        sudo('tar -xzf /tmp/{} -C {}'.format(file_name, target_path))

    # Remove the uploaded archive from the remote server
    sudo('rm /tmp/{}'.format(file_name))

    # Move the contents of the extracted archive to the target directory
    sudo('mv {}/web_static/* {}/'.format(target_path, target_path))

    # Remove the web_static directory from the target directory
    sudo('rm -rf {}/web_static'.format(target_path))

    # Remove the current symlink if it exists
    sudo('rm -rf /data/web_static/current')

    # Create a new symlink to the latest release
    sudo('ln -s {} /data/web_static/current'.format(target_path))

    print('New version deployed!')
    return True


def deploy():
    '''Create and distribute an archive to web servers'''
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
