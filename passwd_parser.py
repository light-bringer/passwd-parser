#!/usr/bin/env python


import os
import shutil
import datetime

file = "./data/shade"
file_object = open(file, 'r')

shell = {}
for line in file_object:
    line = line.strip()
    fields = line.split(":")
    # print fields
    shell[fields[0]] = fields[-1]

file_object.close()

# print shell
for user in shell.keys():
    # print("{0:11} => {1}".format(user, shell[user]))
    pass

def backup(filepath):
    
    '''
    creates a backup of a file from one location to another
    input : location file path
    output : location file path + "_backup_" + curr_datetime 
    '''
    abspath = os.path.abspath(filepath)
    backupstr = abspath + "_backup_" + datetime.datetime.now().strftime("%y%m%d%H%M%S")
    print abspath, backupstr
    try:
        if os.path.exists(abspath):
            print 'Copying %s to %s...' % (filepath, backupstr)
            shutil.copy(abspath, backupstr)
            return 0
    except (OSError, IOError), e:
        print "Some copy error..."
        print e
        return -1
    

def copy_permissions(source, dest):
    pass