#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
The script transfers a ready scene folder to the renderfarm, and sits there and waits for the user to submit a new houdini or maya job.
The user resubmits a new job and specifies a unique log filename remote path (in ex. /home/username/myhoudiniscene/logframes1-100.txt) for this render
The script monitors the whole process with regards to the finished rendered frames and copies them accross. The script runs on a interval but the copying process
is triggered by the renderers fired on Qube farm whenever applicable.
The script afterall, can be used to facilitate the existing renderfarm account 10 quota restriction. 
Finished frames can either be copied back to home or tranfer drives dir or using ssh one could fire Qube to many computer on the network having the finished frames being copied accross
to the corresponding /transfer drives when they are finished.
'''

import os,sys,copyutil
from PyQt4 import QtGui, QtCore

#Default attributes to be loaded when there's no savedOutForm.txt
username="yioannidis"
password=""
localSceneDir="/home/yioannidis/Desktop/myHoudiniSceneDir/"
remoteSceneDir="/home/yioannidis/myHoudiniSceneDir/"
farmOutputDir="/home/yioannidis/myHoudiniSceneDir/outputframes/"
copyAccrossOutputDir="/home/yioannidis/Desktop/myHoudiniSceneDir/outputframes/"
frameStart="1"
frameEnd="15"
logFromPath="/home/yioannidis/myHoudiniSceneDir/testlog.txt"
logToPath="/home/yioannidis/Desktop/myHoudiniSceneDir/outputframes/testlog.txt"
framename="myframe"


instrcutionsText="""1) Prepare the scene directory to be copied accross to renderfarm with relatives
    path to all assets needed (textures etc.)
 
2) Double check the directory does not exist on the renderfarm

3) Press "Start Monitoring to start the auto Monitor Utility

4) Run the goQube from the command line and open a Resubmit job dialog

5) MAKE SURE that you specify a unique logfile name, 
   based on the frame range you are about to render (..mylog1-100.txt)
   on the Resubmit dialog filed named 'Log Output File'
   
6) Fill in the AutoCopy Form

6) Submit the job and let the tool monitor your rendering progress"""
            

def exists(path):
        """Return True if the remote path exists
        """
        if os.path.isfile(path):
            return True
        else:
            print 'savedOutForm.txt not there'
            return False

class IntructionsWindow(QtGui.QWidget):
    
    def __init__(self):
        super(IntructionsWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        global instrcutionsText
        
        self.lbl = QtGui.QLabel(instrcutionsText,self)
        self.lbl.move(10, 10)
        
        
        self.setGeometry(750, 750, 750, 300)
        self.setWindowTitle('Instructions')
        self.show()

class Util(QtGui.QWidget):
    
    def __init__(self):
        super(Util, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):
		global username,password,localSceneDir,remoteSceneDir,farmOutputDir,copyAccrossOutputDir,frameStart,frameEnd,logFromPath,logToPath,framename
		
		#Read in the field vaules in (Optional - Currently not saving any savedOutForm.txt, it's hashed out see. line 145-153)
		if exists("savedOutForm.txt"):
			lines = open("savedOutForm.txt").read().splitlines()
			print "Values read from saved file:\n1)%s\n2)%s\n3)%s\n4)%s\n5)%s\n6)%s\n7)%s\n8)%s\n9)%s\n10)%s\n11)%s"%(lines[0],lines[1],lines[2],lines[3],lines[4],lines[5],lines[6],lines[7],lines[8],lines[9],lines[10])
			username=lines[0]
			password=lines[1]
			localSceneDir=lines[2]
			remoteSceneDir=lines[3]
			farmOutputDir=lines[4]
			copyAccrossOutputDir=lines[5]
			frameStart=lines[6]
			frameEnd=lines[7]
			logFromPath=lines[8]
			logToPath=lines[9]
			framename=lines[10]
			
		self.lbl = QtGui.QLabel('Username',self)
		self.lbl.move(10, 10)
		self.qle = QtGui.QLineEdit(self)
		self.qle.setText(username)
		self.qle.move(10, 30)

		self.lbl2 = QtGui.QLabel('Password', self)
		self.lbl2.move(10, 70)		     
		self.qle2 = QtGui.QLineEdit(self)
		self.qle2.setText(password)
		self.qle2.setEchoMode(QtGui.QLineEdit.Password)
		self.qle2.move(10, 90)
		
		self.lbl3 = QtGui.QLabel('Specify local Scece directory to copy to renderfarm', self)
		self.lbl3.move(10, 130)                
		self.qle3 = QtGui.QLineEdit(self)		
		self.qle3.setText(localSceneDir)
		self.qle3.setFixedWidth(550)
		self.qle3.move(10, 150)

		self.lbl4 = QtGui.QLabel('Specify remote Scece directory on the renderfarm', self)
		self.lbl4.move(10, 190)
		self.qle4 = QtGui.QLineEdit(self)
		self.qle4.setText(remoteSceneDir)
		self.qle4.setFixedWidth(550)
		self.qle4.move(10, 210)

		
		self.lbl5 = QtGui.QLabel('Copy Rendered Frames From.. (renderfarm directory)',self)        
		self.lbl5.move(10, 250)       
		self.qle5 = QtGui.QLineEdit(self)
		self.qle5.setText(farmOutputDir)
		self.qle5.setFixedWidth(550)
		self.qle5.move(10, 270)

		self.lbl6 = QtGui.QLabel('Copy Rendered Frames To.. (local directory)', self)
		self.lbl6.move(10, 310)                
		self.qle6 = QtGui.QLineEdit(self)
		self.qle6.setText(copyAccrossOutputDir)
		self.qle6.setFixedWidth(550)
		self.qle6.move(10, 330)

		self.lbl7 = QtGui.QLabel('Start Frame', self)
		self.lbl7.move(10, 370)                
		self.qle7 = QtGui.QLineEdit(self)
		self.qle7.setText(frameStart)
		self.qle7.move(10, 390)


		self.lbl8 = QtGui.QLabel('End Frame',self)
		self.lbl8.move(10, 430)       
		self.qle8 = QtGui.QLineEdit(self)
		self.qle8.setText(frameEnd)
		self.qle8.move(10, 450)


		self.lbl9 = QtGui.QLabel('Log File path.. (renderfarm directory)',self)
		self.lbl9.move(10, 490)       
		self.qle9 = QtGui.QLineEdit(self)
		self.qle9.setText(logFromPath)
		self.qle9.setFixedWidth(550)
		self.qle9.move(10, 510)

		self.lbl10 = QtGui.QLabel('Log File path.. (local directory)', self)
		self.lbl10.move(10, 550)                
		self.qle10 = QtGui.QLineEdit(self)
		self.qle10.setText(logToPath)
		self.qle10.setFixedWidth(550)
		self.qle10.move(10, 570)

		self.lbl11 = QtGui.QLabel('Frame Name Specified in Houdini (in ex. if myframe$F4.tiff..it should be myframe)', self)
		self.lbl11.move(10, 610)
		self.qle11 = QtGui.QLineEdit(self)
		self.qle11.setText(framename)
		self.qle11.move(10, 630)
		

		#qle.textChanged[str].connect(self.onChanged)
		#qle2.textChanged[str].connect(self.onChanged2)

		self.btn = QtGui.QPushButton('Start Monitoring..', self)
		self.btn.move(300, 700)
		self.btn.clicked.connect(self.doAction)

		self.setGeometry(750, 750, 750, 750)
		self.setWindowTitle('Auto-Copy Renderfarm Utility')
		self.show()




	#self.timer = QtCore.QBasicTimer()
	#self.step = 0

    def doAction(self):
		username = self.qle.text()
		password = self.qle2.text()
		localScene = self.qle3.text()
		remoteScene = self.qle4.text()
		dirFrom = self.qle5.text()
		dirTo = self.qle6.text()
		frameStart = self.qle7.text()
		frameEnd = self.qle8.text()
		logFrom = self.qle9.text()
		logTo = self.qle10.text()
		framename = self.qle11.text()
		
		#Create a save savedOutForm.txt to save field values to if not there already
		#if not exists("savedOutForm.txt"):
		'''
		#Save out values of the form to savedOutForm.txt
		savedOutForm = open("savedOutForm.txt", "w")
		print "Saving File: ", savedOutForm.name
		savedOutForm.write("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n"%(username, password,localScene, remoteScene, farmOutputDir, copyAccrossOutputDir, frameStart, frameEnd, logFromPath, logToPath, framename) )
		savedOutForm.close()
		'''
		copyutil.copyCallback(username, password, localScene, remoteScene, dirFrom, dirTo, frameStart, frameEnd, logFrom, logTo, framename)


    def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Util()
    
    ex2 = IntructionsWindow()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
