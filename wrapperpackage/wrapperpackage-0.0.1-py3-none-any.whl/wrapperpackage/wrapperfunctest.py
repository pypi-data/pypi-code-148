#######################################################################################
# Notebook_Name -  Validations_abc.py
# Purpose - To run the Validation checks on a particular object before and after of it processed and creating the validation checks result and storing it into Azure SQL Tables. 
# Version - 1.0
# History - 
#######################################################################################

# ----------------------------------------------------------------------------------- #
# ----------------------------- Importing Packages ---------------------------------- #
# ----------------------------------------------------------------------------------- #

from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils
from datetime import datetime, timedelta
from pyspark.sql.functions import *
import pyodbc as pyodbc
import pandas as pd
import asyncio

import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils




# ------------------------------------------------------------------------------------ #
# ----------------------------- Building Spark Session ------------------------------- #
# ------------------------------------------------------------------------------------ #

try:
    spark = SparkSession.builder.getOrCreate()
    dbutils = DBUtils(spark)
except Exception as ex:
    Error_Message = "Error Occured While Creating the Spark Session - "+ str(ex)
    print(Error_Message)
    

# ----------------------------------------------------------------------------------- #
# -------------------------- Fetching Notebook level details ------------------------ #
# ----------------------------------------------------------------------------------- #

try:
    NOTEBOOK_PATH = (
        dbutils.notebook.entry_point.getDbutils()
        .notebook()
        .getContext()
        .notebookPath()
        .get()
    )

    userinfo = NOTEBOOK_PATH.split('/')
    Username = userinfo[2]
    logs_info = []
    current_time = datetime.now()
except Exception as ex:
    print("Error Occured While Initiating notebook details - " + str(ex))

# ----------------------------------------------------------------------------------- #
# ---------------------- Declared Global Variable and connection -------------------- #
# ----------------------------------------------------------------------------------- #

try:
    Query_df = spark.sql(""" Select Query from ValidationRuleSQLQuery """)
    Querydata_1 = Query_df .collect()[0][0]
    Querydata_2 = Query_df .collect()[1][0]
    Querydata_3 = Query_df .collect()[2][0]
    Querydata_4 = Query_df .collect()[3][0]
    Query1 = "Select * From abc.Job_Rule_Assignment Where Job_Id = "
    Query2 = " and ValidationType = 'Pre'"
    Query3 = " and ValidationType = 'Post'"
    TableName = "abc.Job_Rule_Execution_Log"
except Exception as ex:
    print("Error Occured declaring Global Variables - " + str(ex))

# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - wrapperFunction
# Purpose - To trigger all validation rules before object processed, fetching all the rule ids assigned for a particular jobid and based on the rule id triggering those validation rules for a particular object and returning the output of the validation rule which we are storing in Azure sql table.
# Arguments - No. of arguments expected 9 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( BalanceAmountColumn )  - Name of a column from table or file for which we will calculate balance amount.
# Arg5( ObjectType )  - Describe type of a object either it is sql table or nas file or adls file.
# Arg6( ObjectPath_PostProcessing )  - ADLS file path of object after we processed and saved in adls.
# Arg7( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg8( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg9( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - wrapperFunction(JobId, ObjectPath, ObjectName, BalanceAmountColumn, ObjectType, 
# ObjectPath_PostProcessing,server_name,database_name,FileType)
# One Function calling statement with Example value - wrapperFunction(461636582315684,
# 'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','SALARY','File',
# 'abfss://sourcecontainer@adlstoadls.dfs.core.windows.net/BlueskyProduct','testsql-ss','testsqldb-ss','csv')
# ------------------------------------------------------------------------------------------------------------------------------------- #



