#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE
import re
import os

# these file types will NOT be tracked as lfs, i.e. source code files:
non_lfs_extensions = ['cs', 'txt', 'py', 'py', 'cpp', 'h', 'hpp', 'bat', 'sh', 'json', 'yaml', 'xml', 'strings', 'meta',
                      'CS', 'TXT', 'PY', 'PY', 'CPP', 'H', 'HPP', 'BAT', 'SH', 'JSON', 'YAML', 'XML', 'STRINGS', 'META',
                      'unity', 'prefab', 'controller', 'mat', 'renderTexture', 'flare', 'anim', 'asset',
                      'gitignore', 'gitattributes']

status_cmd = ['git', 'status', '--porcelain']
added_file_flags = [' A ', 'A ', 'M ', ' M ', '??']
git_reset_cmd = ['git', 'reset']
git_add_cmd = ['git', 'add']
added_changed_attributes_cmd = ['git', 'add', '.gitattributes']
files_to_be_tracked_as_lfs = []


def track():
    git_status = Popen(status_cmd, stdout=PIPE, stderr=PIPE)
    git_status_result = git_status.stdout.readlines()

    for line in git_status_result:
        line = line[:-1]
        file_name_index = line.rfind(' ')
        file_name = line[file_name_index+1:]
        for file_flag in added_file_flags:

            if not line.startswith(file_flag):
                continue

            file_is_lfs = True
            
            for ext in non_lfs_extensions:
                rgx = r'.*\.%s$' % ext
                if re.match(rgx, file_name):
                    file_is_lfs = False

            print 'file_is_lfs:', file_is_lfs
                    
            if file_is_lfs:
                try:
                    _track_as_lfs(file_name)
                except Exception as e:
                    print "LFS tracking failed: "
                    print e
    
    if 0 < len(files_to_be_tracked_as_lfs):
        subprocess.check_call(added_changed_attributes_cmd)


def _track_as_lfs(file_name):
    
    file_split = file_name.split('.')

    if len(file_split) > 1:
        file_name = '"*.%s"' % file_split[-1]

    print "LFS Tracking: " + file_name
    files_to_be_tracked_as_lfs.append(file_name)

    reset_cmd = git_reset_cmd + [file_name]
    lfs_cmd = 'git --work-tree "' + os.getcwd() + '" lfs track ' + file_name
    add_cmd = git_add_cmd + [file_name]

    subprocess.check_call(reset_cmd)
    subprocess.check_call(lfs_cmd, shell=True)
    subprocess.check_call(add_cmd)


if __name__ == "__main__":
    print "LFS tracking hook started"
    try:
        track()
    except Exception as e:
        print "LFS tracking hook failed: "
        print e
        exit(1)
    
    print "LFS tracking hook ended"
    exit(0)
