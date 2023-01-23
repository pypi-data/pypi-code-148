# TODO add file without title reordering

import argparse
from importlib.metadata import version
import sys
import os
import json
import requests
import pandas as pd
import glob
import filetype
import shutil

def main():
	# parse arguments
	parser = argparse.ArgumentParser(description='Order Arrowverse episodes files in air time order.')
	parser.add_argument('-sm', '--skip-rename', action="store_true", default=False, help='skips rename of files')
	parser.add_argument('-dm', '--dry-run-rename', action="store_true", default=False, help='does not really rename files, just prints them (and then exits, equivalent to "mnamer --test")')
	parser.add_argument('-dr', '--dry-run-reorder', action="store_true", default=False, help='does not really reorder files, just prints them')
	parser.add_argument('-dest', '--destination-path', nargs='?', default="", type=str, help='destination folder')
	parser.add_argument('folders', action="extend", nargs='*', default=[], type=str, metavar='FOLDERS', help='folders to process')
	parser.add_argument('-V', '--version', action='version', version='%(prog)s '+version("arrowverse_reorderer"))
	args= parser.parse_args()

	# if no folders are given, use current directory
	folders= args.folders
	if folders==[]:
		folders.append(os.getcwd())

	for folder in folders:
		if not os.path.exists(folder):
			print("Folder "+folder+" does not exist")
			sys.exit(1)

	# if no destination folder is given, use current directory
	name_dest_folder="reordered"
	if args.destination_path!="":
		name_dest_folder= os.path.basename(args.destination_path)

	# rename files with mnamer
	if (not args.skip_rename) and (not args.dry_run_rename) :
		for folder in folders:
			os.system("mnamer -b -r --no-guess --no-overwrite --episode-format=\"{series} - S{season:02}E{episode:02} - {title}{extension}\" --ignore=\"(\\\\"+name_dest_folder+"\\\\)|(\/"+name_dest_folder+"\/)\" "+folder)
	elif (not args.skip_rename) and args.dry_run_rename :
		for folder in folders:
			os.system("mnamer -b -r --no-guess --no-overwrite --episode-format=\"{series} - S{season:02}E{episode:02} - {title}{extension}\" --ignore=\"(\\\\"+name_dest_folder+"\\\\)|(\/"+name_dest_folder+"\/)\" --test "+folder)
			return 0	# exit after dry run
	else :
		print("Skipping rename")

	# reorder files
	destination_path=args.destination_path
	if destination_path=="":
		destination_path= os.path.join(os.getcwd(),name_dest_folder)
	reorder(folders, name_dest_folder, destination_path, args.dry_run_reorder)

	return 0

"""
from	Series - SXXEXX - Title.*
to	000 - Series - SXXEXX - Title.*

get arrowverse order from website
get all filenames
move them to another directory and rename them by prepending "#" column to old filename getting it from the line Series and Title
"""
def reorder(folders, name_dest_folder, destination_path, dry_run=False):
	# set and create destination folder
	if not os.path.exists(destination_path):
		os.makedirs(destination_path)

	# get Arrowverse order from website
	url= "https://arrowverse.info"
	df= pd.read_html(requests.get(url).content)[-1]
	del df["Original Air Date"]
	del df["Source"]

	# for each file in directories, move to new directory
	for folder in folders:
		for file in glob.glob(os.path.join(folder,"**"), recursive=True):
			# if file is a video
			if (os.path.isfile(file) and not name_dest_folder in file) and (filetype.is_video(file) and len(os.path.basename(file).split(" - "))==3):	# if file is a video and its name is in the format * - * - *
				series= os.path.basename(file).split(" - ")[0]
				episode= os.path.basename(file).split(" - ")[1]
				end= os.path.basename(file).split(" - ")[2]
				
				row_df= df.loc[(df['Series'] == series) & (df['Episode'] == episode)]
				row= json.loads(row_df.to_json(orient="records"))[0]
				number= str(row['#']).zfill(3)

				if not dry_run:
					shutil.move(file, os.path.join(destination_path, number+" - "+series+" - "+episode+" - "+end))
				print(file+" moved")
		

		# if (sub)folder is empty, delete it
		for subfolder in os.listdir(folder):
			if len(os.listdir(subfolder))==0:
				os.rmdir(subfolder)
				print("Folder "+subfolder+" deleted\n")
		if len(os.listdir(folder))==0:
			os.rmdir(folder)
			print("Folder "+folder+" deleted\n")

if __name__ == '__main__':
	sys.exit(main())