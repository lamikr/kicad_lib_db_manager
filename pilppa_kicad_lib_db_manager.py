import sys
import os
import csv
from datetime import datetime
from kicad_lib_db_handler import *
from csv_import import *

def main():
	database = r"pilppa_kicad_lib_db.sqlite"
	
	print('argument list', sys.argv)
	csv_fname = sys.argv[1]
	print("csv file: {}".format(csv_fname))
	
	# create a database connection
	db__conn = create_connection(database)
	kicad_lib_db_init(db__conn)

	csv_file = open(csv_fname, "r")
	res = get_component_wareshouse_by_csv_file(csv_file)
	csv_file.close()
	csv_file = open(csv_fname, "r")
	csv_import(res, csv_file, db__conn)
	csv_file.close()
	db__conn.close()
	
if __name__ == '__main__':
    main()