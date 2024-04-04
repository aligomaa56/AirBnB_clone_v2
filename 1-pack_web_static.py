#!/usr/bin/python3
"""Fabric script that Generates a .tgz archive"""
from fabric.api import local
from datetime import datetime
import os


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
