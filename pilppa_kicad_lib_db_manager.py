#
# Copyright (c) 2024 by Mika Laitio <lamikr@gmail.com>
#
# License: GNU Lesser General Public License (LGPL), version 2.1 or later.
# See the lgpl.txt file in the root directory or <http://www.gnu.org/licenses/lgpl-2.1.html>.
#

import sys
import os
import csv
from datetime import datetime
from kicad_lib_db_handler import *
from csv_import import *
from parameter_parser_common import *

def printout_version_info():
	print("    pilppa_kicad_lib_db_manager")
	print("        version: 20240306_1")

def printout_help():
	print("    This tool can be used to import digikey or mouser csv files to kicad lib db format.")
	print("    usage:")
	print("        python ./pilppa_kicad_lib_db_manager.py -h ")
	print("        python ./pilppa_kicad_lib_db_manager.py -v")
	print("        python ./pilppa_kicad_lib_db_manager.py -f <digikey_order_20240306.csv>")
	
def printout_version_info_and_help():
	printout_version_info()
	printout_help()

def main():
	sqlite_database_fname = r"pilppa_kicad_lib_db.sqlite"
	
	if (len(sys.argv) >= 2):
		if (len(sys.argv) == 2):
			if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
				printout_version_info_and_help()	
			elif (sys.argv[1] == '-v' or sys.argv[1] == '--version'):
				printout_version_info()
			else:
				printout_version_info_and_help()
		elif (len(sys.argv) == 3):
			if (sys.argv[1] == '-f'):
				err_flg = False
				try:
					csv_fname = sys.argv[2]
					csv_file = open(csv_fname, "r")
				except IOError as err:
					err_flg = True
					print("    Error opening csv file: {0}: {1}".format(csv_fname, err))

				if (err_flg == False):
					# create a database connection
					db__conn = create_connection(sqlite_database_fname)
					if (db__conn != None):
						res = kicad_lib_db_init(db__conn)
						if (res == True):
							res = get_component_wareshouse_by_csv_file(csv_file)
							if (res != ENUM_COMPONENT_WAREHOUSE.UNKNOWN):
								csv_file.close()
								print("Importing pcb component CSV file: {}".format(csv_fname))
								csv_file = open(csv_fname, "r")
								csv_import(res, csv_file, db__conn)
								csv_file.close()
								db__conn.close()
								print("Finished importing CSV file")
							else:
								print("    Unrecognized CSV file format: {0}".format(csv_file))
						else:
							print("    Failed to init and write to sqlite database file: {0}".format(sqlite_database_fname))
					else:
						print("    Failed to open sqlite database file: {0}".format(sqlite_database_fname))
			else:
				printout_version_info_and_help()
		else:
			printout_version_info_and_help()
	else:
		printout_version_info_and_help()
	
if __name__ == '__main__':
    main()