def wrapperFunction(JobId, ObjectPath, ObjectName, BalanceAmountColumn, ObjectType, ObjectPath_PostProcessing, server_name, 
                    database_name, FileType, storage_account_name, storage_account_key, scope, sqlusername, sqlpassword,log_path):
    
    def store_logs_in_adls(string_log_info):
            z = file_client.append_data(string_log_info,0, len(string_log_info))
            w = file_client.flush_data(len(string_log_info))  
            return True
    
    # Accessing Storage Account and Store Log in ADLS.
    try:
        current_time = datetime.now()
        account_url=f"https://{storage_account_name}.dfs.core.windows.net"
        account_key = dbutils.secrets.get(scope,storage_account_key)
        log_path_info = log_path
        separated_by_forward_slash = log_path_info.split("/")
        length = len(separated_by_forward_slash)
        container_extract = separated_by_forward_slash[2]
        container = container_extract.split("@")
        container_name = container[0]
        #container_name = "rawlayer"
        path_index = length -1
        path = separated_by_forward_slash[3:path_index]
        adls_log_directory = "/".join(path)
        log_file_name = separated_by_forward_slash[-1]
        
        # Created Variables for logFile
        log = f"{current_time} Created Variables to connect storage account and store log in ADLS"
        logs_info.append(log)
        
        # Creating serviceClient from dataLakeServiceClient
        service_client = DataLakeServiceClient(account_url, credential=account_key)
        log = f"{current_time} Creating service_client from DataLakeServiceClient"
        logs_info.append(log)
        
        #Creating fileSystemClient to access ADLS container
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        
        log = f"{current_time} Creating fileystem_client to access ADLS container"
        logs_info.append(log)
        
        # Creating dir_client to access ADLS container directory
        dir_client = file_system_client.get_directory_client(adls_log_directory)
        log = f"{current_time} Creating dir_client to access ADLS container to create directory"
        logs_info.append(log)
        
        # Creating fileClient to access directory in ADLS and create log file
        file_client = dir_client.create_file(log_file_name)
        
        log = f"{current_time} Creating fileClient to access ADLS container to create log file"
        logs_info.append(log)
        
        log = f"{current_time} Created connection with storageAccount to storage log file in ADLS"
        logs_info.append(log)
        
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
       
    try:
        current_time = datetime.now()
        ###  Configuring storage account 
        storage_account_url = f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net"
        spark.conf.set(storage_account_url,dbutils.secrets.get(scope,storage_account_key))
        current_time = datetime.now()
        log = f"{current_time} Create connection with Storage Account"
        logs_info.append(log)
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
    try:
        #### Creating SQL Query to fetch rule assigned to a particular Job ID ####
        Querydata = Query1 + str(JobId) + Query2
        current_time = datetime.now()
        log = f"{current_time} wrapperFunction Querydata variable is initialized"
        logs_info.append(log)

        #### Fetching the rule assigned to a particular Job ID for pre object processing ####
        JobRuleDetails_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata)
        log = f"{current_time} JobRuleDetails_df Dataframe is created"
        logs_info.append(log)

        #### Converting Spark Dataframe to Pandas dataframe ####
        JobRuleDetails_pdf = JobRuleDetails_df.toPandas()
        log = f"{current_time} JobRuleDetails_pdf Pandas Dataframe is created"
        logs_info.append(log)
        Output = str('')
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

    # Checking ObjectName or Object Path is Blank and ObjectType Not in SQL Table  
    if (( None == ObjectName or ObjectName == "") or ((None == ObjectPath or ObjectPath == "") and (ObjectType != 
                                                                                                    "SQLTable"))) : 
        error_message = "Error Occured : ObjectName or Path is blank"

        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)

        # Converting List of Log Message into String 
        string_log_info = "\n".join(logs_info)

        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)

        return "Error Message : ObjectName or Path is blank in Pre Validation Wrapper Function"

    #### Iterating RuleId to trigger a particular rule assigned with the rule id ####
    try:
        for ind in JobRuleDetails_pdf.index:
            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 1):
                #### Triggering Count Validation pre Object processing rule ####
                Out1 = CheckJobRule_CountValidation(JobId, ObjectPath, ObjectName, ObjectType,server_name,database_name,FileType, sqlusername, sqlpassword)

                # Checking if CountValidation return Error comment Error while reading file 
                if (Out1 == 'Error while reading file'):
                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out1} in CountValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in CountValidation'

                # Checking if CountValidation return Error comment Error Occured  
                if(Out1 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in CountValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in CountValidation'

                Output = Output + Out1 + " | " 

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 2):
                #### Triggering Balance Amount Validation pre Object processing rule ####

                Out2 = CheckJobRule_BalanceAmountValidation(JobId, ObjectPath, ObjectName, BalanceAmountColumn, 
                                                            ObjectType,server_name,database_name,FileType, sqlusername, sqlpassword)

                # Checking if BalanceAmountValidation return Error comment Error while reading file 
                if (Out2 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out2} in BalanceAmountValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in BalanceAmountValidation'

                # Checking if BalanceAmountValidation return Error comment Error Occured  
                if(Out2 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in BalanceAmountValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in BalanceAmountValidation'

                Output = Output + Out2 + " | "


            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 3):
                #### Triggering Threshold Validation pre Object processing rule ####

                Out3 = CheckJobRule_ThresholdValidation(JobId, ObjectPath, ObjectName, ObjectType, server_name,database_name,FileType, sqlusername, sqlpassword)

                # Checking if ThresholdValidation return Error comment Error while reading file 
                if (Out3 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out3} in ThresholdValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in ThresholdValidation'

                # Checking if ThresholdValidation return Error comment Error Occured
                if(Out3 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in ThresholdValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in ThresholdValidation'

                Output = Output + Out3 + " | "

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 4):
                #### Triggering Object Name Validation pre Object processing rule ####

                Out4 = CheckJobRule_FileNameValidation(JobId, ObjectPath, ObjectName, server_name, database_name, ObjectType, sqlusername, sqlpassword)

                # Checking if FileNameValidation return Error comment Error while reading file
                if (Out4 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out4} in FileNameValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String 
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in FileNameValidation'

                # Checking if FileNameValidation return Error comment Error Occured
                if(Out4 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in FileNameValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in FileNameValidation'

                Output = Output + Out4 + " | "

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 5):
                #### Triggering Object Size Validation pre Object processing rule ####

                Out5 = CheckJobRule_FileSizeValidation(JobId, ObjectPath, ObjectName, server_name,database_name, ObjectType, sqlusername, sqlpassword)

                # Checking if FileSizeValidation return Error comment Error while reading file
                if (Out5 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out5} in FileSizeValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in FileSizeValidation'

                 # Checking if FileSizeValidation return Error comment Error Occured
                if(Out5 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in FileSizeValidation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in FileSizeValidation'

                Output = Output + Out5 + " | "

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 6):
                #### Triggering Object Arrival Time Validation pre Object processing rule ####

                Out6 = CheckJobRule_FileArrival_Validation(JobId, ObjectPath, ObjectName, server_name,database_name,ObjectType, sqlusername, sqlpassword)
                # Checking if FileArrival_Validation return Error comment Error while reading file
                if (Out6 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out6} in FileArrival_Validation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in FileArrival_Validation'

                # Checking if FileArrival_Validation return Error comment Error Occured
                if(Out6 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in FileArrival_Validation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in FileArrival_Validation'

                Output = Output + Out6 + " | "

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 7):
                #### Triggering Missing Object Validation pre Object processing rule ####

                Out7 = CheckJobRule_Missing_FileCheck_Validation(JobId,ObjectPath,ObjectName,server_name,database_name, 
                                                                 ObjectType, sqlusername, sqlpassword)

                # Checking if Missing_FileCheck_Validation return Error comment Error while reading file
                if (Out7 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out7} in Missing_FileCheck_Validation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in Missing_FileCheck_Validation'

                # Checking if Missing_FileCheck_Validation return Error comment Error Occured
                if(Out7 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in Missing_FileCheck_Validation"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in Missing_FileCheck_Validation'

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 10):
                #### Triggering Missing Object Validation pre Object processing rule ####

                Out10 = CheckJobRule_CountValidation_Egress(JobId, ObjectPath, ObjectName, server_name, database_name, FileType, sqlusername, 
                                                            sqlpassword)
                # Checking if CheckJobRule_CountValidation_Egress return Error comment Error while reading file
                if (Out10 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out10} in Count Validation in Egress Pattern"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in Count Validation in Egress Pattern'

                # Checking if CheckJobRule_CountValidation_Egress return Error comment Error Occured
                if(Out10 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in Count Validation in Egress Pattern"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in Count Validation in Egress Pattern'   

                Output = Output + Out10 + " | "

        current_time = datetime.now()    
        log = f"{current_time} {Output}"
        logs_info.append(log)

        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)

        # storing log messages in adls location
        store_logs_in_adls(string_log_info)

        return Output
    except Exception as ex:
        error_message = error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message


# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - wrapperFunction_postFile
# Purpose - To trigger all validation rules after object processed, fetching all the rule ids assigned for a particular jobid and based on the rule id triggering those validation rules for a particular object and returning the output of the validation rule which we are storing in Azure sql table.
# Arguments - No. of arguments expected 9 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( BalanceAmountColumn )  - Name of a column from table or file for which we will calculate balance amount.
# Arg5( ObjectType )  - Describe type of a object either it is sql table or nas file or adls file.
# Arg6( ObjectPath_PostProcessing )  - ADLS file path of object after we processed and saved in adls.
# Arg7( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg8( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg9( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - wrapperFunction_postFile(JobId, ObjectPath, ObjectName, BalanceAmountColumn, ObjectType, 
# ObjectPath_PostProcessing,server_name,database_name,FileType)
# One Function calling statement with Example value - wrapperFunction_postFile(461636582315684,
# 'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','SALARY','File',
# 'abfss://sourcecontainer@adlstoadls.dfs.core.windows.net/BlueskyProduct','testsql-ss','testsqldb-ss','csv')
# -------------------------------------------------------------------------------------------------------------------------------------- #

