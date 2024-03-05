Purpose of this tool/scripts is to help managing the list of own pcb components.

When components are ordered from warehouses like digikey or mouser, customer can download the list of ordered components
as a CSV or excel file. This tool will parse those CSV files and import the data to sqlite database.

This is very initial proof of concept version that can parse digikey and mouser csv files and create
kicad database library. Project contains sample CSV files that can be used for testing the database cceation.

Kicad 8 can be configured to use the components listed in the created sqlite database file.

Usage:

1. csv file import to new sqlite database:
   
>    ./db_content_import_test.sh


2. open database
>sqlite3 test_sqlite3.db 	

3. view component list from database

>	sqlite> select * from components;
	
	1|HPH2-B-10-UA||||CONN HEADER VERT 10POS 1.27MM||||10||0|
	2|HPH2-B-08-UA||||CONN HEADER VERT 8POS 1.27MM||||20||0|
	3|LTST-C171GKT|LED|Color|green|LED GREEN CLEAR CHIP SMD||Device:LED||100||0|
	4|MLZ2012M220WTD25|Inductor|${Inductance}||FIXED IND 22UH 220MA 2 OHM SMD||Device:L||50||0|
	5|GRM188R60J476ME15D|Capacitor|${Capacitance}|47UF|CAP CER 47UF 6.3V X5R 0603||Device:C|Capacitor_SMD:C_0603_1608Metric|10||0|
	6|CF14JT1M80|Resistor|${Resistance}|1.8M|RES 1.8M OHM 5% 1/4W AXIAL||Device:R||25||0|
	7|LD39100PU33R||||IC REG LINEAR 3.3V 1A 6DFN||||5||0|	
	8|||||||||0||0|
	9|0402YC102K4T4A|Capacitor|${Capacitance}||Multilayer Ceramic Capacitors MLCC - SMD/SMT Multilayer Ceramic Capacitors MLCC - SMD/SMT NEW GLOBAL PN KAM05AR71C102KN 16V 1000pF X7R 0402 10% AEC-Q200||Device:C|Capacitor_SMD:C_0402_1005Metric|100||0|
	10|CRCW04021K50JNED|Resistor|${Resistance}||Thick Film Resistors - SMD Thick Film Resistors - SMD 1/16watt 1.5Kohms 5%||Device:R||100||0|
	11|CRCW0402100KFKED|Resistor|${Resistance}||Thick Film Resistors - SMD Thick Film Resistors - SMD 1/16watt 100Kohms 1%||Device:R||100||0|
	12|LD39100PU18RY||||LDO Voltage Regulators LDO Voltage Regulators 1 A low quiescent current low noise volt regulator||||12||0|
	13|B3U-1000P||||Tactile Switches Tactile Switches Top Actuated w/o boss w/o ground||||10||0|
	14|TSW-102-08-F-S||||Headers & Wire Housings Headers & Wire Housings Classic PCB Header Strips, 0.100" pitch||||40||0|
	15|PESD5Z3.3,115|Diode|Voltage||ESD Suppressors / TVS Diodes ESD Suppressors / TVS Diodes PESD5Z3.3/SOD523/SC-79||Device:D||100||0|

4. configure kicad 8 to use the library db

https://www.youtube.com/watch?v=nZqoay-Yevk
