Purpose of this tool/scripts is to help managing the list of own pcb components.

When components are ordered from warehouses like digikey or mouser, customer will receive a CSV or excel file which contains
the list of components ordered. This tool will parse those CSV files and import the data to sqlite database.

Kicad 8 can then be configured to use the components listed in that database when creating PCB schematics or routing.

This is very initial proof of concept version that can parse the mouser csv file. Sample CSV files are included:
Usage:

1. csv file import to new sqlite database:
   
>    python ./mouser_csv_importer.py component_orders/mouser/mouser_2024_01_31.csv


2. open database
>sqlite3 test_sqlite3.db 	

3. view component list from database

>	sqlite> select * from components;
	
	0402YC102K4T4A|Capacitor||Device:C|Capacitance||||100||0||
	CRCW04021K50JNED|Resistor||Device:R|Resistance||||100||0||
	CRCW0402100KFKED|Resistor||Device:R|Resistance||||100||0||
	LD39100PU18RY||||||||12||0||
	B3U-1000P||||||||10||0||
	TSW-102-08-F-S||||||||40||0||
	PESD5Z3.3,115||||||||100||0||


4. configure kicad 8 to use the library db

https://www.youtube.com/watch?v=nZqoay-Yevk