def wrapperFunction_postFile(JobId, ObjectPath, ObjectName, BalanceAmountColumn, ObjectType, ObjectPath_PostProcessing, 
                             server_name, database_name, FileType, storage_account_name, storage_account_key, scope, sqlusername, 
                             sqlpassword,log_path):
    
    def store_logs_in_adls(string_log_info):
            z = file_client.append_data(string_log_info,0, len(string_log_info))
            w = file_client.flush_data(len(string_log_info))  
            return True
    
    # Accessing Storage Account and Store Log in ADLS.
    try:
        logs_info = []
        current_time = datetime.now()
        current_time = datetime.now()
        account_url=f"https://{storage_account_name}.dfs.core.windows.net"
        account_key = dbutils.secrets.get(scope,storage_account_key)
        log_path_info = log_path
        separated_by_forward_slash = log_path_info.split("/")
        length = len(separated_by_forward_slash)
        container_extract = separated_by_forward_slash[2]
        container = container_extract.split("@")
        container_name = container[0]
        path_index = length -1
        path = separated_by_forward_slash[3:path_index]
        adls_log_directory = "/".join(path)
        log_file_name = separated_by_forward_slash[-1]
        
        # Created Variables for logFile
        log = f"{current_time} Created Variables to connect storage account and store log in ADLS"
        logs_info.append(log)
        
        # Creating serviceClient from dataLakeServiceClient
        service_client = DataLakeServiceClient(account_url, credential=account_key)
        log = f"{current_time} Creating service_client from DataLakeServiceClient"
        logs_info.append(log)
        
        #Creating fileSystemClient to access ADLS container
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        
        log = f"{current_time} Creating fileystem_client to access ADLS container"
        logs_info.append(log)
        
        # Creating dir_client to access ADLS container directory
        dir_client = file_system_client.get_directory_client(adls_log_directory)
        log = f"{current_time} Creating dir_client to access ADLS container to create directory"
        logs_info.append(log)
        
        # Creating fileClient to access directory in ADLS and create log file
        file_client = dir_client.create_file(log_file_name)
        
        log = f"{current_time} Creating fileClient to access ADLS container to create log file"
        logs_info.append(log)
        
        log = f"{current_time} Created connection with storageAccount to storage log file in ADLS"
        logs_info.append(log)
        
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
    
    try:
        current_time = datetime.now()
        #### Creating SQL Query to fetch rule assigned to a particular Job ID ####
        #Querydata = 'Select * From abc.Job_Rule_Assignment Where Job_Id = ' + str(JobId) + " and ValidationType = 'Post'"
        Querydata = Query1 + str(JobId) + Query3

        log = f"{current_time} wrapperFunction_postFile Querydata variable is initialized"
        logs_info.append(log)

        #### Fetching the rule assigned to a particular Job ID for post Object Processing ####

        JobRuleDetails_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata)

        log = f"{current_time} JobRuleDetails_df Dataframe is created in post file processing"
        logs_info.append(log)

        #### Converting Spark Dataframe to Pandas dataframe ####

        JobRuleDetails_pdf = JobRuleDetails_df.toPandas()
        Output = str('')

        log = f"{current_time} JobRuleDetails_pdf Pandas Dataframe is created in post file processing"
        logs_info.append(log)
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
    # Checking ObjectName or Object Path is Blank and ObjectType Not in SQL Table 
    if (( None == ObjectName or ObjectName == "") or ((None == ObjectPath_PostProcessing or ObjectPath_PostProcessing == "") and (ObjectType != "SQLTable"))) : 
        error_message = "ObjectName or Path is blank"
        
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        
        # Storing log messages in adls location
        store_logs_in_adls(string_log_info)
        
        return "\n Error Message : ObjectName or Path is blank in Post Wrapper Function"
    
    #### Iterating RuleId to trigger a particular rule assigned with the rule id ####
    try:
        for ind in JobRuleDetails_pdf.index:
            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 8):

                #### Triggering count Validation rule post Object processing ####
                Out8 = CheckJobRule_CountValidation_PostFileProcessing(JobId, ObjectPath_PostProcessing, 
                                                                       ObjectName,server_name,database_name,FileType, sqlusername, 
                                                                       sqlpassword)

                # Checking if CountValidation_PostFileProcessing return Error comment Error while reading file
                if (Out8 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out8} in CountValidation_PostFileProcessing"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # Storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in CountValidation_PostFileProcessing'

                # Checking if CountValidation_PostFileProcessing return Error comment Error Occured
                if(Out8 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in CountValidation_PostFileProcessing"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # Storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in CountValidation_PostFileProcessing'

                current_time = datetime.now()
                log = f"{current_time} {Out8}"
                logs_info.append(log)
                Output = Output + Out8 + " | "

            if ((JobRuleDetails_pdf['Rule_Id'][ind]) == 9):

                #### Triggering Balance Amount Validation rule post Object processing ####
                Out9 = CheckJobRule_BalanceAmountValidation_PostFileProcessing(JobId, ObjectPath_PostProcessing, ObjectName,
                                                                               BalanceAmountColumn, server_name, database_name, 
                                                                               FileType, sqlusername, sqlpassword)
                # Checking if BalanceAmountValidation_PostFileProcessing return Error comment Error while reading file
                if (Out9 == 'Error while reading file'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured : {Out9} in BalanceAmountValidation_PostFileProcessing"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # Storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error while reading file in BalanceAmountValidation_PostFileProcessing'

                # Checking if BalanceAmountValidation_PostFileProcessing return Error comment Error Occured
                if(Out9 == 'Error Occured'):

                    current_time = datetime.now()
                    log = f"{current_time} Error Occured in BalanceAmountValidation_PostFileProcessing"
                    logs_info.append(log)

                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)

                    # Storing log messages in adls location
                    store_logs_in_adls(string_log_info)

                    return 'Error Occured in BalanceAmountValidation_PostFileProcessing'

                current_time = datetime.now()
                log = f"{current_time} {Out9}"
                logs_info.append(log)
                Output = Output + Out9 + " "

        current_time = datetime.now()    
        log = f"{current_time} {Output}"
        logs_info.append(log)

        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)

        # Storing log messages in adls location
        store_logs_in_adls(string_log_info)

        return Output
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# ------------------------------------------------------------------------------------------------------------------------------------ #
# FunctionName - CheckJobRule_CountValidation
# Purpose - Fetching the record count from Audit Table by stablizing the connecting with Azure SQL server for a particular object as Source Count and then fetch the record count value for the same object from ADLS File or NAS drive Filr or SQL Table based on Object type and then then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 7 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a ADLS or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( ObjectType )  - Describe type of a object either it is sql table or nas file or ADLS file.
# Arg5( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg6( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg7( FileType )  - type of file like .csv, .json, .parquet, .xml
# One Sample function calling statement - CheckJobRule_CountValidation(JobId, ObjectPath, ObjectName, ObjectType, 
# server_name,database_name,FileType)
# One Function calling statement with Example value - 
#CheckJobRule_CountValidation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','File','abfss://sourcecontainer@adlstoadls.dfs.core.windows.net/BlueskyProduct','testsql-ss','testsqldb-ss','csv')
# ------------------------------------------------------------------------------------------------------------------------------------ #

