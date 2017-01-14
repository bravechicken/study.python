from distutils.core import setup
import py2exe,os.path,os,sys

fullpath = os.path.abspath(__file__)
maindir = os.path.split(fullpath)[0] 

libdir = os.path.join(maindir,"lib")
sfxdir = os.path.join(maindir,"sfx")
fontsdir = os.path.join(maindir,"fonts")
imagesdir = os.path.join(maindir,"images")

# list files in maindir
libdirfiles = os.listdir(libdir)
sfxdirfiles = os.listdir(sfxdir)
fontsdirfiles = os.listdir(fontsdir)
imagesdirfiles = os.listdir(imagesdir)

modulenames=[]
newlibfiles=[]
for thing in libdirfiles:
	modulenames.append(thing)
	nthing = os.path.join(libdir,thing)
	newlibfiles.append(nthing)

newsfxfiles=[]
for thing in sfxdirfiles:
	nthing = os.path.join(sfxdir,thing)
	newsfxfiles.append(nthing)

newfontsfiles=[]
for thing in fontsdirfiles:
	nthing = os.path.join(fontsdir,thing)
	newfontsfiles.append(nthing)

newimagesfiles=[]
for thing in imagesdirfiles:
	nthing = os.path.join(imagesdir,thing)
	newimagesfiles.append(nthing)

	
#print newfontsfiles

#help(setup)
#sys.path.append(libdir)

setup( windows = [{'script':'onebulletfrog.py'}],
		author = "Fyeidale Edmond",
		author_email ="fienixgdev@gmail.com",
		options = {"py2exe":{
						"bundle_files":1,
						"compressed":True,
						"optimize":2
							}},
							
		data_files = [ 	(".",["levels.txt","getpath.py"]),
						("sfx", newsfxfiles),
						("fonts", newfontsfiles),
						("images", newimagesfiles)
						] )
