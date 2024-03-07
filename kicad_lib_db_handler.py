#
# Copyright (c) 2024 by Mika Laitio <lamikr@gmail.com>
#
# License: GNU Lesser General Public License (LGPL), version 2.1 or later.
# See the lgpl.txt file in the root directory or <http://www.gnu.org/licenses/lgpl-2.1.html>.
#

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	ret = True
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit();
	except Error as e:
		ret = False
		print(e)
	return ret;

def kicad_lib_db_init(conn):
	ret = True
	sql_create_components_table = """ CREATE TABLE IF NOT EXISTS "Components" (
										"ID" INTEGER PRIMARY KEY ,
                                        "MPN" TEXT UNIQUE,
                                        "CMP_Type" TEXT,
                                        "Value_Type" TEXT,
                                        "Value" TEXT,
                                        "Description" TEXT,
                                        "Manufacturer" TEXT,
                                        "Symbols" TEXT,
                                        "Footprints" TEXT,
                                        "Quantity" INTEGER DEFAULT 0,
										"Unit_Price" TEXT,
                                        "Update_Date" TEXT,
                                        "Verified_Date" INTEGER DEFAULT 0
                                    ); """
                                    
	# create tables
	if conn is not None:
		# create projects table
		ret = create_table(conn, sql_create_components_table)
	else:
		ret	= False;
		print("Error! cannot create the database connection.")
	return ret;

def kicad_lib_db_add_data(conn,
						mpn,
						cmp_type,
						value_type,
						value,
						description,
						manufacturer,
						cmp_symbols,
						footprint_list,
						unit_price,
						quantity):
	# insert first the MPN only in case it does not yet exist
	sql = ''' INSERT INTO COMPONENTS (mpn) SELECT ? WHERE NOT EXISTS (SELECT mpn FROM COMPONENTS WHERE mpn = ?)'''
	conn.execute(sql, (mpn, mpn))
	
	# then start updating the values from other fields only in case they are NULL and new value is not null
	# this prevent us overwriting values that user may have modified by using some other tool	
	sql = ''' UPDATE components SET CMP_Type = COALESCE(dt2.CMP_Type, ?), Value_Type = COALESCE(dt2.Value_Type, ?), Value = COALESCE(dt2.Value, ?), Description = COALESCE(dt2.Description, ?), Manufacturer = COALESCE(dt2.Manufacturer, ?), Symbols = COALESCE(dt2.Symbols, ?), Footprints = COALESCE(dt2.Footprints, ?), Unit_Price = COALESCE(dt2.Unit_Price, ?) FROM Components dt2 WHERE Components.MPN = ? AND dt2.MPN = ?'''
	conn.execute(sql, (cmp_type, value_type, value, description, manufacturer, cmp_symbols, footprint_list, unit_price, mpn, mpn))
	
	# update quantity field separately by adding the quantity to existing quantity
	sql = ''' UPDATE components SET quantity = quantity + ? WHERE mpn = ?'''
	conn.execute(sql, (quantity, mpn))
	
	# update numeric price field separately if it is non-zero
	#sql = ''' UPDATE components SET unit_price = ? WHERE unit_price = 0 and mpn = ?'''
	#conn.execute(sql, (unit_price, mpn))

	conn.commit()
