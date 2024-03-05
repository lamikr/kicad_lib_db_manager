import sys
import os
import csv
import parameter_parser_common
from datetime import datetime
from kicad_lib_db_handler import *
from parameter_parser_common import *
from enum import Enum

class ENUM_DIGIKEY_HEADER1_INDEX(Enum):
	INDEX = 0
	DIGIKEY_PART_NUMBER = 1
	MANUF_PART_NUMBER = 2
	DESCRIPTION = 3
	PCB_ASSIGNMENT_TAG = 4
	ORDER_QTY = 5
	ORDER_QTY_BACKORDER = 6
	PRICE_USD = 7
	EXT_USD = 8

m_digikey_header1_arr = ['\ufeffIndex', 'DigiKey Part #', 'Manufacturer Part Number', 'Description', 'Customer Reference', 'Quantity', 'Backorder', 'Unit Price', 'Extended Price']

def get_digikey_header_by_index(hdr_index):
	try:
		return m_digikey_header1_arr[hdr_index]
	except IndexError:
		return None

def is_digikey_header_column_available(hdr_row, hdr_index):
	try:
		key_str = m_digikey_header1_arr[hdr_index]
		#print(key_str)
		val_str = hdr_row[hdr_index]
		#print(val_str)
		return (key_str==val_str)
	except IndexError:
		return False

def is_csv_header_digikey(hdr_row):
	res = is_digikey_header_column_available(hdr_row, ENUM_DIGIKEY_HEADER1_INDEX.MANUF_PART_NUMBER.value)
	if (res == True):
		res = is_digikey_header_column_available(hdr_row, ENUM_DIGIKEY_HEADER1_INDEX.DESCRIPTION.value)
		if (res == True):
			res = is_digikey_header_column_available(hdr_row, ENUM_DIGIKEY_HEADER1_INDEX.ORDER_QTY.value)
			if (res == True):
				return True
	return False
	
def parse_component_mpn_digikey(row):
	print(row)
	key_str=get_digikey_header_by_index(ENUM_DIGIKEY_HEADER1_INDEX.MANUF_PART_NUMBER.value)
	return row[key_str]
	
def parse_component_order_qty_digikey(row):
	qty_txt	= ''
	try:
		key_str=get_digikey_header_by_index(ENUM_DIGIKEY_HEADER1_INDEX.ORDER_QTY.value)
		qty_txt = row[key_str]
		return int(qty_txt)
	except ValueError:
		print("ERROR")
		print("ERROR")
		print("ERROR")
		print(qty_txt);
		print(row);
		return 0

def parse_component_description_digikey(row):	
	key_str = get_digikey_header_by_index(ENUM_DIGIKEY_HEADER1_INDEX.DESCRIPTION.value)
	return row[key_str]
	
def parse_component_type_enum_digikey(db__desc):
	ret = ENUM_COMPONENT_TYPE.UNKNOWN
	if db__desc.startswith("CAP"):
		ret = ENUM_COMPONENT_TYPE.CAPACITOR
	elif db__desc.startswith("RES"):
		ret = ENUM_COMPONENT_TYPE.RESISTOR
	elif db__desc.startswith("LED"):
		ret = ENUM_COMPONENT_TYPE.LED
	elif db__desc.startswith("FIXED IND"):
		ret = ENUM_COMPONENT_TYPE.INDUCTOR
	elif db__desc.startswith("DIODE"):
		ret = ENUM_COMPONENT_TYPE.DIODE
	elif db__desc.startswith("SENSOR PHOTODIODE"):
		ret = ENUM_COMPONENT_TYPE.DIODE
	elif db__desc.startswith("IC"):
		ret = ENUM_COMPONENT_TYPE.IC
	elif db__desc.startswith("CONN HEADER"):
		ret = ENUM_COMPONENT_TYPE.CONNECTOR
	elif db__desc.startswith("PIN HEADER"):
		ret = ENUM_COMPONENT_TYPE.CONNECTOR
	return ret
	
def parse_component_value_digikey(enum_cmp_type, db__desc):
	res = None
	ret = None

	if enum_cmp_type == ENUM_COMPONENT_TYPE.CAPACITOR:
		regex1 = rf"({regex_any_number})(UF|PF|NF)"
		res = re.search(regex1, db__desc)
	elif enum_cmp_type == ENUM_COMPONENT_TYPE.RESISTOR:
		regex1 = rf"({regex_any_number})( OHM|K OHM|M OHM)"
		res = re.search(regex1, db__desc)
	elif enum_cmp_type == ENUM_COMPONENT_TYPE.INDUCTOR:
		regex1 = rf"({regex_any_number})( UH|NH|PH)"
		res = re.search(regex1, db__desc)
	elif enum_cmp_type == ENUM_COMPONENT_TYPE.LED:
		db_desc_low = db__desc.lower()
		if ("red" in db_desc_low):
			ret = "red"
		elif ("green" in db_desc_low):
			ret = "green"
		elif ("blue" in db_desc_low):
			ret = "blue"
		elif ("yellow" in db_desc_low):
			ret = "white"
		elif ("irda" in db_desc_low):
			ret = "irda"
		elif ("white" in db_desc_low):
			ret = "white"
	if (res and res.group(0) is not None):
		ret = res.group(0)
		ret = ret.removesuffix(' OHM')
		print(ret)
	return ret
