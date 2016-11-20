#!/usr/bin/env python
from distutils.command.check import check

import threading, os, copy
import paramiko, threading, os, copy
import time
import getpass
import re
import glob

t = 0
#global map filesizes()

dictionary = {}
prevDict = {}
prevFileSize=0
prevAccessTime=0
currentFileSize=0
currentAccessTime=0


def exists(sftp, path):
        """Return True if the remote path exists
        """
        try:
            sftp.stat(path)
            return True
        except IOError, e:
            print 'log not there yet, need to submit the Qube job first'
            return False

def uploadAllFilesToSFTP(mylocalpath, myremotepath, sftp, initflag):
    flagcontinue=True
    
    if initflag==True:
        try:
            filestat=sftp.stat(str(unicode(myremotepath)))
            print '%s directory already exists on the farm'%myremotepath
            flagcontinue=False
        except:
            print '%s directory does not exist on the farm'%myremotepath

    if flagcontinue==True:
        #create initial scene directory only once
        if initflag==True:
            sftp.mkdir(myremotepath)  # Create remote_path
            sftp.chdir(myremotepath)
        
        for file in glob.glob(mylocalpath+str('*')):
            base = os.path.basename(file)
            
            if os.path.isdir(file):
                
                print file+str('/')
                
                sftp.mkdir(myremotepath+base+str('/'))  # Create remote_path
                sftp.chdir(myremotepath+base+str('/'))
                
                #recall uploadAllFilesToSFTP() for the newly found dir that we 're in now
                uploadAllFilesToSFTP(file+str('/*'), myremotepath+base+str('/'),sftp, False)
            else:
                #.. upload all simple files of the newly found dir that we 're in now
                sftp.put(file, os.path.join(myremotepath, base))

import re
import queryHip


