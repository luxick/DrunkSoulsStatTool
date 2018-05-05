"""
Package application using zipapp into an executable zip archive
"""
import os
import zipapp
import sys

import shutil

INTERPRETER = '/usr/bin/env python3'

CLIENT_VERSION = '0.2'
SERVER_VERSION = '0.2'

try:
    build_mode = sys.argv[1]
except IndexError:
    print('No build mode specified')
    sys.exit(0)

print('Building Mode: {}'.format(build_mode))

path = os.path.dirname(__file__)
# Specify build path
BUILD_PATH = os.path.join(path, 'build')
# Make sure it exists
if not os.path.isdir(BUILD_PATH):
    os.mkdir(BUILD_PATH)


def build(target_filename, folder_name, entry_point):
    source_path = os.path.join(BUILD_PATH, 'source')
    if os.path.isdir(source_path):
        shutil.rmtree(source_path)
    os.mkdir(source_path)
    shutil.copytree(os.path.join(path, 'dsst', folder_name), os.path.join(source_path, folder_name))
    shutil.copytree(os.path.join(path, 'dsst', 'common'), os.path.join(source_path, 'common'))
    archive_name = os.path.join(BUILD_PATH, target_filename)
    zipapp.create_archive(source=source_path, target=archive_name, interpreter=INTERPRETER,
                          main=entry_point)
    print('Created {}'.format(archive_name))
    shutil.rmtree(source_path)


def build_server():
    build('dsst-server-{}'.format(SERVER_VERSION), 'dsst_server', 'dsst_server.server:main')


def build_gtk3():
    build('dsst-gtk3-{}'.format(CLIENT_VERSION), 'dsst_gtk3', 'dsst_gtk3.gtk_ui:main')


build_modes = {
    'server': build_server,
    'gtk3': build_gtk3
}

if build_mode == 'all':
    for mode, build_function in build_modes.items():
        build_function()
else:
    build_modes[build_mode]()