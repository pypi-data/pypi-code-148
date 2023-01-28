import streamlit as st
import sqlite3
import pandas as pd



def Convert_cols(column,dtype,data):
    data[column] = data[column].astype(dtype)
    return data

def Unary_op(df,tabs,conn,data):
    col_name = st.text_input("Input the name for the column","column")
    col = st.selectbox("select the column for the operation",[i for i in data.columns])
    num = st.number_input("Input Number",0)
    operator = st.selectbox("Select operation to perform",["+","-","*","/","**"])
    choice = st.selectbox("Select an option:", ['True','False'])
    if operator == "+":
        df[col_name] = df[col] + num
        st.write(df)
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "-":
        df[col_name] = df[col] - num
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "*":
        df[col_name] = df[col] * num
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "/":
        df[col_name] = df[col] / num
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "**":
        df[col_name] = df[col]** num
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        
def Binary_op(df,tabs,conn,data):
    col_name = st.text_input("Input the name for the column","column")
    col_1 = st.selectbox("select first column for the operation",[i for i in data.columns])
    col_2 = st.radio("Select second column for the operation:", [i for i in data.columns])
    operator = st.selectbox("Select operation to perform",["+","-","*","/","**"])
    choice = st.selectbox("Select an option:", ['True','False'])
    if operator == "+":
        df[col_name] = df[col_1] + df[col_2]
        st.write(df)
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "-":
        df[col_name] = df[col_1] - df[col_2]
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "*":
        df[col_name] = df[col_1] * df[col_2]
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "/":
        df[col_name] = df[col_1] / df[col_2]
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
    elif operator == "**":
        df[col_name] = df[col_1]** df[col_2]
        if choice == 'True' :
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
        else :
            df.drop(col_name,axis=1,inplace=True)
            df.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
            return df
def Add_values(tabs,conn):
    #table_name = input("Select A table")
    values = st.text_input("Input the values")
    values = values.split(",")
    print(values)
    data = pd.read_sql_query(f'SELECT * FROM {tabs}', conn, index_col= None)
    print(len(data.columns))
    print(data.columns)
    df_1 = pd.DataFrame([values],columns= data.columns, index= None)
    print(df_1.columns)
    data = pd.concat([data,df_1], ignore_index=False)
    data.to_sql(f'{tabs}',conn,index= False, if_exists= 'replace')
    return data

def create_table(conn):
    columns = st.text_input("Input column names")
    columns = columns.split(",")
    table_name = st.text_input("Input table names")
    df = pd.DataFrame(columns=columns, index= None)
    df.to_sql(f"{table_name}",conn,index= False, if_exists= 'replace')
    st.write(df.columns)

def create_account(cursor,conn):
    username = st.text_input("Type Username")
    password = st.text_input("Type password")
    cursor.execute("INSERT INTO user(username, password) VALUES(?, ?)",(username,password))
    conn.commit()