def copyCallback(username, password,localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logfromFarmPath, logtoLocalPath, framename):

    global prevFileSize, prevAccessTime, currentFileSize, currentAccessTime, prevDict, dictionary

    #Afer 60 secs re-execute copyCallback
    global t
    t = threading.Timer(60.0, copyCallback, [username, password, localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logfromFarmPath, logtoLocalPath, framename])

    paramiko.util.log_to_file('/tmp/paramiko.log')

    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
            host='W10905'

            ssh.connect(host, username='yanioaioan', password='12345678')
    except paramiko.SSHException:
            print "Connection Failed"
            quit()

    stdin,stdout,stderr = ssh.exec_command("echo Connected")

    for line in stdout.readlines():
            print line.strip()


    #print(os.path.isdir("/home/yanioaioan/"))
    #print(os.path.exists("/home/yanioaioan/test.txt"))
    '''

    # Open a transport

    myhost = "192.168.56.101"#tete

    port = 22
    transport = paramiko.Transport((myhost, port))

    # Authenticate


    passw = password
    user = username




    print '\n*********************\n*********************'
    print 'username=%s \npassword=%s'%(user,"********")
    print '*********************\n*********************\n'

    transport.connect(username = str(unicode(user)), password = str(unicode(passw)))

    # open sftp connection

    sftp = paramiko.SFTPClient.from_transport(transport)

    #os.system("sftp "+username+"@tete")


    # Upload files from local folder to renderfarm at first
    #uploadAllFilesToSFTP("/home/yanioaioan/Desktop/myMayaSceneDir/", '/home/yanioaioan/myMayaSceneDir/', sftp, True)

    import subprocess

    #subprocess.call('python ', shell=True)
    #subprocess.call(['python', 'uploadToSftp.py', str(unicode(localScene)), str(unicode(remoteScene)), "sftp", "True" , str(username)])

    #uploadAllFilesToSFTP(str(unicode(localScene)), str(unicode(remoteScene)), sftp, True)


    print 'logfromFarmPath='+str(logfromFarmPath)

    #if log exists
    if exists(sftp,str(unicode(logfromFarmPath))):
    ###subprocess.call("sftp "+username+str(myhost)+" <<< $'get "+str(logfromFarmPath)+" ./ '",shell=True)
    #os.system("sftp "+"yanioaioan"+"@tete <<< $'mkdir "+"created""'")

    #<<< ls testSim/logNew.txt && get testSim/logNew.txt



        log=os.stat("logNew.txt")


        #if log not empty
        if log:
            #print 'log not there'
            print 'Log found'
            print log


            # list files' number in the output images directory
            #directory="/home/yanioaioan/"
            #number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

            files=sftp.listdir(unicode(farmOutputDir))
            ###files=subprocess.call("sftp "+username+"@192.168.56.101"+" <<< $'ls "+str(farmOutputDir)+" ' | wc -l > filenumber2.txt",shell=True)

            ###files=os.popen("cat filenumber.txt").read()
            ###files=files.split()[0]


            print "files=%s"%(files)



            #sortedfiles = sorted(files)

            #print "total number of files to be rendered="+str(len(sortedfiles))
            #number_of_files=len(sortedfiles)

            #Check if the directory that the rendered frames will be copied accross exist
            if not os.path.exists(copyAccrossOutputDir):
                os.mkdir(copyAccrossOutputDir)
                print 'creating dir'+str(copyAccrossOutputDir)

            #list all file copied accross locally so far
            copiedFiles = os.listdir(copyAccrossOutputDir)
            print "total number of files copied across="+str(len(copiedFiles))

            try:

                filestat=sftp.stat(str(unicode(logfromFarmPath)))
                #sftp.remove(str(unicode(logfromFarmPath)))
                print 'log found on the farm, now time to copy accross'

                #download log to monitor
                #####sftp.get(str(unicode(logfromFarmPath)), str(unicode(logtoLocalPath)))

                print "Fetch From.. "
                print str(unicode(logfromFarmPath))
                print "To.. "
                print str(unicode(logtoLocalPath))
                ###subprocess.call("sftp "+username+"@"+"test.rebex.net"+" <<< $'get "+str(unicode(logfromFarmPath))+" "+str(unicode(logtoLocalPath))+"'",shell=True)


                print 'frameStart=%d'%int(frameStart)
                print 'frameEnd=%d'%int(frameEnd)

                totalframestocopyaccross= int(frameEnd)-int(frameStart)+1
                print 'totalframestocopyaccross=%d'%totalframestocopyaccross
                print "len(copiedFiles)=%d"%len(copiedFiles)
                print "int(totalframestocopyaccross)=%d"%(int(totalframestocopyaccross))

                if len(copiedFiles)<int(totalframestocopyaccross):
                    for i in range(int(frameStart),int(frameEnd)):


                        #Now query the hip file
                        framename,framePadding,frameExtension,framestartROP,frameEndROP,totalfiles = queryHip.queryHipFile(localScene+"untitled.hipnc")
                        formatPad=len(framePadding)
                        print'Hipnc Read'

                        with open(logtoLocalPath,'r') as fin:
                                #output = fin.read()
                                #print output
                                for line in fin:
                                    '''was working till Houdini 13....verbose hrendering does not support clear way of identifying if frames are complete (based on the logging)'''
                                    #line = re.findall("*\.tiff*", line)


                                    #line = re.findall('Mantra1.*%s.*0*%s.*'%("test",i) , line)#works with maya 2016 - v-ray logging V-Ray Standalone EDU, version 3.10.01 for x64, V-Ray core version is 3.25.01

                                    #stringmatch=#frame %s (%s of %s.*).*%(i,i,frameEnd)

                                    print "line=%s"%(line)
                                    #line = "Rendering 10 frames"

                                    #matchline = re.findall("Rendering\w+", line)

                                    #print 'Test against=%s'%('mantra1 frame %d (%d of %d)'%(i,i,frameEndROP))
                                    print 'Test against=%s'%('mantra1 frame '+str(i))

                                    #regexp = re.compile(r'mantra1 frame %d \(%d of %d\)'%(i,i,frameEndROP))
                                    regexp = re.compile(r'mantra1 frame '+str(i)+'')
                                    match=0
                                    if regexp.search(line) is not None:
                                      print 'matched frame '+str(i)
                                      frameNumberMatched=i
                                      match=1



                                    #print "line=%s"%line
                                    #print "stringmatch=%s"%stringmatch
                                    #print "matchline=%s"%matchline


                                    #a=raw_input("Press Enter to continue...")


                                    if match==1:

                                            print '..Copy remote file to local dir..'#imageFileName[2]#frame number
                                            match=0

                                            print "************"
                                            print
                                            print "************"

                                            print "filepath=%s"%(str(unicode(farmOutputDir))+str(framename+str(str(i).zfill(formatPad))+"."+frameExtension))
                                            print "localpath=%s"%(str(unicode(copyAccrossOutputDir))+str(framename+str(str(i).zfill(formatPad))+"."+frameExtension))

                                            filepath = (str(unicode(farmOutputDir))+str(framename+str(str(i).zfill(formatPad))+"."+frameExtension))
                                            localpath = (str(unicode(copyAccrossOutputDir))+str(framename+str(str(i).zfill(formatPad))+"."+frameExtension))

                                            print "COPYING-->=%s"%(filepath)

                                            try:
                                                #copy rendered frame accross
                                                sftp.get(filepath, localpath)

                                                # Delete file if sftp.get() has successfully finished copying
                                                #sftp.remove(filepath)
                                            except:
                                                print "Copying frame %s failed for some reason, so we didn't remove it from the farm's home directory"



                        '''
                        with open(logtoLocalPath) as fin:
                            for line in fin:
                                #was working till Houdini 13....verbose hrendering does not support clear way of identifying if frames are complete (based on the logging)
                                #line = re.findall("*\.tiff*", line)


                                line = re.findall('Successfully written image file.*%s.*0*%s.*'%("test",i) , line)#works with maya 2016 - v-ray logging V-Ray Standalone EDU, version 3.10.01 for x64, V-Ray core version is 3.25.01

                                #Helpers usefull for maintenance

                                #if line:
                                #   print "line="+str(line)


                                #if line found in the log, means we can safely copy accross
                                if line:

                                    #Helpers usefull for maintenance

                                    #print 'line='+str(line)+' found'
                                    #it will raise an exception of file to copy across if not there
                                    #filestat=sftp.stat(str(unicode(farmOutputDir))+str(sortedfiles[i])) #"/home/yanioaioan/myHoudiniSceneDir/outputframes/frame0010.tiff"
                                    #print i


                                    for filename in sortedfiles:

                                        #Helpers usefull for maintenance

                                        #filepath = str(unicode(farmOutputDir))+str(sortedfiles[i])
                                        #filename = re.findall('myframe*%s.'%i, filename)
                                        #print filename
                                        #print framename
                                        #old way of doing it
                                        #filename = re.findall("%s\.0*%s\.[a-z]*" % (framename,i), filename)
                                        #filename = re.findall(imageFileName[-1] , filename)


                                        imageFileName=line[0].split('/')#split and get the last element, which would be the string

                                        if filename:

                                            print "************"
                                            print str(imageFileName[-1])+' imageFileNameStrippedoutof line regexpred\t<---'+str(line[0])
                                            print "************"
                                            print str(filename)+' found complete..and copied accross'

                                            filepath = str(unicode(farmOutputDir))+str(filename)
                                            localpath = str(unicode(copyAccrossOutputDir))+str(username)+str("_")+str(filename)

                                            try:
                                                #copy rendered frame accross
                                                sftp.get(filepath, localpath)

                                                # Delete file if sftp.get() has successfully finished copying
                                                sftp.remove(filepath)
                                            except:
                                                print "Copying frame %s failed for some reason, so we didn't remove it from the farm's home directory"

                        '''
                        #it will raise an exception of file to copy across is not there not there
                        #filestat=sftp.stat(str(unicode(farmOutputDir))+str(sortedfiles[i])) #"/home/yanioaioan/myHoudiniSceneDir/outputframes/frame0010.tiff"
                        # Download
                        #filepath = str(unicode(farmOutputDir))+str(sortedfiles[i]) #'/home/yanioaioan/myHoudiniSceneDir/outputframes/frame0010.tiff'
                        #localpath = str(copyAccrossOutputDir)+str(username)+str(sortedfiles[i])


                elif len(copiedFiles)>=int(totalframestocopyaccross):
                    #cancel the timer thread
                    t.cancel()
                    print 'All frames have been succesfully finished - copied accross'
                    exit()

            except:
                print 'Please submit a Qube job so as for a logfile to be created first'


    sftp.close()
    transport.close()


    #ssh.close()


    print(time.ctime())
    t.start()

if __name__ == "__main__":
    '''
    #If needed to run from terminal with user interaction
    username = raw_input("Please enter username: ")
    password = getpass.getpass()#raw_input("Please enter password: ")
    localScene = raw_input("Please enter full path to the local Scece directory to copy to renderfarm : ")#/home/yanioaioan/Desktop/myHoudiniSceneDir/
    remoteScene = raw_input("Please enter full path to the remote Scece directory on the renderfarm :")#/home/yanioaioan/myHoudiniSceneDir/
    farmOutputDir = raw_input("Please enter full path of the RenderFarm rendered output directory : ")#/home/yanioaioan/myHoudiniSceneDir/outputframes/
    copyAccrossOutputDir = raw_input("Please enter full path of the desired output directory to copy across: ")#/home/yanioaioan/Desktop/myHoudiniSceneDir/outputframes/ or /transfer/outputframes/
    frameStart = int(raw_input("Please enter the start of the framerange to be rendered: "))
    frameEnd = int(raw_input("Please enter the end of the framerange to be rendered: "))
    logfromFarmPath = raw_input("Please enter full path of the log file on the farm : ")
    logtoLocalPath= raw_input("Please enter full path of the log file on the locally : ")
    framename = raw_input("Please enter the frame name (excluding any file extensions)")
    '''

    #If needed to run directly

    username ="yanioaioan"
    password = "266592kR"
    '''
    localScene="/home/yanioaioan/Desktop/QUBE/myMayaSceneDir/"
    remoteScene="/home/yanioaioan/myMayaSceneDir/"
    farmOutputDir="/home/yanioaioan/myMayaSceneDir/textures/perspShape/"
    copyAccrossOutputDir="/home/yanioaioan/Desktop/QUBE/myMayaSceneDir/textures/perspShape/"
    frameStart="1"
    frameEnd="100"
    logfromFarmPath="/home/yanioaioan/myMayaSceneDir/textures/logNew.txt"
    logtoLocalPath="/home/yanioaioan/Desktop/QUBE/myMayaSceneDir/textures/logNew.txt"
    framename="test"
    '''


    localScene="/home/yanioaioan/Desktop/QUBE/testSim/"
    remoteScene="/home/yanioaioan/testSim/"
    farmOutputDir="/home/yanioaioan/testSim/render/"
    copyAccrossOutputDir="/home/yanioaioan/Desktop/QUBE/testSim/render/"
    frameStart="1"
    frameEnd="25"
    logfromFarmPath="/home/yanioaioan/testSim/logNew.txt"
    logtoLocalPath="/home/yanioaioan/Desktop/QUBE/testSim/logNew.txt"
    framename="test_"



    copyCallback(username, password, localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logfromFarmPath, logtoLocalPath, framename)
    