def CheckJobRule_CountValidation(JobId, ObjectPath, ObjectName, ObjectType,server_name,database_name,FileType, sqlusername, sqlpassword):
    try:

        #### Creating RuleID Value ####
        RuleId = int(1)
        
        SourceCount = "Source Count"
        # Declaring function level variables 
        Source_Value_Type = "Source Count"
        Target_Value_Type = "Target Count"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #Querydata = "Select * from abc.Audit_Log where Product_Name not like 'Post%' "
        
        #### Fetching all the pre processed Object data from Audit Table(Source) ####
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)

        #### Fetching data from Audit Table(Source) for a particular Object ####
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)

        #### Converting Spark Dataframe to Pandas dataframe ####
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching Source Count for a particular Object ####
        SourceValue = int(AuditTableFileCount_pdf['File_Count'])

        #### Checking Object Type wheather is it ADLS File, SQL Table or NAS Drive file ####
        if (ObjectType == 'File'):
            #### Fetching data from Given Object path(Target) for a particular Object ####
            try:
                ## Reading file from filepath and name variable
                RawLogData_df = spark.read.load(path=ObjectPath, format=f"{FileType}", header = True)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if (ObjectType == 'SQLTable'):
            #### Creating SQL Query to fetch data for a particular Object ####
            Querydata = Query1[0:14] + str(ObjectName)
            try:       
                RawLogData_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if(ObjectType == 'NASFile'):
            if(FileType == 'json'):
                try:
                #### Fetching data from Given Object path(Target) for a particular Object ####
                    file = pd.read_json(ObjectPath, lines=True)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                    
                #### Creating Spark dataframe ####
                RawLogData_df = spark.createDataFrame(file)
            if(FileType == 'csv'):
                try:
                    #### Fetching data from Given Object path(Target) for a particular Object ####
                    file = pd.read_csv(ObjectPath)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                    
                #### Creating Spark dataframe ####
                RawLogData_df = spark.createDataFrame(file)
        #### Fetching Target Count for a particular Object ####
        TargetValue = int(RawLogData_df.count())


        #### Checking the condition and storing the Validation rule result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'

        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        #### Checking the Status of rule result and storing the function return value ####
        if (RuleStatus == 'Passed'):
            out = str('CountValidation passed')
        else:
            out = str('CountValidation Failed')

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)

        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
    ################################
    
# ------------------------------------------------------------------------------------------------------------------------------------ #
# FunctionName - CheckJobRule_BalanceAmountValidation
# Purpose - Fetching the Balance amount column value from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Value and then fetch the whole data for the same object from ADLS File or NAS drive Filr or SQL Table based on Object type and then storing it in spark dataframe and calculating the balance amount for particular column as target value then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 8 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( BalanceAmountColumn )  - Name of a column from table or file for which we will calculate balance amount.
# Arg5( ObjectType )  - Describe type of a object either it is sql table or nas file or adls file.
# Arg6( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg7( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg8( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - CheckJobRule_BalanceAmountValidation(JobId, ObjectPath, ObjectName, BalanceAmountColumn, #ObjectType,server_name,database_name,FileType)
# One Function calling statement with Example value -
#wrapperFunction(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','SALARY','File',#'testsql-ss','testsqldb-ss','csv')
# ----------------------------------------------------------------------------------------------------------------------------------- #

def CheckJobRule_BalanceAmountValidation(JobId, ObjectPath, ObjectName, BalanceAmountColumn, 
                                         ObjectType,server_name,database_name,FileType,  sqlusername, sqlpassword):
    try:

        #### Creating RuleID Value ####
        RuleId = int(2)
        
        # Declaring function level variables
        Source_Value_Type = "Source Balance Amount"
        Target_Value_Type = "Target Balance Amount"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"
            
        #Querydata = "Select * from abc.Audit_Log where Product_Name not like 'Post%' "

        #### Fetching all the pre processed Object data from Audit Table(Source) ####
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)

        #### Fetching data from Audit Table(Source) for a particular Object ####
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)

        #### Converting Spark Dataframe to Pandas dataframe ####
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching Source Balance Amount for a particular Object ####
        SourceValue = int(AuditTableFileCount_pdf['File_Balance_Amount'])
        
        #Querydata = "Select FileName,BalanceAmountColumn from metaabc.File_MetaData"
        
        FileMetaData_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_2)

        FileMetaDataFilter_df = FileMetaData_df.filter(FileMetaData_df.FileName == ObjectName)
        BalanceAmountColumn1 = FileMetaDataFilter_df.collect()[0][1]

        #### Checking Object Type wheather is it ADLS File, SQL Table or NAS Drive file ####
        if (ObjectType == 'File'):
            #TargetData_df = spark.read.csv(path=ObjectPath + ObjectName, header=True)
            try:
            #### Fetching data from Given Object path(Target) for a particular Object ####
                TargetData_df = spark.read.load(path=ObjectPath, format=f"{FileType}", header = True) 
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if (ObjectType == 'SQLTable'):
            #### Creating SQL Query to fetch data for a particular Object ####
            Querydata = Query1[0:14] + str(ObjectName)
            #### Creating Connection with Azure Sql Server ####
            try:
                TargetData_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if(ObjectType == 'NASFile'):
            if(FileType == 'json'):
                #### Fetching data from Given Object path(Target) for a particular Object ####
                try:
                    file = pd.read_json(ObjectPath, lines=True)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                #### Creating Spark dataframe ####
                TargetData_df = spark.createDataFrame(file)

            if(FileType == 'csv'):
                #### Fetching data from Given Object path(Target) for a particular Object ####
                try:
                    file = pd.read_csv(ObjectPath)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                #### Creating Spark dataframe ####
                TargetData_df = spark.createDataFrame(file)
                    
        #### Fetching Target Balance Amount for a particular Object ####
        BalanceAmount = TargetData_df.agg({BalanceAmountColumn: 'sum'})
        for col in BalanceAmount.dtypes:
            TargetValue = int(BalanceAmount.first()[col[0]])

        #### Checking the condition and storing the result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'
            
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        #### Checking the Status of rule result and storing the function return value ####
        if (RuleStatus == 'Passed'):
            out = str('BalanceAmountValidation passed')
        else:
            out = str('BalanceAmountValidation Failed')

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# ------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_ThresholdValidation
# Purpose - Fetching the record count value from Audit Table by stablizing the connecting with Azure SQL server for a particular object as Source Value and then fetch the minimum and maximum Threshold record count value for the same object from Filemetadata azure sql table as target range value and then then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 7 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( ObjectType )  - Describe type of a object either it is sql table or nas file or adls file.
# Arg5( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg6( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg7( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - CheckJobRule_ThresholdValidation(JobId, ObjectPath, ObjectName, ObjectType, 
# server_name,database_name,FileType)
# One Function calling statement with Example value -
#CheckJobRule_ThresholdValidation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','File','testsql-#ss','testsqldb-ss','csv')
# ------------------------------------------------------------------------------------------------------------------------------------- #


