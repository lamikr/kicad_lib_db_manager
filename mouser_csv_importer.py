import sys
import os
import csv
from datetime import datetime
from kicad_lib_db_handler import *

def mouser_date_to_numeric_year_month_day_date(date_str: str):
    source_format = "%d-%b-%y"
    destination_format = "%Y%m%d"
    d = datetime.strptime(date_str, source_format)
    return d.strftime(destination_format)

def main():
	database = r"test_sqlite3.db"
	
	print('argument list', sys.argv)
	csv_fname = sys.argv[1	]
	print("csv file: {}".format(csv_fname))

	# create a database connection
	conn = create_connection(database)
	kicad_lib_db_init(conn)

	csv_file = open(csv_fname, "r")
	reader = csv.reader(csv_file, delimiter=',')
	ii=0
	jj=0
	for row in reader:
		if (ii == 0):
			print(row)
			#for column in row:
			#	print(column)
			#	jj += 1
			ii += 1

	print("1")
	csv_file = open(csv_fname, "r")
	dict_reader = csv.DictReader(csv_file, delimiter=',')
	print("2")
	for row in dict_reader:
		print(row['Order Qty.'])
		print(mouser_date_to_numeric_year_month_day_date(row['Date']))
		mpn=row['Mfr. #:']
		cmp_type=''
		cmp_symbols=''
		value_title=''
		value=''
		footprints=''
		quantity_txt=row['Order Qty.']
		# todo handle int convertion errors and empty strings, etc...
		quantity=int(quantity_txt)
		desc=row['Desc.:']
		desc_lowercase=desc.lower()
		sz2='0201'
		if 'capacitor' in desc_lowercase:
			cmp_type='Capacitor'
			cmp_symbols='Device:C'
			value_title="Capacitance"
			'''
			if '0201' in desc_lowercase():
				footprints='Resistor_SMD:R_0201_0603Metric'
			if '0402' in desc_lowercase():
				footprints='Resistor_SMD:R_0402_1005Metric'
			if '0603' in desc_lowercase():
				footprints='Resistor_SMD:R_0603_1608Metric'
			if '0805' in desc_lowercase():
				footprints='Resistor_SMD:R_0805_2012Metric'
			'''
		if 'resistor' in desc_lowercase:
			cmp_type='Resistor'
			cmp_symbols='Device:R'
			value_title="Resistance"
			'''
			if '0201' in desc_lowercase():
				footprints='Resistor_SMD:R_0201_0603Metric'
			if '0402' in desc_lowercase():
				footprints='Resistor_SMD:R_0402_1005Metric'
			if '0603' in desc_lowercase():
				footprints='Resistor_SMD:R_0603_1608Metric'
			if '0805' in desc_lowercase():
				footprints='Resistor_SMD:R_0805_2012Metric'
			'''
		kicad_lib_db_add_data(conn, mpn, cmp_type, cmp_symbols, value_title, value, footprints, quantity)
	
if __name__ == '__main__':
    main()


