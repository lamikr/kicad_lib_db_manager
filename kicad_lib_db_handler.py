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
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def kicad_lib_db_init(conn):
	
	'''
	sql_create_components_table = """ CREATE TABLE IF NOT EXISTS "Components" (
        MPN TEXT PRIMARY KEY,
		Type TEXT,
		Manufacturer TEXT,
		Symbols TEXT,
		Value_tittle TEXT,
		Value TEXT,
		Description TEXT,
		Footprints TEXT,
		Quantity_own TEXT,
		Last_update_date TEXT,
		Verified INTEGER DEFAULT 0,
		Cost numeric,
		Mass double,
    );"""
	'''
	sql_create_components_table = """ CREATE TABLE IF NOT EXISTS components (
                                        mpn TEXT PRIMARY KEY,
                                        type TEXT,
                                        manufacturer TEXT,
                                        symbols TEXT,
                                        Value_title TEXT,
                                        value TEXT,
                                        description TEXT,
                                        footprints TEXT,
                                        quantity INTEGER DEFAULT 0,
                                        last_update_date TEXT,
                                        verified INTEGER DEFAULT 0,
                                        Cost numeric,
                                        Mass double
                                    ); """	
	# create tables
	if conn is not None:
		# create projects table
		create_table(conn, sql_create_components_table)
	else:
		print("Error! cannot create the database connection.")

def kicad_lib_db_add_data(conn, mpn, cmp_type, cmp_symbols, value_title, value, footprints, quantity):
	sql = ''' INSERT INTO components(mpn, type, symbols, value_title, value, footprints, quantity)
              VALUES(?,?,?,?,?,?,?) on CONFLICT(MPN) DO UPDATE SET type=excluded.type, symbols=excluded.symbols, value_title=excluded.value_title, value=excluded.value, footprints=excluded.footprints, quantity=excluded.quantity WHERE true'''
	conn.execute(sql, (mpn, cmp_type, cmp_symbols, value_title, value, footprints, quantity))
	#sql = ''' INSERT INTO components(mpn) values("1")'''
	#conn.execute(sql)
	conn.commit()