def CheckJobRule_ThresholdValidation(JobId, ObjectPath, ObjectName, ObjectType,server_name,database_name,FileType,  sqlusername, sqlpassword):
    
    try:
        #### Creating RuleID Value ####
        RuleId = int(3)
        
        # Declaring function level variables
        Source_Value_Type = "Source Threshold Value"
        Target_Value_Type = "Target Object Count"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #Querydata = "Select * from metaabc.File_MetaData"
        #### Fetching all the pre processed Object data from FileMetadata Table(Source) ####
        FileMetadata_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_3)

        #### Fetching data from Audit Table(Source) for a particular Object ####
        FileMetadata_df = FileMetadata_df.filter(FileMetadata_df.FileName == ObjectName)

        #### Converting Spark Dataframe to Pandas dataframe ####
        FileMetadata_pdf = FileMetadata_df.toPandas()

        #### Fetching Minimum and maximum threshold values ####
        SourceValue_min = FileMetadata_pdf.loc[0]['MinValue']
        SourceValue_max = FileMetadata_pdf.loc[0]['MaxValue']

        #### Creating the Source Value by using minimum and maximum value ####
        SourceValue = 'MinValue = ' + str(SourceValue_min) + ' and MaxValue = ' + str(SourceValue_max)

        #### Checking Object Type wheather is it ADLS File, SQL Table or NAS Drive file ####
        if (ObjectType == 'File'):
            try:
                #### Fetching data from Given Object path(Target) for a particular Object ####
                RawLogData_df = spark.read.load(path=ObjectPath, format=f"{FileType}", header = True)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if (ObjectType == 'SQLTable'):
            Querydata = Query1[0:14] + str(ObjectName)
            try:
                RawLogData_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        if(ObjectType == 'NASFile'):
            if(FileType == 'json'):
                try:
                    #### Fetching data from Given Object path(Target) for a particular Object ####
                    file = pd.read_json(ObjectPath, lines=True)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                RawLogData_df = spark.createDataFrame(file)

            if(FileType == 'csv'):
                try:
                    #### Fetching data from Given Object path(Target) for a particular Object ####
                    file = pd.read_csv(ObjectPath)
                except Exception as ex:
                    current_time = datetime.now()
                    error_message = "\n Error Message : " + str(ex)
                    log = f"{current_time} Error Occured {error_message}"
                    logs_info.append(log)
                    # Converting List of Log Message into String
                    string_log_info = "\n".join(logs_info)
                    # storing log messages in adls location 
                    store_logs_in_adls(string_log_info)
                    return error_message
                RawLogData_df = spark.createDataFrame(file)
        
        #### Fetching Target Value for a particular Object ####
        TargetValue = int(RawLogData_df.count())

        #### Checking the condition and storing the result ####
        if (TargetValue >= SourceValue_min and TargetValue <= SourceValue_max):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'
        
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        #### Checking the Status of rule result and storing the function return value ####
        if (RuleStatus == 'Passed'):
            out = 'ThresholdValidation passed'
        else:
            out = 'ThresholdValidation Failed'

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# ------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_FileNameValidation
# Purpose - Fetching the Object Name value from Audit Table by stablizing the connecting with Azure SQL server for a particular object as Source Value and then checking is there any object with the same name existing in audit table and storing the result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 5 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg5( database_name )  - Azure SQL Database name which we are using to read tables data from it
# One Sample function calling statement - CheckJobRule_FileNameValidation(JobId, ObjectPath, ObjectName,server_name,database_name)
# One Function calling statement with Example value -
#CheckJobRule_FileNameValidation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv',#'testsql-ss','testsqldb-ss')
# ------------------------------------------------------------------------------------------------------------------------------------- #


def CheckJobRule_FileNameValidation(JobId, ObjectPath, ObjectName,server_name,database_name,ObjectType, sqlusername, sqlpassword):
    
    try:
        RuleId = int(4)
        
        # Declaring function level variables
        Source_Value_Type = "Object Name"
        Target_Value_Type = "Object Name"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #### Fetching Object Data ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name not like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)
        #### Checking Validation Condition ####
        AuditTable_df = int(AuditTable_df.filter(AuditTable_df.File_Name == ObjectName).count())

        #### Checking the condition and storing the result ####
        if (AuditTable_df > 0):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'

        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(ObjectName), str(ObjectName), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out = 'FileNameValidation passed'
        else:
            out = 'FileNameValidation Failed'

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# ------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_FileSizeValidation
# Purpose - Fetching the Object Size value from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Value and then fetch the object size value for the same object from Filemetadata azure sql table as target value and then then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 5 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( server_name )  - Azure SQL Server name which we are using to read tables data from it.
# Arg5( database_name )  - Azure SQL Database name which we are using to read tables data from it.
# One Sample function calling statement - CheckJobRule_FileSizeValidation(JobId, ObjectPath, ObjectName,server_name,database_name)
# One Function calling statement with Example value -
#CheckJobRule_FileSizeValidation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv',#'testsql-ss','testsqldb-ss')
# ------------------------------------------------------------------------------------------------------------------------------------ #

