from enum import Enum
import csv
import os
import re
from parameter_parser_mouser import *
from parameter_parser_digikey import *

def get_component_wareshouse_by_csv_file(csv_file):
	ret = ENUM_COMPONENT_WAREHOUSE.UNKNOWN
	
	reader = csv.reader(csv_file, delimiter=',')
	hdr_row = next(reader);	#get the first line
	print(hdr_row)
	res = is_csv_header_mouser(hdr_row)
	if (res == True):
		ret = ENUM_COMPONENT_WAREHOUSE.MOUSER
	else:
		res = is_csv_header_digikey(hdr_row)
		if (res == True):
			ret = ENUM_COMPONENT_WAREHOUSE.DIGIKEY
	return ret

def parse_component_type(description):
	print(description)

def parse_component_footprint(cmp_type, description):
	print(cmp_type)
	
def csv_import(res, csv_file, db__conn):
	print("csv_import started")

	if ((res == ENUM_COMPONENT_WAREHOUSE.DIGIKEY) or (res == ENUM_COMPONENT_WAREHOUSE.MOUSER)):
		enum_cmp_type = ENUM_COMPONENT_TYPE.UNKNOWN
		dict_reader = csv.DictReader(csv_file, delimiter=',')
		for row in dict_reader:
			db__cmp_type=''
			db__cmp_symbols=''
			db__val_type=''
			db__val=''
			db__footprint_list=''
			if (res == ENUM_COMPONENT_WAREHOUSE.DIGIKEY):
				db__mpn = parse_component_mpn_digikey(row)
				db__quantity = parse_component_order_qty_digikey(row)
				db__desc = parse_component_description_digikey(row)
				enum_cmp_type = parse_component_type_enum_digikey(db__desc)
				db__val = parse_component_value_digikey(enum_cmp_type, db__desc)
			elif (res == ENUM_COMPONENT_WAREHOUSE.MOUSER):
				db__mpn = parse_component_mpn_mouser(row)
				db__quantity = parse_component_order_qty_mouser(row)
				db__desc = parse_component_description_mouser(row)
				enum_cmp_type = parse_component_type_enum_mouser(db__desc)
				db__val = parse_component_value_mouser(enum_cmp_type, db__desc)
			
			if enum_cmp_type == ENUM_COMPONENT_TYPE.CAPACITOR:
				db__cmp_type='Capacitor'
				db__cmp_symbols='Device:C'
				db__val_type="${Capacitance}"
				if '0201' in db__desc:
					db__footprint_list='Capacitor_SMD:C_0201_0603Metric'
				if '0402' in db__desc:
					db__footprint_list='Capacitor_SMD:C_0402_1005Metric'
				if '0603' in db__desc:
					db__footprint_list='Capacitor_SMD:C_0603_1608Metric'
				if '0805' in db__desc:
					db__footprint_list='Capacitor_SMD:C_0805_2012Metric'
				if '1206' in db__desc:
					db__footprint_list='Capacitor_SMD:C_1206_3216Metric'
				if '1210' in db__desc:
					db__footprint_list='Capacitor_SMD:C_1210_3225Metric'
				if '1812' in db__desc:
					db__footprint_list='Capacitor_SMD:C_1812_3246Metric'
				if '2010' in db__desc:
					db__footprint_list='Capacitor_SMD:C_2010_5025Metric'
				if '2512' in db__desc:
					db__footprint_list='Capacitor_SMD:C_2512_6332Metric'
			if enum_cmp_type == ENUM_COMPONENT_TYPE.RESISTOR:
				db__cmp_type='Resistor'
				db__cmp_symbols='Device:R'
				db__val_type="${Resistance}"
				if '0201' in db__desc:
					db__footprint_list='Resistor_SMD:R_0201_0603Metric'
				if '0402' in db__desc:
					db__footprint_list='Resistor_SMD:R_0402_1005Metric'
				if '0603' in db__desc:
					db__footprint_list='Resistor_SMD:R_0603_1608Metric'
				if '0805' in db__desc:
					db__footprint_list='Resistor_SMD:R_0805_2012Metric'
				if '1206' in db__desc:
					db__footprint_list='Resistor_SMD:R_1206_3216Metric'
				if '1210' in db__desc:
					db__footprint_list='Resistor_SMD:R_1210_3225Metric'
				if '1812' in db__desc:
					db__footprint_list='Resistor_SMD:R_1812_3246Metric'
				if '2010' in db__desc:
					db__footprint_list='Resistor_SMD:R_2010_5025Metric'
				if '2512' in db__desc:
					db__footprint_list='Resistor_SMD:R_2512_6332Metric'
			if enum_cmp_type == ENUM_COMPONENT_TYPE.INDUCTOR:
				db__cmp_type='Inductor'
				db__cmp_symbols='Device:L'
				db__val_type="${Inductance}"
				if '0201' in db__desc:
					db__footprint_list='Inductor_SMD:L_0201_0603Metric'
				if '0402' in db__desc:
					db__footprint_list='Inductor_SMD:L_0402_1005Metric'
				if '0603' in db__desc:
					db__footprint_list='Inductor_SMD:L_0603_1608Metric'
				if '0805' in db__desc:
					db__footprint_list='Inductor_SMD:L_0805_2012Metric'
				if '1206' in db__desc:
					db__footprint_list='Inductor_SMD:L_1206_3216Metric'
				if '1210' in db__desc:
					db__footprint_list='Inductor_SMD:L_1210_3225Metric'
				if '1812' in db__desc:
					db__footprint_list='Inductor_SMD:L_1812_3246Metric'
				if '2010' in db__desc:
					db__footprint_list='Inductor_SMD:L_2010_5025Metric'
				if '2512' in db__desc:
					db__footprint_list='Inductor_SMD:L_2512_6332Metric'
			if enum_cmp_type == ENUM_COMPONENT_TYPE.LED:
				db__cmp_type='LED'
				db__cmp_symbols='Device:LED'
				db__val_type="Color"
				if '0201' in db__desc:
					db__footprint_list='LED_SMD:LED_0201_0603Metric'
				if '0402' in db__desc:
					db__footprint_list='LED_SMD:LED_0402_1005Metric'
				if '0603' in db__desc:
					db__footprint_list='LED_SMD:LED_0603_1608Metric'
				if '0805' in db__desc:
					db__footprint_list='LED_SMD:LED_0805_2012Metric'
				if '1206' in db__desc:
					db__footprint_list='LED_SMD:LED_1206_3216Metric'
				if '1210' in db__desc:
					db__footprint_list='LED_SMD:LED_1210_3225Metric'
				if '1812' in db__desc:
					db__footprint_list='LED_SMD:LED_1812_3246Metric'
				if '2010' in db__desc:
					db__footprint_list='LED_SMD:LED_2010_5025Metric'
				if '2512' in db__desc:
					db__footprint_list='LED_SMD:LED_2512_6332Metric'
			if enum_cmp_type == ENUM_COMPONENT_TYPE.DIODE:
				db__cmp_type='Diode'
				db__cmp_symbols='Device:D'
				db__val_type="Voltage"
				if '0201' in db__desc:
					db__footprint_list='Diode_SMD:D_0201_0603Metric'
				if '0402' in db__desc:
					db__footprint_list='Diode_SMD:D_0402_1005Metric'
				if '0603' in db__desc:
					db__footprint_list='Diode_SMD:D_0603_1608Metric'
				if '0805' in db__desc:
					db__footprint_list='Diode_SMD:D_0805_2012Metric'
				if '1206' in db__desc:
					db__footprint_list='Diode_SMD:D_1206_3216Metric'
				if '1210' in db__desc:
					db__footprint_list='Diode_SMD:D_1210_3225Metric'
				if '1812' in db__desc:
					db__footprint_list='Diode_SMD:D_1812_3246Metric'
				if '2010' in db__desc:
					db__footprint_list='Diode_SMD:D_2010_5025Metric'
				if '2512' in db__desc:
					db__footprint_list='Diode_SMD:D_2512_6332Metric'
			print(db__mpn)
			kicad_lib_db_add_data(db__conn,
							db__mpn, db__cmp_type, db__cmp_symbols, db__val_type, db__val, db__desc, db__footprint_list, db__quantity)
	else:
		print("Error, csv file format not recognized")
