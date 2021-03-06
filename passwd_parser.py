#!/usr/bin/env python2

"""
This module removes the /etc/passwd entries 
for a given user

Usage : /path/to/python2 programname.py -u user1,user2
"""


import os
import shutil
import datetime
import argparse


def read_passwd(filepath):
    '''
    a function to read the passwd files format
    and turn them into a dictionary with key as
    the username and the rest of the data parsed
    as a list
    input : filepath
    output : dict {
        'user' : [
            'user',
            'First Name...',
            '11eaadas',
            ......
            ]
    }
    '''
    file_object = open(filepath, 'r')
    shell = {}
    for line in file_object:
        line = line.strip()
        fields = line.split(":")
        # print fields
        shell[fields[0]] = fields
    file_object.close()
    return shell


def search_and_remove(users, shelldict):
    '''
    searches for users in a dictionary which contains
    the parsed passwd file
    input : user <list>, shelldict <dict>
    output : cleanedup dictionary <dict>

    '''
    shells = {}
    shells = dict(shelldict)
    for user in users:
        if user in shells.keys():
            print "user found : %s" % (user)
            auser = shells.pop(user, None)
            if auser:
                print "User popped : %s" % (auser)
    return shells


def write_passwd(filepath, shelldict):
    '''
    a function to write the metadata to the
    new generated passwd file
    '''
    try:
        with open(filepath, 'w') as fifi:
            for value in shelldict.values():
                line = ":".join(value)
                print "writing line: %s to file" % (line)
                fifi.write("%s\n" % line)

    except (OSError, IOError), error:
        print "Some file creation error..."
        print error
        return False


def backup(filepath, appendstr):
    '''
    creates a backup of a file from one location to another
    input : location file path
    output : location file path + "_backup_" + curr_datetime
    '''
    srcabspath = os.path.abspath(filepath)
    destabspath = srcabspath + "_" + appendstr   \
        + "_" + datetime.datetime.now().strftime("%y%m%d%H%M%S")
    print srcabspath, destabspath
    try:
        if os.path.exists(srcabspath):
            print 'Backing up %s to %s...' % (filepath, destabspath)
            shutil.copy2(srcabspath, destabspath)
            if copy_permissions(src=srcabspath, dest=destabspath):
                print "File permissions and stat succesfully copied"
            else:
                print "File permissions and stat not succesfully copied"
                return False
            return destabspath
    except (OSError, IOError), err:
        print "Some copy error..."
        print err
        return False


def copy_permissions(src, dest):
    '''
    Copy file permissions from src file to dest file
    '''
    try:
        import stat
        shutil.copystat(src, dest)
        st = os.stat(src)
        os.chown(dest, st[stat.ST_UID], st[stat.ST_GID])
        return True

    except (OSError, IOError), err:
        print "Some exception..."
        print err
        return False


def move_file(src, dest):
    '''
    a function to move a file from one location to another
    overwrites if the destination file exists
    '''
    dst_dirname = os.path.dirname(dest)
    try:
        dst_filename = os.path.join(dst_dirname, os.path.basename(src))
        shutil.move(src, dst_filename)
        print "moved file from %s to %s" % (src, dst_filename)
    except (OSError, IOError), err:
        print "Some exception in moving the file..."
        print err
        return False


def main(args):
    '''
    the holy grail main ()
    '''
    userlist = str(args.users)
    userlist = userlist.split(',')
    files = ['/etc/passwd', '/etc/shadow']
    users = userlist
    tempdir = "temp"
    result = ""
    for file in files:
        result = backup(file, "backup")
        if result is False:
            print "backup is not possible..."
            exit(-1)
        else:
            backupfilepath = result
            shellobj = read_passwd(file)
            updated_shell_dict = search_and_remove(users, shellobj)
            tempfile = os.path.join(tempdir, os.path.basename(file))
            write_passwd(filepath=tempfile, shelldict=updated_shell_dict)
            move_file(tempfile, file)
            copy_permissions(backupfilepath, file)

    return


if __name__ == '__main__':
    helpstr = """Send usernames in comma separated format, with no space.\n
                Example : python programname.py -u user1,user2"""
    Parser = argparse.ArgumentParser()
    Parser.add_argument('-u', action='store', dest='users',
                        help=helpstr, required=True)
    Parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parseresults = Parser.parse_args()
    main(parseresults)