def CheckJobRule_FileSizeValidation(JobId, ObjectPath, ObjectName,server_name,database_name,ObjectType, sqlusername, sqlpassword):
    try:
        RuleId = int(5)
        
        # Declaring function level variables
        Source_Value_Type = "Source Object Size"
        Target_Value_Type = "Target Object Size"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #### Fetching all the pre processed Object data from Audit Table(Source) ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name not like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching Source Value(File Size) for a particular Object ####
        SourceValue = AuditTableFileCount_pdf.loc[0]['File_Size']

        #### Fetching all the pre processed Object data from FileMetadata Table(Target) ####
        #Querydata = "Select * from metaabc.File_MetaData"
        FileMetadata_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_3)
        FileMetadata_df = FileMetadata_df.filter(FileMetadata_df.FileName == ObjectName)
        FileMetadata_pdf = FileMetadata_df.toPandas()

        #### Fetching Target Value(File Size) for a particular Object ####
        TargetValue = FileMetadata_pdf.loc[0]['FileSize']

        #### Checking the condition and storing the result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'
        
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out5 = str('File Size Validation passed')
        else:
            out5 = str('File Size Validation Failed')

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out5}"
        logs_info.append(log)
        
        return out5
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_Missing_FileCheck_Validation
# Purpose - Fetching the Object File Arrival Time from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Value and then fetch the Buffer time for the same object from Filemetadata azure sql table and then calculate the positive and negative buffer value for the object and check is the object arriving in that time range or not as target value and storing the result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 5 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg5( database_name )  - Azure SQL Database name which we are using to read tables data from it
# One Sample function calling statement - CheckJobRule_Missing_FileCheck_Validation(JobId, ObjectPath, #ObjectName,server_name,database_name)
# One Function calling statement with Example value -
#CheckJobRule_Missing_FileCheck_Validation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','testsql-ss','testsqldb-ss')
# -------------------------------------------------------------------------------------------------------------------------------------- #

def CheckJobRule_Missing_FileCheck_Validation(JobId, ObjectPath, ObjectName,server_name,database_name,ObjectType, sqlusername, 
                                              sqlpassword):
    
    try:
        RuleId = int(7)
        
        # Declaring function level variables
        Source_Value_Type = "Source Object Arrival Time"
        Target_Value_Type = "Target Expected Time"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #### Fetching data from Audit Table(Source) ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name not like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching File Arrival Time for a particular Object ####
        Source_FileNameValue = AuditTableFileCount_pdf.loc[0]['File_Name']
        FileArrival_Time = AuditTableFileCount_pdf.loc[0]['File_Arrival_Time']

        #### Fetching Source Value (Object Arrival Time) for a particular Object ####
        File_Arrival_Time = FileArrival_Time.strftime("%H:%M:%S")

        #### Fetching data from Metadata Table(Target) ####
        #Querydata = "Select * from metaabc.File_MetaData"
        FileMetadata_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_3)
        FileMetadata_df = FileMetadata_df.filter(FileMetadata_df.FileName == ObjectName)
        FileMetadata_pdf = FileMetadata_df.toPandas()

        #### Fetching File Name Time for a particular Object ####
        Target_FileNameValue = FileMetadata_pdf.loc[0]['FileName']

        #### Fetching File Buffer Time for a particular Object ####
        File_Expected_Time = FileMetadata_pdf.loc[0]['File_Expected_Time']

        #### Fetching File Arrival Time for a particular Object ####
        File_Buffer_Time = FileMetadata_pdf.loc[0]['File_Buffer_Time']

        #### Calculating Positive and Negative Buffer time ####
        File_Buffer_Time = File_Buffer_Time / 60
        Postive_Buffer_Time = File_Expected_Time + timedelta(hours=File_Buffer_Time)
        Postive_Buffer_Time = Postive_Buffer_Time.strftime("%H:%M:%S")
        Negative_Buffer_Time = File_Expected_Time - timedelta(hours=File_Buffer_Time)
        Negative_Buffer_Time = Negative_Buffer_Time.strftime("%H:%M:%S")

        #### Checking the condition and storing the result ####
        if (Source_FileNameValue == Target_FileNameValue) and (Negative_Buffer_Time < File_Arrival_Time < 
                                                               Postive_Buffer_Time):
            TargetValue = 'File has arrived in the time interval from ' + str(Negative_Buffer_Time) + ' to ' + str(Postive_Buffer_Time)
            RuleStatus = "Passed"
        else:
            TargetValue = 'File has not arrived in the time interval from ' + str(Negative_Buffer_Time) + ' to ' + str(Postive_Buffer_Time)
            RulesStatus = "Failed"

        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(File_Arrival_Time), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out = 'Missing_FileCheck_Validation passed'
        else:
            out = 'Missing_FileCheck_Validation Failed'

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_FileArrival_Validation
# Purpose - Fetching the Object File Arrival Time from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Value and then fetch the Buffer time for the same object from Filemetadata azure sql table and then calculate the positive and negative buffer value for the object and check is the object arriving in that time range or not and based on that assiging the value as ontime, late as target value and storing the result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 5 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( Objectpath )  - File Path for a adls or NAS file for which we are running validation checks.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg5( database_name )  - Azure SQL Database name which we are using to read tables data from it
# One Sample function calling statement - CheckJobRule_FileArrival_Validation(JobId, ObjectPath, #ObjectName,server_name,database_name)
# One Function calling statement with Example value -
#CheckJobRule_FileArrival_Validation(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','testsql-ss','testsqldb-ss')
# ------------------------------------------------------------------------------------------------------------------------------------- #

