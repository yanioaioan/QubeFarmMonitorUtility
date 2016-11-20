#!/usr/bin/python
def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    import sys, os

    # Importing hou will load in Houdini's libraries and initialize Houdini.
    # In turn, Houdini will load any HDK extensions written in C++.  These
    # extensions need to link against Houdini's libraries, so we need to
    # make sure that the symbols from Houdini's libraries are visible to
    # other libraries that Houdini loads.  So, we adjust Python's dlopen
    # flags before importing hou.
    if hasattr(sys, "setdlopenflags"):
        old_dlopen_flags = sys.getdlopenflags()
        import DLFCN
        sys.setdlopenflags(old_dlopen_flags | DLFCN.RTLD_GLOBAL)

    try:
        import hou
    except ImportError:
        # Add $HFS/houdini/python2.7libs to sys.path so Python can find the
        # hou module.
        sys.path.append(os.environ['HFS'] + "/houdini/python%d.%dlibs" % sys.version_info[:2])
        import hou
    finally:
        if hasattr(sys, "setdlopenflags"):
            sys.setdlopenflags(old_dlopen_flags)

enableHouModule()
import hou
import re

def queryHipFile(sceneFile):
	
	#enableHouModule()
	#print hou.releaseLicense()
	hou.hipFile.load(sceneFile)

	for object in hou.node("/obj").children():
		print "Points in", object.path()
		#for point in object.displayNode().geometry().points():
		#    print point.position()
		
	for object in hou.node("/out").children():
		print "Points in", object.path()
		#for point in object.displayNode().geometry().points():
		#    print point.position()
		
		if object.path()=="/out/mantra1":
			print 'hey'
			print object.path()
			out_node = hou.node(object.path())
			print out_node
			outputImage = out_node.parm("vm_picture")
			outputImagePath = outputImage.eval()

			framestartROP = out_node.parm("f1")
			framestartROP = framestartROP.eval()
			
			frameEndROP = out_node.parm("f2")
			frameEndROP = frameEndROP.eval()
			
					
			#split
			outputImagePathList=outputImagePath.split('/')
			print outputImagePathList[-1]
			
			#make sure we split framename, padding and extension
			#then we will use them to check how many have been edxported and how many are about to be copied back from server..
			
			# "(semicolon or a comma) followed by a space"
                        pattern = re.compile(r"\.|_|-")
		
			pattern.split(outputImagePathList[-1])
			
			framename=pattern.split(outputImagePathList[-1])[0]#test
			framePadding=pattern.split(outputImagePathList[-1])[1]#0015
			frameExtension=pattern.split(outputImagePathList[-1])[2]#ext
							
			print "framename=%s"%(framename)
			print "framePadding=%s"%(framePadding)
			print "framemeExtension=%s"%(frameExtension)	
									
			print framestartROP				
			totalfiles=frameEndROP
			print "total number of files should be=%d"%(totalfiles)
			
			return framename,framePadding,frameExtension,framestartROP,frameEndROP,totalfiles
			
			

    

