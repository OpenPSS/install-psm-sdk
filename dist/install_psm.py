#!/usr/bin/python3

import os
import sys
import requests
import subprocess
import psutil
import shutil

if len(sys.argv) < 2:
    print("Not specified enough arguments, need version")
    exit(-1)
version = sys.argv[1]

SDK_URL = "https://archive.org/download/psm-sdk/PSM_SDK_"+version+".exe"
SDK_EXE = "PSM_SDK.exe"

print ("Installing PSM SDK v"+version)

dl =requests.get(SDK_URL)

if not dl.status_code == 200:
    print("Failed to download PSM SDK, '" + SDK_URL + "' : " + str(dl.status_code))
    exit(-1)
    
print("Downloading: "+SDK_URL)
open(SDK_EXE, "wb").write(dl.content)

print ("Extracting subinstallers")
status = subprocess.Popen(["7z.exe", "x", SDK_EXE, "software", "-y", "-bb0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

if not status == 0:
    print("7z extract failed. ("+str(status)+")")
    exit(status)

for installer in os.listdir("software"):
    print("Installing dependancy: "+installer)
    if installer.endswith(".msi"):
        subprocess.Popen(["msiexec.exe", "/qn", "/i", "software\\"+installer]).wait()
    if installer.endswith(".exe"):
        subprocess.Popen(["software\\"+installer, "/q"]).wait()

shutil.rmtree('software')

print("Installing: "+SDK_EXE)
p = subprocess.Popen([SDK_EXE, "/S"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)


while p.poll() is None:
    for proc in psutil.process_iter():
        if proc.name() == "dpinst.exe":
            try:
                print("Ending process: "+proc.name())
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    
status = p.poll()
if not status == 0:
    print("Got status: ("+str(status)+")")
exit(status)
