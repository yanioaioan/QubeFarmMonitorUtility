#!/usr/bin/env python


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
            print 'log not there yet, need to submit the houdin Qube job first'
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
                
def copyCallback(username, password,localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logfromFarmPath, logtoLocalPath, framename):
	
	global prevFileSize, prevAccessTime, currentFileSize, currentAccessTime, prevDict, dictionary
	
	#Afer 60 secs re-execute copyCallback
	global t
	t = threading.Timer(10.0, copyCallback, [username, password, localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logfromFarmPath, logtoLocalPath, framename])
	
	
	#totalframeNumberToBeRendered=40
	
	paramiko.util.log_to_file('/tmp/paramiko.log')
	'''
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
			host='W10905'
			
			ssh.connect(host, username='yioannidis', password='12345678')
	except paramiko.SSHException:
			print "Connection Failed"
			quit()
	 
	stdin,stdout,stderr = ssh.exec_command("echo Connected")
	 
	for line in stdout.readlines():
			print line.strip()
			

	#print(os.path.isdir("/home/yioannidis/"))
	#print(os.path.exists("/home/yioannidis/test.txt"))
	'''

	# Open a transport

	myhost = "tete"
	port = 22
	transport = paramiko.Transport((myhost, port))

	# Authenticate

	#password = "12345678"
	#username = "yioannidis"
	transport.connect(username = username, password = password)

	
	# open sftp connection

	sftp = paramiko.SFTPClient.from_transport(transport)
	
	# Upload files from local folder to renderfarm at first
	#uploadAllFilesToSFTP("/home/yioannidis/Desktop/myMayaSceneDir/", '/home/yioannidis/myMayaSceneDir/', sftp, True)
	uploadAllFilesToSFTP(str(unicode(localScene)), str(unicode(remoteScene)), sftp, True)
	
	

	if exists(sftp,str(unicode(logfromFarmPath))):
		#print 'log not there'

		# list files' number in the output images directory
		#directory="/home/yioannidis/"
		#number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

		files=sftp.listdir(unicode(farmOutputDir))
		sortedfiles = sorted(files)
		
		print "total number of files to be rendered="+str(len(sortedfiles))
		number_of_files=len(sortedfiles)
        
        #Check if the directory that the rendered frames will be copied accross exist
        if not os.path.exists(copyAccrossOutputDir):
            os.mkdir(copyAccrossOutputDir)

        copiedFiles = os.listdir(copyAccrossOutputDir)
        print "total number of files copied across="+str(len(copiedFiles))


        try:
            filestat=sftp.stat(str(unicode(logfromFarmPath)))
            #sftp.remove(str(unicode(logfromFarmPath)))

            #download log to monitor
            sftp.get(str(unicode(logfromFarmPath)), str(unicode(logtoLocalPath)))

            #	for line in open(str(unicode(logtoLocalPath))):
            #		if " frame 1" in line:
            #			print line
                    

            print 'frameStart=%d'%int(frameStart)
            print 'frameEnd=%d'%int(frameEnd)

            totalframestocopyaccros= int(frameEnd)-int(frameStart)+1
            print 'totalframestocopyaccros=%d'%totalframestocopyaccros



            if len(copiedFiles)<int(totalframestocopyaccros):
                for i in range(int(frameStart),int(frameEnd)+1):
                    #print sortedfiles[i]
                    keyword='\ frame\ %d$'%i
                    #print keyword

                    
                    with open(logtoLocalPath) as fin:
                        for line in fin:
                            line = re.findall(keyword, line)
                            if line:
                                print 'line='+str(line)+' found'
                                #it will raise an exception of file to copy across is not there not there'''
                                #filestat=sftp.stat(str(unicode(farmOutputDir))+str(sortedfiles[i])) #"/home/yioannidis/myHoudiniSceneDir/outputframes/frame0010.tiff"
                                #print i
                                
                                for filename in sortedfiles:
                                    #filepath = str(unicode(farmOutputDir))+str(sortedfiles[i])
                                    #filename = re.findall('myframe*%s.'%i, filename)
                                    #print filename
                                    
                                    #print framename
                                    
                                    filename = re.findall("%s0*%s\.[a-z]*" % (framename,i), filename)
                                    if filename:
                                        print str(filename[0])+' found..and copied'
                                        filepath = str(unicode(farmOutputDir))+str(filename[0])
                                        localpath = str(copyAccrossOutputDir)+str(username)+str(filename[0])
                                        
                                        #copy rendered frame accross
                                        sftp.get(filepath, localpath)
                                        # Delete file
                                        sftp.remove(filepath)

                    # it will raise an exception of file to copy across is not there not there'''
                    #filestat=sftp.stat(str(unicode(farmOutputDir))+str(sortedfiles[i])) #"/home/yioannidis/myHoudiniSceneDir/outputframes/frame0010.tiff"

                    # Download
                    
                    #filepath = str(unicode(farmOutputDir))+str(sortedfiles[i]) #'/home/yioannidis/myHoudiniSceneDir/outputframes/frame0010.tiff'
                    #localpath = str(copyAccrossOutputDir)+str(username)+str(sortedfiles[i])
            elif len(copiedFiles)>=int(totalframestocopyaccros):
                #cancel the timer thread
                t.cancel()
                print 'All frames have been succesfully finished - copied accross'

        except:
            print 'Please submit a Qube job so as for a logfile to be created first'
            

	sftp.close()
	transport.close()


	#ssh.close()

	
	print(time.ctime())
	t.start()
	
if __name__ == "__main__":

    username = raw_input("Please enter username: ")
    password = getpass.getpass()#raw_input("Please enter password: ")
    localScene = raw_input("Please enter full path to the local Scece directory to copy to renderfarm : ")#/home/yioannidis/Desktop/myHoudiniSceneDir/
    remoteScene = raw_input("Please enter full path to the remote Scece directory on the renderfarm :")#/home/yioannidis/myHoudiniSceneDir/
    farmOutputDir = raw_input("Please enter full path of the RenderFarm rendered output directory : ")#/home/yioannidis/myHoudiniSceneDir/outputframes/
    copyAccrossOutputDir = raw_input("Please enter full path of the desired output directory to copy across: ")#/home/yioannidis/Desktop/myHoudiniSceneDir/outputframes/ or /transfer/outputframes/
    frameStart = int(raw_input("Please enter the start of the framerange to be rendered: "))
    frameEnd = int(raw_input("Please enter the end of the framerange to be rendered: "))
    logfromFarmPath = raw_input("Please enter full path of the log file on the farm : ")
    logtoLocalPath= raw_input("Please enter full path of the log file on the locally : ")
    framename = raw_input("Please enter the frame name (excluding any file extensions)")

    copyCallback(username, password, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logFromPath, logToPath, framename)
