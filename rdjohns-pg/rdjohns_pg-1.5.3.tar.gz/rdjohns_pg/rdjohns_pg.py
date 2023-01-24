import json
import psycopg2
from .Write_log import writeLogTxt, getNameFileOutput

def jsonToTuple(data):
    """Conver list json to tuple

    Args:
        data (json): _description_

    Returns:
        list: list of tuple
    """
    res = []
    for elem in data:
        d = []
        for item in elem:
            d +=[elem[item]]
            
        res += [tuple(d)]
    return res

def excecuteElement(config,records,ps_delete_query):
    """_summary_

    Args:
        config (json): config database
        records (list): list of tuple 
        ps_delete_query (str): query

    Returns:
        int: 0 or >0 it works and -1 have an error
    example:
        * DELETE ELEMENT IN THE TABLE FROM THE DATABASE
            records = [(1,),(2,)]
            ps_delete_query = "Delete from mobile where id = %s"
        * UPDATE ELEMENT IN THE TABLE FROM THE DATABASE
            records = [(750, 4), (950, 5)]
            sql_update_query = "Update mobile set price = %s where id = %s"
        * INSERT ELEMENT IN THE TABLE FROM THE DATABASE
            records = [(4, 'LG', 800), (5, 'One Plus 6', 950)]
            sql_insert_query = "INSERT INTO mobile (id, model, price)  VALUES (%s,%s,%s)"
    """
    res = 0
    try:
        connection = psycopg2.connect(host=config['host'],port=config['port'],database=config['database'],user=config['user'],password=config['password'])
        cursor = connection.cursor()
        cursor.executemany(ps_delete_query, records)
        connection.commit()
        res = cursor.rowcount
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL :", error)
        res = -1
        writeLogTxt(name=getNameFileOutput()+'_Log.txt',data="Error excecuteElement : " + str(error)+'\n'+('**'*45)+'\n\n',root_directory_name="",dir_name = '_LOG_Postgres')
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return res

def selectElement(config,where,sql_select_query,one=False):
    """_summary_

    Args:
        config (json): config database
        where (tuple): like (5,)
        sql_select_query (str): like "select * from mobile where id = %s"
        one (bool, optional): select one or multiple. Defaults to False.

    Returns:
        list :  list tuple
    """
    
    record = None
    try:
        connection = psycopg2.connect(host=config['host'],port=config['port'],database=config['database'],user=config['user'],password=config['password'])
        cursor = connection.cursor()
        cursor.execute(sql_select_query, where)
        if one:
            record = cursor.fetchone()
        else:
            record = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)
        writeLogTxt(name=getNameFileOutput()+'_Log.txt',data="Error selectElement : "+ str(error)+('**'*45)+'\n\n' ,root_directory_name="",dir_name = '_LOG_Postgres')

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return record

def excecuteSQL(config,sql_query):
    """ excecuteSQL brute for Create Table, Shama ... but not crud

    Args:
        config (json): config database
        sql_query (str): sql query

    Returns:
        Boolean: resul of query (True or False)
    """
    res = False
    try:
        connection = psycopg2.connect(host=config['host'],port=config['port'],database=config['database'],user=config['user'],password=config['password'])
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        res = True
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL :", error)
        writeLogTxt(name=getNameFileOutput()+'_Log.txt',data="Error excecuteSQL : "+str(error)+('**'*45)+'\n\n',root_directory_name="",dir_name = '_LOG_Postgres')
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return res