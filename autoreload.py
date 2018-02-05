#!/usr/bin/env python
import os
import sys
import subprocess
import time


def file_filter(name):
    return (not name.startswith(".")) and (not name.endswith(".swp"))


def file_times(path):
    for top_level in filter(file_filter, os.listdir(path)):
        for root, dirs, files in os.walk(top_level):
            for file in filter(file_filter, files):
                yield os.stat(os.path.join(root, file)).st_mtime


def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print(stdout)


def print_stderr(process):
    stderr = process.stderr
    if stderr != None:
        print(stderr)


# We concatenate all of the arguments together, and treat that as the command to run
command = ' '.join(sys.argv[1:])

# The path to watch
path = '.'

# How often we check the filesystem for changes (in seconds)
wait = 1

# The process to autoreload
process = subprocess.Popen(command, shell=True)

# The current maximum file modified time under the watched directory
last_mtime = max(file_times(path))
max_mtime = last_mtime


while True:
    print_stdout(process)
    print_stderr(process)
    if max_mtime > last_mtime:
        last_mtime = max_mtime
        print('Restarting process.')
        process.kill()
        time.sleep(1)
        process = subprocess.Popen(command, shell=True)

    max_mtime = max(file_times(path))
    time.sleep(wait)

