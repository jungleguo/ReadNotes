# charset = -*-utf-8-*-
from os import listdir, getcwd, chdir, system, path, makedirs
import tarfile
import shutil
import time
import json
import requests
import sys


def getTaskProjectDirs():
    tasksDirs = path.join(getcwd(), "Tasks")
    taskProjectDirs = [path.join(tasksDirs, f) for f in listdir(
        tasksDirs) if path.isdir(path.join(tasksDirs, f))]
    return taskProjectDirs


def build(taskProjectDirs):
    for taskDir in taskProjectDirs:
        chdir(taskDir)
        try:
            system('dotnet publish -c release')
        except:
            print("build %s failed.", path.basename(taskDir))

    print("All build succeed.")


def pack():
    pass


def backupImage():
    pass


def updateImage():
    pass


def getDockerServiceUrl():
    pass


def publish():
    pass


if __name__ == "__main__":
    taskProjectDirs = getTaskProjectDirs()
    if len(taskProjectDirs) > 0:
        build(taskProjectDirs)
    
    
