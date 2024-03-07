**Pilppa Kicad Lib DB Manager**

Python tool for integrating the list of pcb components bought from PCB warehouses like Digikey and Mouser to Kicad via DBLib driver that allows viewing them as a schematic symbols and pcb footprints.

This tool will work by parsing the CSV file of components that are ordered from warehouses like digikey or mouser. From digikey that file can be downloaed directly, while in mouser case you can download the excel file and then export that to CSV file with libraoffice or microsoft excel.

Data from imported CSV files are stored to sqlite3 database that can be then integrated to Kicad 8 library database.

This tool contains also the required pilppa_kicad_lib_db.kicad_dbl kicad configuration file which contains mapping instruction from database to sql.

**Usage Example:**

Following script will show how to import one digikey csv file and one mouser csv file to database and then integrate that to kicad 8.

1. csv file import to new sqlite database:
   
>    ./db_content_import_test.sh


2. open database
>sqlite3 test_sqlite3.db 	

3. view component list from database

>	sqlite> select * from components;
	
	will then so rows with following type of data in database table
	
> 1|HPH2-B-10-UA||||CONN HEADER VERT 10POS 1.27MM||||10|0.542||0
...

4. Install SQLITE odbc driver for your operating system. For ubuntu use command:

> sudo apt-get install libsqliteodbc unixodbc


5. Create new kicad project kicad8_test

6. Copy sqlite database and configuration files under kicad8_test project

> - cp pilppa_kicad_lib_db.kicad_dbl <path to kicad project>
> - cp pilppa_kicad_lib_db.sqlite <path to kicad project>


7. Open kicad project and configure driver

> - Select Kicad Menu/Preferences/Configure Symbol Libraries
> - Press + button
> - Set name to "Pilppa"
> - Set Library Format to Database
> - Press browse button and select pilppa_kicad_lib_db.kicad_dbl
> - Press ok to close the Symbol libraries dialog
> 
8. Test The component selection from the db library

> - Open schematics with Kicad
> - Press A button
> - List of components will be showed
> - Write 0402YC1 and component will be found from "Components/Pilppa category"
> 

**Additional Information**
configure kicad 8 to use the library db

https://www.youtube.com/watch?v=nZqoay-Yevk
