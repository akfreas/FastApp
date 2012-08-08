#!/usr/bin/python
import os, sys
import errno
import stat
import argparse
import fileinput
import shutil
from Foundation import NSDictionary

from argparse import ArgumentParser


def rename_project(directory, name, bundle_id):

    search_string = "find %s -name *.xcodeproj" % directory
    name_to_change = os.popen(search_string).readlines()[0].rstrip().split("/")[-1].split(".")[0]
    theList = os.popen("find %s -name \"*%s*\"" % (directory, name_to_change))

    file_to_change = "%s/%s.xcodeproj/project.pbxproj" % (directory, name_to_change)
    replace_all(file_to_change, name_to_change, name)

    plist_files = os.popen("find %s -name *-Info.plist" % directory)

    for plist_file in plist_files:
        plist_file = plist_file.rstrip()
        plist = NSDictionary.dictionaryWithContentsOfFile_(plist_file)
        plist["CFBundleIdentifier"] = bundle_id 
        plist.writeToFile_atomically_(plist_file, True)

    for theFile in theList:
        if "xcuserdata" not in theFile:
            newFileName = theFile.rstrip().replace(name_to_change, name)
            os.rename(theFile.rstrip(), newFileName)


def replace_all(file,searchExp,replaceExp):

    old = open(file)
    x = [y.replace(searchExp, replaceExp) for y in old.readlines()]
    new = open(file, "w")
    new.writelines(x)
    new.close()
    old.close()



def start_app(app_name, dest, bundle_id):
    
    try:
        shutil.copytree("Project/", dest)
        os.chmod(dest + "/*", 755)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            print "There already exists a directory '%s'" % dest

    rename_project(dest, app_name, bundle_id)

def command_line_controller():
        
    parser = ArgumentParser(description="Allows fast creation of Xcode projects that have a certain file structure and pre-loaded frameworks.")

    parser.add_argument('app_name', help="The name you wish to give to your FastApp")
    parser.add_argument('destination', help="Destination directory for your app.")
    parser.add_argument('bundle_id', help="The bundle ID for your app.")


    arguments = parser.parse_args()

    start_app(arguments.app_name, arguments.destination, arguments.bundle_id)    
    print "App %s created in %s" % (arguments.app_name, arguments.destination)

#    rename_project(arguments.directory, arguments.new_name)

def main():
    command_line_controller()   

if __name__ == '__main__':
    main()
