#!/usr/bin/python
import os, sys
import argparse
import fileinput



NameToChange = os.popen("find . -name *.xcodeproj").readlines()[0].rstrip().split("./")[1].split(".")[0]


def renameProject(name):

    theList = os.popen("find . -name \"*" + NameToChange +"*\"")
    print NameToChange

    fileToChange = NameToChange + ".xcodeproj/project.pbxproj"
    replaceAll(fileToChange, NameToChange, name)

    for theFile in theList:
        if "xcuserdata" not in theFile:
            print theFile
            newFileName = theFile.rstrip().replace(NameToChange, name)
            os.rename(theFile.rstrip(), newFileName)

def replaceAll(file,searchExp,replaceExp):

    old = open(file)
    x = [y.replace(searchExp, replaceExp) for y in old.readlines()]
    new = open(file, "w")
    new.writelines(x)
    new.close()
    old.close()

def command_line_controller():
        
    parser = argparse.ArgumentParser(description="Keeps track of commit hashes so we can avoid archiving workspace in jenkins.")

    parser.add_argument('--new_name', '-n', dest="new_name", help="Sets project name")

    arguments = parser.parse_args()

    renameProject(arguments.new_name)
def main():
    command_line_controller()   

if __name__ == '__main__':
    main()
