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
        conn.commit();
    except Error as e:
        print(e)


def kicad_lib_db_init(conn):
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
                                        last_update_date TEXT,
                                        verified INTEGER DEFAULT 0,
                                        price numeric
                                    ); """	
	# create tables
	if conn is not None:
		# create projects table
		create_table(conn, sql_create_components_table)
	else:
		print("Error! cannot create the database connection.")

def kicad_lib_db_add_data(conn, mpn, cmp_type, value_type, value, description, manufacturer, cmp_symbols, footprint_list, quantity):
	# INSERT INTO COMPONENTS (mpn, quantity) SELECT 'b', 30 WHERE NOT EXISTS (SELECT mpn FROM COMPONENTS WHERE mpn = 'b');
	#sql = ''' INSERT INTO components(mpn, type, symbols, value_type, value, description, footprints)
    #          VALUES(?,?,?,?,?,?,?,?) on CONFLICT(MPN) DO UPDATE SET type=excluded.type, symbols=excluded.symbols, value_type=excluded.value_type, value=excluded.value, description=excluded.description, footprints=excluded.footprints WHERE true'''
	#conn.execute(sql, (mpn, cmp_type, cmp_symbols, value_type, value, description, footprint_list, quantity))

	# insert first the MPN only in case it does not yet exist
	sql = ''' INSERT INTO COMPONENTS (mpn) SELECT ? WHERE NOT EXISTS (SELECT mpn FROM COMPONENTS WHERE mpn = ?)'''
	conn.execute(sql, (mpn, mpn))
	# then start updating the values from other fields only in case they are NULL and new value is not null
	# this prevent us overwriting values that user may have modified by using some other tool
	
	sql = ''' UPDATE components SET type = COALESCE(dt2.type, ?), value_type = COALESCE(dt2.value_type, ?), value = COALESCE(dt2.value, ?), description = COALESCE(dt2.description, ?), manufacturer = COALESCE(dt2.manufacturer, ?), symbols = COALESCE(dt2.symbols, ?), footprints = COALESCE(dt2.footprints, ?) FROM components dt2 WHERE components.mpn = ? AND dt2.mpn = ?'''
	conn.execute(sql, (cmp_type, value_type, value, description, manufacturer, cmp_symbols, footprint_list, mpn, mpn))
	
	sql = ''' UPDATE components SET quantity = quantity + ? WHERE mpn = ?'''
	conn.execute(sql, (quantity, mpn))

	
	#sql = ''' UPDATE COMPONENTS SET type=COALESCE(ex.type, ?), symbols=COALESCE(ex.symbols, ?), value_type=COALESCE(ex.value_type, ?), value=IFNULL(ex.value, ?), description=IFNULL(ex.description, ?), footprints=IFNULL(ex.footprints, ?) where MPN=? FROM COMPONENTS ex WHERE ex.MPN=?'''
	#conn.execute(sql, (cmp_type, cmp_symbols, value_type, value, description, footprint_list, mpn, mpn))	
	
	#sql = ''' INSERT INTO components(mpn) values("1")'''
	#conn.execute(sql)
	conn.commit()
