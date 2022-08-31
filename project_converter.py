import os
from project import *

# This script can be used to convert a HiBoP project from 3.x to 4.x
# Be sure to make a backup of your projects before using this script

# User Input
projects_directory = "C:\\Users\\Zigaroula\\Documents\\HBP\\Projects"

# Create directory
converted_dir = os.path.join(projects_directory, "converted")
if not os.path.isdir(converted_dir):
    os.mkdir(converted_dir)

# List project files in directory
project_files = [f for f in next(os.walk(projects_directory))[2] if f.endswith(".hibop")]

# Open each project and save it in the converted directory with the right 4.x format
for project_file in project_files:
    project = Project.load(os.path.join(projects_directory, project_file))
    project.save(converted_dir)
