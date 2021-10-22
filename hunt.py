#!/usr/bin/python

import sys, getopt
import subprocess
import os
import time

netstatCommand = 'netstat -anob | Select-String -Pattern D2R.exe -Context 1,0 | findstr :443 | findstr ESTABLISHED | findstr /v 37.244.28.80 | findstr /v 34.117.122.6 | findstr /v 24.105.29.76 | findstr /v 117.52.35.179 | findstr /v 117.52.35.79 | findstr /v 137.221.106.88'

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ht:")
    except getopt.GetoptError:
        print("python hunt.py -t <target_ip>")

    for opt, arg in opts:
        if opt == "-h":
            print("python hunt.py -t <target_ip>")
            sys.exit()
        elif opt == "-t":
            checkValidIp(arg)
            huntIp(arg)
            sys.exit()
        else:
            print("python hunt.py -t <target_ip>")


def huntIp(targetIp):
    lastIps = []
    while True:
        currentIps = getGameIp()
        if targetIp in currentIps:
            break
        if currentIps != lastIps:
            lastIps = currentIps
            if currentIps != []:
                print("Current game ip is: " + ",".join(currentIps) + "...")
        time.sleep(1)

    print("!!! Found target ip: " + targetIp + "!!!")
    print("Killing tiny task...")
    killTinyTask()

def getGameIp():
    try:
        netstatOutput = subprocess.check_output("powershell -command " + netstatCommand)
        return list(map(lambda x: x.split()[2].decode("utf-8").split(":")[0], netstatOutput.splitlines()))
    except subprocess.CalledProcessError as netstatException:
        return []

def killTinyTask():
    os.system("taskkill /f /im \"TinyTask.exe\"")

def checkValidIp(ip):
    assert (len(ip.split(".")) == 4), "Invalid ip: " + ip
    for number in ip.split("."):
        assert (number.isdigit()), number + " is not a integer"
        assert (int(number) >= 0 and int(number) < 256), number + " is not in the valid ip range"

if __name__ == "__main__":
    main(sys.argv[1:])
