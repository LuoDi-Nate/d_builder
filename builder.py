import getopt
import sys

print 'begin build'

print sys.argv[0]

opts, args = getopt.getopt(sys.argv[1:], "ih:o:")

for opt, value in opts:
    if opt == '-i':
        print "i :", value
    elif opt == '-h':
        print "h :", value
