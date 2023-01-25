import configs
import pandas as pd

def config_file():
    print(f"Hello {configs.config.my_name} !!")

def other_package():
    data_frame = pd.read_excel(configs.config.my_file, dtype='object')
    json_contact_list = {}
    for index, row in data_frame.iterrows():
        json_contact_list[row['Nom du site']] = {
            "Nom": row['Nom'],
            "Prénom": row['Prénom'],
            "Mail": row['Mail'],
            "Téléphone": row['Téléphone']
        }
    return json_contact_list
