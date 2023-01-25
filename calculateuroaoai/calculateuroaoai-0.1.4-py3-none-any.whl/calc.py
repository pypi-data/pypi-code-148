import pandas as pd

def addition_from_our_calc(num1, num2):
    return num1 + num2

def multiplication_from_our_calc(num1, num2):
    return num1 * num2

def other_package():
    data_frame = pd.read_excel('data_excel.xlsx', dtype='object')
    json_contact_list = {}
    for index, row in data_frame.iterrows():
        json_contact_list[row['Nom du site']] = {
            "Nom": row['Nom'],
            "Prénom": row['Prénom'],
            "Mail": row['Mail'],
            "Téléphone": row['Téléphone']
        }
    return json_contact_list