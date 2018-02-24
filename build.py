"""
Package application using zipapp into an executable zip archive
"""
import os
import zipapp

INTERPRETER = '/usr/bin/env python3'
SOURCE_PATH = 'dsst'
TARGET_FILENAME = 'dsst'

# The bundled file should be placed into the build directory
target_path = os.path.join(os.path.dirname(__file__), 'build')
# Make sure it exists
if not os.path.isdir(target_path):
    os.mkdir(target_path)
target = os.path.join(target_path, TARGET_FILENAME)
# Create archive
zipapp.create_archive(source=SOURCE_PATH, target=target, interpreter=INTERPRETER)
