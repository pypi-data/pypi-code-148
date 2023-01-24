#******************************************************************************************************************************************
#*******************                                                                                                    *******************
#*******************                  Créer le 05-12-2022 at 12h56 by Rakotonindriana Johns David                       *******************
#*******************                                                                                                    *******************
#******************************************************************************************************************************************
from django.db import models

from django.shortcuts import render, HttpResponse
from django.db import connections
import pandas as pd
from django.utils.crypto import get_random_string

def getDateMaj(table,colonne="date_creation"):
        sql ="""SELECT 
                to_char(max({}), 'DD/MM/YYYY à HH24:MI:ss') as {}
            FROM {}
        """.format(colonne,colonne,table);
        prod= connections['fnac'].cursor()
        prod.execute(sql)
        result = prod.fetchall()
        prod.close() 
        res = ''
        # print(result[0][0])
        if len(result) !=0 :
            res = result[0][0]
        return res
################################################################################################
######  Insertion des données sur la table tableName dans la base de donnée connection #########
################################################################################################
def InsertCommande(data,tableName,connection):
    name = []
    value = []
    retour = ''
    if len(data)>0:
        sql =" INSERT INTO "+tableName+" ( "
        for key in data:
            if data[key]:
                name.append(key)
                value.append("'"+("''".join(str(data[key]).split("'")))+"'")
        value = ','.join(value)
        name = ','.join(name)
        
        sql +=name+") VALUES ("+value+");"
        # print(sql)
        if excecuteSQLCommand(sql,connection):
            retour = True#'success'
        else:
            retour = False#'error'
    else:
        retour = False#'Aucun'
    return retour
################################################################################################
#####  Mise à jour des données sur la table tableName dans la base de donnée connection ########
################################################################################################
def UpdateCommande(data,tableName,base,where=' '):
    if len(data)>0:
        sql =" UPDATE "+tableName+" SET  "
        i = 0
        for key in data:
            if( str(data[key]) =='NULL'):
                if i==0:
                    sql += " {} = {} ".format(key,(str(data[key]).replace("'" , "''", 100)))
                else:
                    sql += " , {} = {} ".format(key,(str(data[key]).replace("'" , "''", 100)))
            else : 
                if i==0:
                    sql += " {} = '{}' ".format(key,(str(data[key]).replace("'" , "''", 100)))
                else:
                    sql += " , {} = '{}' ".format(key,(str(data[key]).replace("'" , "''", 100)))
            i+=1
        sql += " WHERE "+where
        # print(sql)
        if excecuteSQLCommand(sql,base):
            retour = True
        else:
            retour = False
    else:
        retour = False
    return retour  
################################################################################################
######                      Executer SQL sur la base de donnée connection              #########
################################################################################################
def excecuteSQLCommand(sql,connection):
    try:
        cursor1= connections[connection].cursor()
        cursor1.execute(sql)
        cursor1.close()
        return True
    except:
        return False
################################################################################################
######                                     Supprimer                                   #########
################################################################################################   
def delete(tableName,where,base):
    sql ="""DELETE FROM {} WHERE {};
    """.format(tableName,where)
    if excecuteSQLCommand(sql,base):
        retour = True
    else:
        retour = False
    return retour
################################################################################################
######                                     Remove none                                 #########
################################################################################################ 
def RemoveNone(data,none,value='NULL'):
    for i in data : 
        if(str(data[i])==none):
            data.update({i:value})
    return data
################################################################################################
######                                     SELECT                                      #########
################################################################################################ 
def Select(sql,base='default'):
    prod = connections[base].cursor()
    prod.execute(sql)
    result = prod.fetchall()
    field_names = [i[0] for i in prod.description]
    prod.close()
    if len(result) != 0 :
        df = pd.DataFrame(result, columns=field_names)
    else :
        df = pd.DataFrame(columns=field_names)
    return df