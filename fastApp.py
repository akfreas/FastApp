#!/usr/bin/python
import os, sys
import errno
import stat
import argparse
import fileinput
import shutil
import pystache
import re
from Foundation import NSDictionary
import json

from argparse import ArgumentParser
from glob import glob

def rename_project(project_dir, new_project_name, bundle_id):

    search_string = "find %s -name *.xcodeproj" % project_dir
    name_to_change = os.popen(search_string).readlines()[0].rstrip().split("/")[-1].split(".")[0]

    project_directories = os.walk(project_dir) #[y for x in os.walk(project_dir) for y in glob(os.path.join(x[0], ''))]


    for directory in project_directories:
        if "git" in directory[0]:
            continue
        expression = re.compile(re.escape(name_to_change), re.IGNORECASE)
        new_directory = expression.sub(new_project_name, directory[0])
        print "creating %s" % new_directory
        os.makedirs(new_directory)
        files = [os.path.join(directory[0], x) for x in directory[2]]
        for dir_file in files:
            new_filename = expression.sub(new_project_name, dir_file)
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
    expression = re.compile(re.escape(searchExp), re.IGNORECASE)
    x = [expression.sub(replaceExp, y) for y in old.readlines()]
    new = open(file, "w")
    new.writelines(x)
    new.close()
    old.close()



def start_app(new_app_name, source_project, dest_project, bundle_id):
    
    rename_project(source_project, new_app_name, bundle_id)
def render_into_fastlane(main_app_path, fastlane_file, params):

    info_file_path = os.path.join(main_app_path, 'fastlane', fastlane_file)
    app_info_file = open(info_file_path, "r")

    new_file = pystache.render(app_info_file.read(), params)

    app_info_file.close()

    new_info_file = open(info_file_path, "w+")
    new_info_file.write(new_file)
    new_info_file.close()



def command_line_controller():
        
    parser = ArgumentParser(description="Allows fast creation of Xcode projects that have a certain file structure and pre-loaded frameworks.")

    parser.add_argument('source_project', help="The source scaffolding project you wish to use.")


    arguments = parser.parse_args()
    
    try:
        config_path = os.path.join(os.path.dirname(__file__), "app_info.json")
        params = json.load(open(config_path)) 
    except IOError:
        params = {}

    defaults = params
    def get_input(message_string, key):
        message_defaults = message_string
        value = ""
        if key in defaults:
            value = defaults[key]
            message_defaults += "[%s]" % value
        val = raw_input(message_defaults) or value
        params[key] = val


    get_input('Bundle ID for app: ', 'bundle_id')
    get_input('Enter the main scheme name: ', 'scheme')
    get_input('App name: ', 'app_name')
    get_input('iTC Team ID: ', 'team_id')
    get_input('iTC Team name: ', 'team_name')
    get_input('iTC Username: ', 'itunes_username')
    params['app_language'] = "English"
    main_app_path = os.path.join(os.getcwd(), params['app_name'])

    start_app(params['app_name'], arguments.source_project, params['app_name'], params['bundle_id'])
    print "App %s created in %s" % (params['app_name'], params['app_name'])

    render_into_fastlane(main_app_path, 'Fastfile', params)
    render_into_fastlane(main_app_path, 'Appfile', params)

    do_initial_commit(main_app_path)
    
def do_initial_commit(main_app_path):
    os.environ["GIT_WORK_TREE"] = main_app_path
    os.environ["GIT_DIR"] = os.path.join(main_app_path, ".git")
    os.system("git init; git add -A; git commit -am 'Initial commit.'")
    del os.environ["GIT_WORK_TREE"] 


#    rename_project(arguments.directory, arguments.new_name)

def main():
    command_line_controller()   

if __name__ == '__main__':
    main()
