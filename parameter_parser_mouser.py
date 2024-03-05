import sys
import os
import csv
import parameter_parser_common
from datetime import datetime
from kicad_lib_db_handler import *
from parameter_parser_common import *
from enum import Enum

class ENUM_MOUSER_HEADER1_INDEX(Enum):
	SALES_ORDER = 0
	WEB_ORDER = 1
	PO_NUMBER = 2
	LINE_NUMBER = 3
	ORDER_DATE = 4
	ORDER_STATUS = 5
	MOUSER_PROD_NUMBER = 6
	MANUF_PROD_NUMBER = 7
	DESCRIPTION = 8
	PCB_ASSIGNMENT_TAG = 9
	ORDER_QTY = 10
	EXT_USD = 11
	PRICE_USD = 12
	STATUS = 13
	DELIVERY_DATE = 14
	INVOICE_NUMBER = 15

m_mouser_header1_arr = ['Sales Order #:', 'Web Order #:', 'PO Number:', 'Line No.', 'Order Date:', 'Order Status:', 'Mouser #:', 'Mfr. #:', 'Desc.:', 'Customer #', 'Order Qty.', 'Ext. (USD)', 'Price (USD)', 'Status', 'Date', 'Invoice #']

def mouser_date_to_numeric_year_month_day_date(date_str: str):
    source_format = "%d-%b-%y"
    destination_format = "%Y%m%d"
    d = datetime.strptime(date_str, source_format)
    return d.strftime(destination_format)

def get_mouser_header_by_index(hdr_index):
	try:
		return m_mouser_header1_arr[hdr_index]
	except IndexError:
		return None

def is_mouser_header_column_available(hdr_row, hdr_index):
	try:
		key_str = m_mouser_header1_arr[hdr_index]
		#print(key_str)
		val_str = hdr_row[hdr_index]
		#print(val_str)
		return (key_str==val_str)
	except IndexError:
		return False

def is_csv_header_mouser(hdr_row):
	res = is_mouser_header_column_available(hdr_row, ENUM_MOUSER_HEADER1_INDEX.MANUF_PROD_NUMBER.value)
	if (res == True):
		res = is_mouser_header_column_available(hdr_row, ENUM_MOUSER_HEADER1_INDEX.DESCRIPTION.value)
		if (res == True):
			res = is_mouser_header_column_available(hdr_row, ENUM_MOUSER_HEADER1_INDEX.ORDER_QTY.value)
			if (res == True):
				return True
	return False
	
def parse_component_mpn_mouser(row):
	print(row)
	key_str=get_mouser_header_by_index(ENUM_MOUSER_HEADER1_INDEX.MANUF_PROD_NUMBER.value)
	return row[key_str]
	
def parse_component_order_qty_mouser(row):
	key_str=get_mouser_header_by_index(ENUM_MOUSER_HEADER1_INDEX.ORDER_QTY.value)
	qty_txt = row[key_str]
	return int(qty_txt)

def parse_component_description_mouser(row):	
	key_str = get_mouser_header_by_index(ENUM_MOUSER_HEADER1_INDEX.DESCRIPTION.value)
	return row[key_str]
	
def parse_component_type_enum_mouser(db__desc):
	ret = ENUM_COMPONENT_TYPE.UNKNOWN
	desc_lwrc = db__desc.lower()
	if 'capacitor' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.CAPACITOR
	elif 'resistor' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.RESISTOR
	elif ' led ' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.LED
	elif 'diode' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.DIODE
	elif 'inductor' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.INDUCTOR
	elif 'connector' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.CONNECTOR
	elif 'header' in desc_lwrc:
		ret = ENUM_COMPONENT_TYPE.CONNECTOR
	return ret
	
def parse_component_value_mouser(enum_cmp_type, db__desc):
	res = None
	ret = None

	if enum_cmp_type == ENUM_COMPONENT_TYPE.CAPACITOR:
		regex1 = rf"({regex_any_number})(uF|pF|nF)"
		res = re.search(regex1, db__desc)
	elif enum_cmp_type == ENUM_COMPONENT_TYPE.RESISTOR:
		regex1 = rf"({regex_any_number})(ohms|Kohms|Mohms)"
		res = re.search(regex1, db__desc)
	elif enum_cmp_type == ENUM_COMPONENT_TYPE.INDUCTOR:
		regex1 = rf"({regex_any_number})(uH|nH|pH)"
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
	# check if regexp found matching value and store it to string
	if (res and res.group(0) is not None):
		ret = res.group(0)
		ret = ret.removesuffix('ohms')
		#print(ret)
	return ret
