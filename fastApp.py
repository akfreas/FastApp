#!/usr/bin/python
import os, sys
import errno
import stat
import argparse
import fileinput
import shutil
import pystache
from Foundation import NSDictionary

from argparse import ArgumentParser
from glob import glob

def rename_project(project_dir, new_project_name, bundle_id):

    search_string = "find %s -name *.xcodeproj" % project_dir
    name_to_change = os.popen(search_string).readlines()[0].rstrip().split("/")[-1].split(".")[0]

    project_directories = os.walk(project_dir) #[y for x in os.walk(project_dir) for y in glob(os.path.join(x[0], ''))]


    for directory in project_directories:
        new_directory = directory[0].replace(name_to_change, new_project_name)
        print "creating %s" % new_directory
        os.makedirs(new_directory)
        files = [os.path.join(directory[0], x) for x in directory[2]]
        for dir_file in files:
            new_filename = dir_file.replace(name_to_change, new_project_name)
            shutil.copyfile(dir_file, new_filename)
            replace_all(new_filename, name_to_change, new_project_name)



    plist_files = os.popen("find %s -name *Info.plist" % project_dir)

    for plist_file in plist_files:
        plist_file = plist_file.rstrip()
        plist = NSDictionary.dictionaryWithContentsOfFile_(plist_file)
        plist["CFBundleIdentifier"] = bundle_id 
        plist.writeToFile_atomically_(plist_file, True)
    
def replace_all(file,searchExp,replaceExp):

    old = open(file)
    x = [y.replace(searchExp, replaceExp) for y in old.readlines()]
    new = open(file, "w")
    new.writelines(x)
    new.close()
    old.close()



def start_app(new_app_name, source_project, dest_project, bundle_id):
    
    rename_project(source_project, new_app_name, bundle_id)

def command_line_controller():
        
    parser = ArgumentParser(description="Allows fast creation of Xcode projects that have a certain file structure and pre-loaded frameworks.")

    parser.add_argument('source_project', help="The source scaffolding project you wish to use.")


    arguments = parser.parse_args()


    params = {} #{'bundle_id' : 'com.sashimiblade.camcam', 'app_name' : 'CamCam'}
    params['bundle_id'] = raw_input('Bundle ID for app: ')
    params['scheme'] = raw_input('Enter the main scheme name: ')
    params['app_name'] = raw_input('App name: ')
    params['app_language'] = "English"
    params['team_id'] = raw_input('iTC Team name: ')
    params['itunes_username'] = raw_input('iTC Username: ')
    start_app(params['app_name'], arguments.source_project, params['app_name'], params['bundle_id'])
    print "App %s created in %s" % (params['app_name'], params['app_name'])

    info_file_path = os.path.join(params['app_name'], 'fastlane', 'Appfile')
    app_info_file = open(info_file_path, "r")

    new_file = pystache.render(app_info_file.read(), params)

    app_info_file.close()

    new_info_file = open(info_file_path, "w+")
    new_info_file.write(new_file)
    new_info_file.close()



#    rename_project(arguments.directory, arguments.new_name)

def main():
    command_line_controller()   

if __name__ == '__main__':
    main()
