#!/usr/bin/python

import sys,os,glob

#uploadAllFilesToSFTP(str(unicode(localScene)), str(unicode(remoteScene)), sftp, True)




def uploadAllFilesToSFTP(mylocalpath, myremotepath, sftp, initflag, username):
	
	os.system("sftp "+username+"@tete <<< ls")

	flagcontinue=True

	if flagcontinue==True:
		    '''
			#create initial scene directory only once
			if initflag=="True":
				#sftp.mkdir(myremotepath)  # Create remote_path
				
				print "MKDIRIRING"
				os.system("sftp "+username+"@tete <<< mkdir myremotepath")
				#sftp.chdir(myremotepath)
				os.system("sftp "+username+"@tete <<< cd myremotepath")
			
			for file in glob.glob(mylocalpath+str('*')):
				print file
			
				base = os.path.basename(file)
				
				if os.path.isdir(file):
					
					print file+str('/')
					
					#sftp.mkdir(myremotepath+base+str('/'))  # Create remote_path
					print  "PATH=%s"%(myremotepath+base)
					path=str(myremotepath)+str(base)
					os.system("sftp "+username+"@tete <<< mkdir path")
			
					#sftp.chdir(myremotepath+base+str('/'))
					os.system("sftp "+username+"@tete <<< cd myremotepath+base) ")
					
					#recall uploadAllFilesToSFTP() for the newly found dir that we 're in now
					uploadAllFilesToSFTP(file+str('/*'), myremotepath+base, "sftp", "False", str(username))
				else:
					#.. upload all simple files of the newly found dir that we 're in now
					#sftp.put(file, os.path.join(myremotepath, base))
					os.system("sftp "+username+"@tete <<< put(file, os.path.join(myremotepath, base)) ")

			'''               

if __name__ == "__main__":
	
	mylocalpath = sys.argv[1]
	myremotepath = sys.argv[2]
	initflag = sys.argv[4]
	username = sys.argv[5]

	uploadAllFilesToSFTP(mylocalpath,myremotepath,"sftp", initflag, username)