def CheckJobRule_FileArrival_Validation(JobId, ObjectPath, ObjectName,server_name,database_name,ObjectType, sqlusername, sqlpassword):
    
    try:
        RuleId = int(6)
        
        # Declaring function level variables
        Source_Value_Type = "Source Object Arrival Time"
        Target_Value_Type = "Target Object Arrival Time"
        if(ObjectType == 'File'):
            Source_Name = "Audit Table"
            Target_Name = "ADLS Raw Layer"
            
        if(ObjectType == 'NASFile'):
            Source_Name = "Audit Table"
            Target_Name = "NAS Drive"
            
        if(ObjectType == 'SQLTable'):
            Source_Name = "Audit Table"
            Target_Name = "Azure SQL Server"

        #### Fetching data from Audit Table(Source) ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name not like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_1)

        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching File Name for a particular Object ####
        Source_FileNameValue = AuditTableFileCount_pdf.loc[0]['File_Name']

        #### Fetching File Arrival Time for a particular Object ####
        FileArrival_Time = AuditTableFileCount_pdf.loc[0]['File_Arrival_Time']

        #### Formating the Time value ####
        File_Arrival_Time = FileArrival_Time.strftime("%H:%M:%S")

        #### Fetching data from FileMetadata Table(Target) ####
        #Querydata = "Select * from metaabc.File_MetaData"
        FileMetadata_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_3)
        FileMetadata_df = FileMetadata_df.filter(FileMetadata_df.FileName == ObjectName)
        FileMetadata_pdf = FileMetadata_df.toPandas()

        #### Fetching File Name for a particular Object ####
        Target_FileNameValue = FileMetadata_pdf.loc[0]['FileName']

         #### Fetching File Expected Time for a particular Object ####
        File_Expected_Time = FileMetadata_pdf.loc[0]['File_Expected_Time']

         #### Fetching File Buffer Time for a particular Object ####
        File_Buffer_Time = FileMetadata_pdf.loc[0]['File_Buffer_Time']

        #### Formating and calculating File Buffer Time value ####
        File_Expected_Time_tt = File_Expected_Time.strftime("%H:%M:%S")
        File_Buffer_Time = File_Buffer_Time / 60

        Postive_Buffer_Time = File_Expected_Time + timedelta(hours=File_Buffer_Time)
        Postive_Buffer_Time = Postive_Buffer_Time.strftime("%H:%M:%S")
        Negative_Buffer_Time = File_Expected_Time - timedelta(hours=File_Buffer_Time)
        Negative_Buffer_Time = Negative_Buffer_Time.strftime("%H:%M:%S")
        
        TargetValue = 'Postive_Buffer_Time = ' + str(Postive_Buffer_Time) + ' and Negative_Buffer_Time = ' + str(Negative_Buffer_Time)


        #### Checking the condition and storing the result ####
        if (Source_FileNameValue == Target_FileNameValue) and Negative_Buffer_Time <= File_Arrival_Time <= File_Expected_Time_tt:
            RuleStatus = "On Time"
        else:
            RuleStatus = "Delay"
        
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(File_Arrival_Time), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'On Time' or RuleStatus == 'Delay'):
            out = 'FileArrival_Validation passed'
        else:
            out = 'FileArrival_Validation Failed'

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_BalanceAmountValidation_PostFileProcessing
# Purpose - Fetching the Balance amount column value from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Value and then fetch the whole data for the same object from ADLS File which we copied from different sources like NAS , ADLS, SQL Server and then storing it in spark dataframe and calculating the balance amount for particular column as target value then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 7 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( ObjectPath_PostProcessing )  - ADLS file path of object after we processed and saved in adls.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( BalanceAmountColumn )  - Name of a column from table or file for which we will calculate balance amount.
# Arg5( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg6( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg7( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - CheckJobRule_BalanceAmountValidation_PostFileProcessing(JobId, ObjectPath_PostProcessing, ObjectName, BalanceAmountColumn,server_name,database_name,FileType)
# One Function calling statement with Example value -
#CheckJobRule_BalanceAmountValidation_PostFileProcessing(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','SALARY','testsql-ss','testsqldb-ss','csv')
# ------------------------------------------------------------------------------------------------------------------------------------- #

def CheckJobRule_BalanceAmountValidation_PostFileProcessing(JobId, ObjectPath_PostProcessing, ObjectName,
                                                            BalanceAmountColumn,server_name,database_name,FileType, sqlusername, 
                                                            sqlpassword):
    try:
        RuleId = int(9)
        
        # Declaring function level variables
        Source_Value_Type = "Source Balance Amount Post Object Processing"
        Target_Value_Type = "Target Balance Amount Post Object Processing"
        Source_Name = "Audit Table"
        Target_Name = "ADLS"

        #### Fetching all the Post processed Object data from Audit Table(Source) ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_4)
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching Balance Amount for a particular Object ####
        SourceValue = int(AuditTableFileCount_pdf['File_Balance_Amount'])

        
        #Querydata = "Select FileName,BalanceAmountColumn from metaabc.File_MetaData"
        FileMetaData_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_2)
        FileMetaDataFilter_df = FileMetaData_df.filter(FileMetaData_df.FileName == ObjectName)
        BalanceAmountColumn1 = FileMetaDataFilter_df.collect()[0][1]

        #### Checking Object Type wheather is it Parquet or not and based on that further processing it ####
        if(FileType == 'parquet'):
            #### Reading parquet File ####
            try:
                RawLogData_df = spark.read.parquet(ObjectPath_PostProcessing)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message
        else:
            try:
                #### Reading Other Files ####
                RawLogData_df = spark.read.load(path=ObjectPath_PostProcessing, format=f"{FileType}", header = True)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        #### Calculating Balance amount value post file processing ####
        BalanceAmount = RawLogData_df.agg({BalanceAmountColumn: 'sum'})
        for col in BalanceAmount.dtypes:
            TargetValue = int(BalanceAmount.first()[col[0]])


        #### Checking the condition and storing the result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'
        
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out = 'BalanceAmountValidation Post File Processing passed'
            
        else:
            out = 'BalanceAmountValidation Post File Processing Failed'
            

        #### Returning the validation rule result to the child notebook  ####
        
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message

# -------------------------------------------------------------------------------------------------------------------------------------- #
# FunctionName - CheckJobRule_CountValidation_PostFileProcessing
# Purpose - Fetching the record count from Audit Table by stablizing the connection with Azure SQL server for a particular object as Source Count and then fetch the record count value for the same object from ADLS File which we copied from different sources like NAS , ADLS, SQL Server and then then comparing the Source value and target value and storing the comparison result in string and returning the string as function output to the main wrapper function.
# Arguments - No. of arguments expected 6 
# Arg1( JobId )  - Databricks Job Id 
# Arg2( ObjectPath_PostProcessing )  - ADLS file path of object after we processed and saved in adls.
# Arg3( ObjectName )  - Name of the file or azure sql table for which we are running validation checks.
# Arg4( server_name )  - Azure SQL Server name which we are using to read tables data from it
# Arg5( database_name )  - Azure SQL Database name which we are using to read tables data from it
# Arg6( FileType )  - type of file like .csv, .json, .parquet
# One Sample function calling statement - wrapperFunction(JobId,ObjectPath_PostProcessing, ObjectName, 
# server_name,database_name,FileType)
# One Function calling statement with Example value -
#wrapperFunction(461636582315684,'abfss://validationrule@adlstoadls.dfs.core.windows.net/','employees_20221215T180510.csv','testsql-ss','testsqldb-ss','csv')
# ------------------------------------------------------------------------------------------------------------------------------------- #

