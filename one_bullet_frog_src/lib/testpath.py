import os,os.path

mypath= os.path.abspath(__file__)

sp=os.path.split(mypath)

print "split again"

spp=os.path.split(sp[0])

print spp
#

os.chdir(spp[0])

newdir=os.getcwd()

print "new dir is",newdir

joinedpath = os.path.join(newdir,"data")

print "the joint path is",joinedpath