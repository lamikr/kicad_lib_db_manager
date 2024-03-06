rm -f pilppa_kicad_lib_db.sqlite
python ./pilppa_kicad_lib_db_manager.py -f component_orders/digikey/digikey_2024_03_01.csv
python ./pilppa_kicad_lib_db_manager.py -f component_orders/mouser/mouser_2024_01_31.csv
sqlite3 pilppa_kicad_lib_db.sqlite "select * from components;"