def CheckJobRule_CountValidation_PostFileProcessing(JobId, ObjectPath_PostProcessing, ObjectName, server_name, database_name, 
                                                    FileType, sqlusername, sqlpassword):
    
    try:
        RuleId = int(8)
        # Declaring function level variables
        Source_Value_Type = "Source Count Post Object Processing"
        Target_Value_Type = "Target Count Post Object Processing"
        Source_Name = "Audit Table"
        Target_Name = "ADLS"

        #### Fetching all the Post processed Object data from Audit Table(Source) ####
        #Querydata = "Select * from abc.Audit_Log  where Product_Name  like 'Post%' "
        AuditTable_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_4)
        AuditTableFileCount_df = AuditTable_df.filter(AuditTable_df.File_Name == ObjectName)
        AuditTableFileCount_pdf = AuditTableFileCount_df.toPandas()

        #### Fetching Source Count for a particular Object ####
        SourceValue = int(AuditTableFileCount_pdf['File_Count'])

        #### Checking Object Type wheather is it Parquet or not and based on that further processing it ####
        if(FileType == 'parquet'):
            #### Reading parquet Files ####
            try:
                RawLogData_df = spark.read.parquet(ObjectPath_PostProcessing)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message
        else:
            #### Reading Other Files ####
            try:
                RawLogData_df = spark.read.load(path=ObjectPath_PostProcessing, format=f"{FileType}", header = True)
            except Exception as ex:
                current_time = datetime.now()
                error_message = "\n Error Message : " + str(ex)
                log = f"{current_time} Error Occured {error_message}"
                logs_info.append(log)
                # Converting List of Log Message into String
                string_log_info = "\n".join(logs_info)
                # storing log messages in adls location 
                store_logs_in_adls(string_log_info)
                return error_message

        #### Fetching Target Count for a particular Object ####
        TargetValue = int(RawLogData_df.count())

        #### Checking the condition and storing the result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'
        
        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]
        
        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out = 'CountValidation Post File Processing passed'
           
        else:
            out = 'CountValidation Post File Processingn Failed'
            
        log = f"{Created_Time} {out}"
        logs_info.append(log)
        #### Returning the validation rule result to the child notebook  ####
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
def CheckJobRule_CountValidation_Egress(JobId, ObjectPath, ObjectName, server_name, database_name, FileType, sqlusername, sqlpassword):
    try:
        RuleId = int(10)

        # Declaring function level variables
        Source_Value_Type = "Source Count for Egress Object"
        Target_Value_Type = "Target Count for Egress Object"
        Source_Name = "ADLS"
        Target_Name = "SQL Server"

        #### Checking Object Type wheather is it Parquet or not and based on that further processing it ####
        try:
            RawLogData_df = spark.read.parquet(ObjectPath)
        except Exception as ex:
            current_time = datetime.now()
            error_message = "\n Error Message : " + str(ex)
            log = f"{current_time} Error Occured {error_message}"
            logs_info.append(log)
            # Converting List of Log Message into String
            string_log_info = "\n".join(logs_info)
            # storing log messages in adls location 
            store_logs_in_adls(string_log_info)
            return error_message

        #### Fetching Source Count for a particular Object ####
        SourceValue = int(RawLogData_df.count())

        #### Fetching all the Post processed Object data from Audit Table(Source) ####
        Querydata_5 = "Select count(*) as Target_Value from SalesLT.formula1dl_results"
        TargetValue_df = commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,Querydata_5)
        TargetValue_pdf = TargetValue_df.toPandas()
        #### Fetching Target Count for a particular Object ####
        TargetValue = int(TargetValue_pdf['Target_Value'])

        #### Checking the condition and storing the result ####
        if (SourceValue == TargetValue):
            RuleStatus = 'Passed'
        else:
            RuleStatus = 'Failed'

        Created_Time = str(datetime.now())
        New_date = Created_Time[0:23]

        # Calling commonInsertFunction to insert validation rule result into SQL ABC table
        commonInsertFunction(server_name, database_name, sqlusername, sqlpassword, TableName, JobId, RuleId, 
                             str(SourceValue), str(TargetValue), Source_Value_Type, Target_Value_Type, Source_Name, 
                             Target_Name, RuleStatus, New_date, Username)

        if (RuleStatus == 'Passed'):
            out = 'CountValidation for Egress passed'

        else:
            out = 'CountValidation for Egress Failed'

        #### Returning the validation rule result to the child notebook  ####
        return out
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
        

    
def commonInsertFunction(ServerName, DatabaseName, jdbcUsername, jdbcPassword, TableName, Job_Id, Rule_Id, Source_Value, 
                         Target_Value, Source_Value_Type, Target_Value_Type, Source_Name, Target_Name, Rule_Run_Status, 
                         Created_Time, Created_By):
    try:
        # Declaring function level variables
        pyodbc_conn = "Driver={ODBC Driver 17 for SQL Server};Server="
        pyodbc_server = ".database.windows.net;Database="
        UID = ";UID="
        PWD = ";PWD="
        insert_statement = "Insert into "
        tables_name = " (Job_Id, Rule_Id, Source_Value, Target_Value, Source_Value_Type, Target_Value_Type, Source_Name, Target_Name, Rule_Run_Status, Created_Time, Created_By) Values(" 
        
    
#        cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};Server=" + ServerName + ".database.windows.net;Database=" + DatabaseName + ";UID=" + jdbcUsername + ";PWD=" + jdbcPassword + ";")
        
        cnxn_str = (pyodbc_conn + ServerName + pyodbc_server + DatabaseName + UID + jdbcUsername + PWD + jdbcPassword + ";")

        #### Connecting with pyodbc with the above created connection to perform the insert and update query in SQL table 
        cnxn = pyodbc.connect(cnxn_str)

        #### Creating a pyodbc connection object ####
        cursor = cnxn.cursor()
            
        #### Creating Insert SQL query  ####
        
        #query = "Insert into "+ TableName + " (Job_Id, Rule_Id, Source_Value, Target_Value, Source_Value_Type, Target_Value_Type, Source_Name, Target_Name, Rule_Run_Status, Created_Time, Created_By) Values(" + str(Job_Id) +  "," + str(Rule_Id) + ",'" + Source_Value + "','" + Target_Value + "','" + Source_Value_Type + "','" + Target_Value_Type + "','" + Source_Name + "','" + Target_Name + "','" + Rule_Run_Status + "','" + Created_Time + "','" + Created_By + "')"
        
        query = insert_statement + TableName + tables_name + str(Job_Id) +  "," + str(Rule_Id) + ",'" + Source_Value + "','" + Target_Value + "','" + Source_Value_Type + "','" + Target_Value_Type + "','" + Source_Name + "','" + Target_Name + "','" + Rule_Run_Status + "','" + Created_Time + "','" + Created_By + "')"
        
        
        #### Executing the Insert query to the sql table with the help of pyodbc object ####
        cursor.execute(query)

        #### Committed the changes so it will reflect in the original sql table ####
        cnxn.commit()
        
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
        
def commonSQLFunction(server_name,database_name,sqlusername,sqlpassword,sqlquery):
    
    try:
        ### Inserting validation rule result into SQL ABC table
        Common_df = spark.read.format("jdbc") \
            .option("url", f"jdbc:sqlserver://{server_name}.database.windows.net:1433;database={database_name}") \
            .option("query", sqlquery) \
            .option("user", sqlusername) \
            .option("password", sqlpassword) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .load()
        return Common_df
    
    except Exception as ex:
        error_message = "\n Error Message : " + str(ex)
        current_time = datetime.now()
        log = f"{current_time} Error Occured {error_message}"
        logs_info.append(log)
        # Converting List of Log Message into String
        string_log_info = "\n".join(logs_info)
        # storing log messages in adls location 
        store_logs_in_adls(string_log_info)
        return error_message
    
