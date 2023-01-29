import os
import pathlib
import csv


PATH = pathlib.Path(__file__).parent.absolute()

id_data_map = {}
# First of all we need to load both of these csv files and merge them by ID
main_csv_path = os.path.join(PATH, 'aqsoldb_full.csv')
with open(main_csv_path) as file:
    dict_reader = csv.DictReader(file.readlines())
    for data in dict_reader:
        element_id = data['ID']
        data['split'] = 1
        id_data_map[element_id] = data

test_csv_path = os.path.join(PATH, 'dataset-E.csv')
with open(test_csv_path) as file:
    dict_reader = csv.DictReader(file.readlines())
    for data in dict_reader:
        element_id = data['ID']
        data['split'] = 0
        id_data_map[element_id] = data

# Write it all into a single csv file
fieldnames = ['index', 'ID', 'SMILES', 'InChIKey', 'Solubility', 'split']
result_csv_path = os.path.join(PATH, 'aqsoldb.csv')
with open(result_csv_path, mode='w') as file:
    dict_write = csv.DictWriter(file, fieldnames=fieldnames)
    dict_write.writeheader()
    id_data_map = dict(sorted(id_data_map.items(), key=lambda t: t[0]))
    for index, data in enumerate(id_data_map.values()):
        _data = {name: data[name] for name in fieldnames if name in data}
        _data['index'] = index
        dict_write.writerow(_data)
