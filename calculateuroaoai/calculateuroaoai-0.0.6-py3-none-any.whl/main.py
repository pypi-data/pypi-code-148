import pandas as pd


def test_other_package():
    data_frame = pd.read_excel('data/data_excel.xlsx', dtype='object')
    json_contact_list = {}
    for index, row in data_frame.iterrows():
        json_contact_list[row['Nom du site']] = {
            "Nom": row['Nom'],
            "Prénom": row['Prénom'],
            "Mail": row['Mail'],
            "Téléphone": row['Téléphone']
        }
    return json_contact_list