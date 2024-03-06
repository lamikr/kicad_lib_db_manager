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
	sql_create_components_table = """ CREATE TABLE IF NOT EXISTS components (
										id INTEGER PRIMARY KEY ,
                                        mpn TEXT UNIQUE,
                                        type TEXT,
                                        value_type TEXT,
                                        value TEXT,
                                        description TEXT,
                                        manufacturer TEXT,
                                        symbols TEXT,
                                        footprints TEXT,
                                        quantity INTEGER DEFAULT 0,
										unit_price numeric DEFAULT 0,
                                        last_update_date TEXT,
                                        verified INTEGER DEFAULT 0
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
	sql = ''' UPDATE components SET type = COALESCE(dt2.type, ?), value_type = COALESCE(dt2.value_type, ?), value = COALESCE(dt2.value, ?), description = COALESCE(dt2.description, ?), manufacturer = COALESCE(dt2.manufacturer, ?), symbols = COALESCE(dt2.symbols, ?), footprints = COALESCE(dt2.footprints, ?), unit_price = COALESCE(dt2.unit_price, ?) FROM components dt2 WHERE components.mpn = ? AND dt2.mpn = ?'''
	conn.execute(sql, (cmp_type, value_type, value, description, manufacturer, cmp_symbols, footprint_list, unit_price, mpn, mpn))
	
	# update quantity field separately by adding the quantity to existing quantity
	sql = ''' UPDATE components SET quantity = quantity + ? WHERE mpn = ?'''
	conn.execute(sql, (quantity, mpn))
	
	# update quantity field separately by adding the quantity to existing quantity
	sql = ''' UPDATE components SET unit_price = ? WHERE unit_price = 0 and mpn = ?'''
	conn.execute(sql, (unit_price, mpn))

	conn.commit()
