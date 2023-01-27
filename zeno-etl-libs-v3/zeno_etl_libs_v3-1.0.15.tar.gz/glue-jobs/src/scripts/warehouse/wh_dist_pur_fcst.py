# -*- coding: utf-8 -*-
"""
Created on Wed May 4 11:52:28 2022

@author: vivek.sidagam@zeno.health

Purpose: To generate distributor level forecast at warehouse for the next month
"""
import math
import os
import sys
import argparse

import pandas as pd
import ast
import numpy as np
from datetime import datetime, timedelta
from calendar import monthrange


sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB, MongoDB, MSSql
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger, send_logs_via_email
from zeno_etl_libs.helper.email.email import Email

from zeno_etl_libs.utils.warehouse.data_prep.wh_data_prep \
    import get_launch_stock_per_store

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="To generate distributor level forecast at warehouse for the next month.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to', default="vivek.sidagam@zeno.health",
                        type=str, required=False)
    parser.add_argument('-nso', '--nso_history_days', default=90, type=int,
                        required=False)

    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    email_to = args.email_to
    nso_history_days = args.nso_history_days

    logger = get_logger()
    logger.info("Script begins")

    status = False
    err_msg = ''
    df_uri = ''
    run_date = str(datetime.now().date())
    current_month_date = (
            datetime.now().date() -
            timedelta(days=datetime.now().day - 1))
    next_month_date = datetime(current_month_date.year + \
                               int(current_month_date.month / 12), \
                               ((current_month_date.month % 12) + 1), 1).date()
    num_days = monthrange(next_month_date.year, next_month_date.month)[1]

    try:
        df = pd.DataFrame()
        rs_db = DB()
        rs_db.open_connection()
        # MSSql connection
        #mssql = MSSql(connect_via_tunnel=False)
        #mssql_connection = mssql.open_connection()
        q1 = """
                select
            wis."drug-id"  as "drug_id",
            SUM(wis."balance-quantity") as "balance_quantity",
            SUM(wis."locked-quantity") as "locked_quantity"
        from
            "prod2-generico"."prod2-generico"."wh-inventory-ss" wis
        where
            date(wis."snapshot-date")= current_date
            and wis."wh-id" in (199,342) 
        group by wis."drug-id" 
        """
        #wh_inventory = pd.read_sql(q1, )

        wh_inventory=rs_db.get_df(q1)

        logger.info("data pulled from RS")

        wh_inventory['drug_id'] = pd.to_numeric(wh_inventory['drug_id'])

        wh_inventory = wh_inventory.astype(int, errors='ignore')

        wh_inventory['total_quantity'] = wh_inventory['balance_quantity'] + wh_inventory['locked_quantity']

        # get wh portfolio
        drugs_list = rs_db.get_df(
            '''
                  select
                wssm."drug-id" as drug_id,
                d."drug-name" as drug_name,
                f.fcst,
                f.ss,
                f.rop,
                f.oup,
                f."max-review-period"
            from
                "prod2-generico"."wh-sku-subs-master" wssm
             join (
                select
                    "drug-id",
                    fcst,   
                    "safety-stock" as ss,
                    "reorder-point" as rop,
                    "order-upto-point" as oup,
                    wss."max-review-period" as "max-review-period"
                from
                    "prod2-generico"."wh-safety-stock" wss
                where
                    "forecast-date" = (
                    select
                        max("forecast-date")
                    from
                        "prod2-generico"."wh-safety-stock")) f on
                f."drug-id" = wssm."drug-id"
            left join "prod2-generico".drugs d on
                d.id = wssm."drug-id"
            where
                wssm."add-wh" = 'Yes'
                and d."type" <> 'discontinued-products'
                and d.company <> 'GOODAID'
            ''')

        drugs_list.fillna(0, inplace=True)

        drugs_list = drugs_list.astype(int, errors='ignore')

        # getting params

        # logger.info('reading input file to get expected_nso')
        #
        # params_table_raw = """
        #     select
        #         "month-begin-dt" as month_begin_dt,
        #         value as expected_nso
        #     from
        #         "prod2-generico"."wh-forecast-repln-input"
        #     where
        #         "param-name" = 'expected_nso'
        # """
        # params_table = rs_db.get_df(params_table_raw)
        # params_table = params_table.apply(pd.to_numeric, errors='ignore')
        # try:
        #     expected_nso = int(params_table[
        #                            params_table['month_begin_dt'] == next_month_date]['expected_nso'])
        # except Exception as error:
        #     expected_nso = 0
        #
        # logger.info('expected_nso parameter read --> ' + str(expected_nso))
        # logger.info('nso_history_days --> ' + str(nso_history_days))

        # getting launch stock per store
        #launch_stock_per_store = get_launch_stock_per_store(rs_db, nso_history_days)
        #logger.info('launch stock per store pulled')
        #drugs_list = drugs_list.merge(launch_stock_per_store, on='drug_id', how='left')
        #drugs_list['launch_stock_per_store'].fillna(0, inplace=True)
        #drugs_list['fcst'] += drugs_list['launch_stock_per_store'] * expected_nso
        #drugs_list['fcst'] = drugs_list['fcst'].round().astype(int)
        #del drugs_list['launch_stock_per_store']

        df = drugs_list.copy()

        df = df.merge(wh_inventory, on='drug_id', how='left')

        df=df.fillna(0)

        preferred_distributor='''
        select
        "drug-id" as "drug_id" ,
        pd."distributor-id" as "distributor_1" ,
        pd."distributor-name" as "distributor_name_1"
        from
        "prod2-generico"."prod2-generico"."preferred-distributor" pd
        where pd."is-active" ='True'
        '''

        preferred_distributor = rs_db.get_df(preferred_distributor)

        df=pd.merge(df,preferred_distributor,how='left',on='drug_id')


        review_time='''
        select
            "distributor-id" as "distributor_1",
            "review-days" as "review_time",
            wdrt."weekly-po" 
        from
            "prod2-generico"."prod2-generico"."wms-distributors-review-time" wdrt
        Where  wdrt."is-active" ='True'
        '''

        review_time=rs_db.get_df(review_time)

        df=pd.merge(df,review_time,how='left',on='distributor_1')

        #day_of_week = next_month_date.strftime("%A")

        #df['weekly-po'][0]


        #df['day_condition']=df['weekly-po'].apply(lambda a:True if not pd.isnull(a) and  day_of_week in a and isinstance(a, str)\
                                                    #else False)

        #df['number-of-orders']=df['max-review-period'].copy().\
            #apply(lambda a: 10 if (a==3 & df['day_condition']==False)  else 9)


        #df['number-of-orders'] = np.round(28/df['max-review-period'])

        df['max-review-period'].unique()

        df['number-of-orders']=df['max-review-period'].copy().apply(lambda a: 10 if a==3 else( 5 if a==7 else 7 if a==4 else 0))


        df['daily_demand']=math.ceil(df['fcst']/31)


        df['consumption']=np.round(df['daily_demand']*df['max-review-period'])

        #Purchase in first order


        df['below_oup'] = np.where(df['total_quantity']>= df['oup'], True, False)

        df.loc[df['below_oup'] == False, 'purchase_quantity_1'] = df['oup']-df['total_quantity']

        df.loc[df['below_oup'] == True, 'purchase_quantity_1'] = 0

        df_new=df

        df=df_new

        df['current_inv'] = df['total_quantity']

        df['purchase_quantity'] = df['purchase_quantity_1']

        df['current_inv'] = df['current_inv'] + df['purchase_quantity'] - df['consumption']

        df['purchase_quantity_new'] = df['purchase_quantity']


        for i in range(len(df)) :
            a=int(df['number-of-orders'][i])
            for j in range( 0,a-1):
                if int(df['oup'][i])> int(df['current_inv'][i]):
                    df.loc[i,'purchase_quantity']=(df['oup'][i]-df['current_inv'][i])
                    df.loc[i,'current_inv']=df['current_inv'][i] + df['purchase_quantity'][i] - df['consumption'][i]
                    df.loc[i,'purchase_quantity_new']=df['purchase_quantity_new'][i]+df['purchase_quantity'][i]
                else:
                    df['purchase_quantity']=0
                    df.loc[i,'current_inv']=df['current_inv'][i]-df['consumption'][i]


        df['purchase_quantity_new'] = np.where(df['purchase_quantity_new'] <= 0, 0,df['purchase_quantity_new'] )

        #df_pref=pd.read_csv(r"D:\review_time& preferred distributor\preferred_distributors.csv")
        #s3=S3()
        #df_pref=pd.read_csv(s3.download_file_from_s3(file_name="warehouse/preferred_distributors.csv"))

        #df_new=pd.merge(df,df_pref,how='left',on='drug_id')

        #store_quantity='''
        
        
        #'''

        #store_quantity= rs_db.get_df(store_quantity)

        #df_new_1=pd.merge(df_new,store_quantity,how='left',on='drug_id')

        df_new.to_csv(r"D:\acsv_files\warehouse_m_1\purchase_m+1_new_1_jan_2023.csv")

























        #if df['below_rop']==False:
            #df['number_of_cycle']=np.ceil((df['fcst'] - (df['total_quantity'] - df['rop']))/(
                    #df['oup'] - df['rop']) )
            #df['total_value']=df['number_of_cycle']*(df['oup']-df['rop'])
            #df['required']=df['fcst'] - (df['total_quantity'] - df['rop'])


        #df.loc[df['below_rop'] == False, 'purchase_quantity'] = np.ceil(
            #(df['fcst'] - (df['total_quantity'] - df['rop'])) / (
                    #df['oup'] - df['rop']) ) * (df['oup'] - df['rop'])

        #df.loc[df['below_rop'] == True, 'purchase_quantity'] = np.ceil(
            #df['oup'] - (df['total_quantity'] - 4 * df['fcst'] / num_days)) + (
                                                                       #df['oup'] - df['rop']) * np.ceil(
            #(df['fcst'] - np.ceil(df['oup'] - (
                    #df['total_quantity'] - 4 * df['fcst'] / num_days))) / (
                    #f['oup'] - df['rop']) )

        df['purchase_quantity'].fillna(0, inplace=True)

        df.loc[df['purchase_quantity'] <= 0, 'purchase_quantity'] = 0

        del df['below_rop']

        df['purchase_quantity'] = df['purchase_quantity'].astype(int)

        df.to_csv(r"D:\acsv_files\warehouse_m_1\drug_purchase.csv")



        #mg_db = MongoDB()
        #mg_client = mg_db.open_connection("generico-crm")

        #db = mg_client['generico-crm']
        #collection = db["wmsDrugDistributorMappingV2"].find(
            #{
                #"is_active" : "true"
            #},
            #{
                #"drug_id": "$drug_id",
                #"rank1": "$rank1",
                #"rank1_name": "$rank1_name"
            #}
        #)
        #dist_list = pd.DataFrame(list(collection))

        s3 = S3()

        df_uri = s3.save_df_to_s3(df=df, file_name='wh_dist_pur_fcst_{date}.csv'.format(date=str(next_month_date)))

        status = True

    except Exception as error:
        err_msg = str(error)
        logger.exception(str(error))

    # Sending email
    email = Email()
    if status:
        result = 'Success'
        email.send_email_file(subject='''Warehouse distributor M+1 purchase forecast for {date} ({env}): {result} 
        '''.format(date=str(next_month_date), env=env, result=result),
                              mail_body=f"Run time: {datetime.now()} {err_msg}",
                              to_emails=email_to, file_uris=[df_uri])
    else:
        result = 'Failed'
        email.send_email_file(subject='''Warehouse distributor M+1 purchase forecast for {date} ({env}): {result} 
        '''.format(date=str(next_month_date), env=env, result=result),
                              mail_body=f"Run time: {datetime.now()} {err_msg}",
                              to_emails=email_to, file_uris=[])

    logger.info("Script ended")
