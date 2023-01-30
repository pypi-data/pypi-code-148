#-*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd
import os
import csv


def stackTodb(dataFrame, dbTableName):
    print(dataFrame)
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/stackline'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    dataFrame.to_sql(name=dbTableName, con=db_connection, if_exists='append', index=False)
    print("finished")


def csv_cleaning(csvFile, csv_folder_cleaned):
    file=open(csvFile,'r', encoding='latin1')
    targetFile = csv_folder_cleaned + "\\CLEANED_" + os.path.basename(csvFile)
    target=open(targetFile,'w', encoding='latin1')
    
    for line in file:
        target.write(line[:-1].rstrip(',') + "\n")

    file.close()
    target.close()

def csvCleaner(csv_folder, csv_folder_cleaned):
    fileList = os.listdir(csv_folder)

    for i in range(len(fileList)):
        csv_cleaning(csv_folder + "\\" + fileList[i], csv_folder_cleaned)

def commonPreprocess(dataframe):
    # brand명 기준으로 이후 6글자 추출
    dataframe['brand'] = dataframe['brand'].str.lower()
    dataframe['title'] = dataframe['title'].str.lower()
    dataframe['product_name_1'] = dataframe.apply(lambda x: x['brand'] + ' ' + ' '.join(x['title'].split(x['brand'])[1].split()[:5]) if x['brand'] in x['title'] else '', axis=1)

    return dataframe

def csvImporter(csv_folder, csv_folder_cleaned, db_table_name):
    column_name = ["retailer_id", "retailer_name", "retailer_sku", "upc", "model_number", "title", "brand", "category", "subcategory", "week_id", "week_ending", "units_sold", "retail_sales", "retail_price", "conversion_rate", "total_traffic", "organic_traffic"]
    csvCleaner(csv_folder, csv_folder_cleaned)

    fileList = os.listdir(csv_folder_cleaned)
    for i in range(len(fileList)):

        dataframe = pd.read_csv(csv_folder_cleaned + "\\" + fileList[i], sep=',', engine='c', encoding='latin1')
        dataframe.columns = column_name
        dataframe.insert(0, "file_name", fileList[i][:-4], True)

        commonPreprocess(dataframe)
        stackTodb(dataframe, db_table_name)

# if __name__ == "__main__":
#     db_table_name = 'tb_stackline_dataset'
#     csv_folder = "csvFolder"
#     csv_folder_cleaned = "csvFolder_cleaned"
     
#     csvImporter(csv_folder, csv_folder_cleaned, db_table_name)