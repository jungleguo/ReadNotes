# charset = -*-utf-8-*-
from os import listdir, getcwd, chdir, system, path, makedirs, sep
from docker import DockerClient
import tarfile
import shutil
import time
import json
import requests
import sys
import win32api

PROJECT_NAME = "PROJECT_NAME"
DOCKER_IMAGE = "DOCKER_IMAGE"


def getConfigServiceUrl(gateWayUrl):
    return gateWayUrl + "/eggkeeper/v1/PO_Purchase_Order"


def getDockerServiceUrl(ip):
    return "http://" + ip + ":8500/dockerapi/v2/services"


def getTaskVersion(taskName):
    info = win32api.GetFileVersionInfo(taskName, sep)
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(
        ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    return version


def getTaskVersions(gateWayUrl, ):
    taskVersion = requests.get(
        getConfigServiceUrl(gateWayUrl) + "/PO_Task_Versions",
        headers={"content-type": "application/json"})


def getCurrentDir():
    return path.join(getcwd())


def getTaskProjectDirs():
    currentDir = getCurrentDir()
    tasksDirs = path.join(currentDir, "Tasks")
    taskProjectDirs = [path.join(tasksDirs, f) for f in listdir(
        tasksDirs) if path.isdir(path.join(tasksDirs, f))]
    return taskProjectDirs


def getPublishDirs(taskProjectDirs):
    publishDirs = [path.join(f, "bin/release/netcoreapp2.1/publish")
                   for f in taskProjectDirs if path.isdir(path.join(f, "bin/release/netcoreapp2.1/publish"))]
    return publishDirs


def build(taskProjectDirs):
    for taskDir in taskProjectDirs:
        chdir(taskDir)
        try:
            system('dotnet publish -c release')
        except:
            print("build %s failed.", path.basename(taskDir))

    print("All build succeed.")


def getDockerDir():
    currentDir = getCurrentDir()
    dockerDir = path.join(currentDir, "docker")
    return dockerDir if path.isdir(dockerDir) else makedirs(dockerDir)


def getDockerClient(base_url, version='auto'):
    client = DockerClient(base_url, version)
    return client


def buildImage(docker_client, project_name):
    param = {}
    param["path"] = path
    dockerClient = docker_client
    try:
        image = dockerClient.images.build(param)
    except:
        print("build %s failed, exception: %s" % (project_name, image[1]))
    return image[0]


def backupImage():
    pass


def updateImage(gateWayUrl, systemName, name, value):
    body = {}
    body["systemName"] = systemName
    body["configName"] = name
    body["configValue"] = value
    r = requests.put(getConfigServiceUrl(gateWayUrl),
                     data=json.dumps(body),
                     headers={'content-type': 'application/json'})
    print("Update image config:%s, status_code: %d" % (name, r.status_code))


def publish():
    dockerClient = DockerClient()
    dockerClient.images.push();


if __name__ == "__main__":
    dockerDir = getDockerDir()
    taskProjectDirs = getTaskProjectDirs()
    if len(taskProjectDirs) > 0:
        build(taskProjectDirs)
    publishDirs = getPublishDirs(taskProjectDirs)
