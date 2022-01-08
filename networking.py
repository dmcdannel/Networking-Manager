from os import listdir
from os.path import exists
import subprocess
import glob

#this is for ubuntu machines 18+

#first we will want to see the current interfaces we have
def findInterfaces():
    cmd = "ls /sys/class/net"
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = proc.communicate()

    listOfInterfaces = []
    interfaces = output.decode("utf-8").split("\n")

    for item in interfaces:
        if "lo" not in item:
            listOfInterfaces.append(item)
    
    listOfInterfaces = listOfInterfaces[:-1]

    return listOfInterfaces

#then we would like to view the ipconfig on said interfaces

def findCurrentIpConfig(interface):
    cmd = "ip a show "+interface
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = proc.communicate()
    
    config = output.decode("utf-8")
    findinet = config.find("inet")
    ip = config[findinet:findinet+20]
    ip = ip[-15:]#this part needs to be heavily tested however seems to be working
    
    return ip
    

#then i assume we would like to set it if we would like to change it
def changeIpConfig(interface):
    paths = [r"/etc/netplan/", r"/lib/netplan/", r"/run/netplan/"]

    mypath = None
    filename = None

    while(mypath == None):
        for item in paths:
            files = glob.glob(item+r"*.yaml")
            if len(files) > 0:
                mypath = item
                filename = files
            else:
                cmd = "sudo netplan generate"
                proc = subprocess.Popen(cmd.split())
        print("loop complete")

    print(mypath, filename)

    #so now we have found the yaml file we need any now we need to edit it of course....

    print("Warning this will delete the configuration we are working with and generate a new file")
    print("This could delete important configuration. I always recommend a backup.")
    x = input("Do you wish to proceed with a backup? y/n")
    if x == "y":
        cmd = "sudo cp "+filename[0]+" "+filename[0]+".back"
        proc = subprocess.Popen(cmd.split())
    elif x == "n":
        pass
    else:
        print("Not a valid input, exiting")
        exit()
#my netplan is blank how da fuq

    print("made it down here")
findInterfaces()#returns list
findCurrentIpConfig("enp39s0")#returns string
changeIpConfig("enp39s0")