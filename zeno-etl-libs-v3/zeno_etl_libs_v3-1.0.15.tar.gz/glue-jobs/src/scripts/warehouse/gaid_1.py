# -*- coding: utf-8 -*-
"""
Created on Wed May 4 11:52:28 2022

@author: akshay.bhutada@zeno.health

Purpose: To generate distributor level forecast at warehouse for the next month
"""


import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from dateutil.tz import gettz
from datetime import date, timedelta
import calendar
import math

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.utils.ipc.doid_update_ss import doid_update
from zeno_etl_libs.helper.parameter.job_parameter import parameter


#tag = parameters



env = "dev"

os.environ['env'] = env

logger = get_logger()




def gaid_forecast():

    job_params = parameter.get_params(job_id=125)
    email_to = job_params['email_to']

    logger = get_logger()
    logger.info("Scripts begins. Env = " + env)

    rs_db = DB()
    rs_db.open_connection()

    date=datetime.strptime('2022-09-01', '%Y-%m-%d')

    #date.today()

    this_month_first_date = date.replace(day=1)
    days_in_this_month = calendar.monthrange(this_month_first_date.year, this_month_first_date.month)[1]
    m_plus_1_month_first_date = date.replace(day=1) + timedelta(days=days_in_this_month)
    days_in_m_plus_1_month = calendar.monthrange(m_plus_1_month_first_date.year, m_plus_1_month_first_date.month)[1]
    m_plus_2_month_first_date = m_plus_1_month_first_date + timedelta(days=days_in_m_plus_1_month)
    days_in_m_plus_2_month = calendar.monthrange(m_plus_2_month_first_date.year, m_plus_2_month_first_date.month)[1]
    m_plus_3_month_first_date = m_plus_2_month_first_date + timedelta(days=days_in_m_plus_2_month)
    days_in_m_plus_3_month = calendar.monthrange(m_plus_3_month_first_date.year, m_plus_3_month_first_date.month)[1]

    this_month_first_date_str=str(this_month_first_date)

    final_df = pd.DataFrame()
    list_of_month = [1,2,3,4]



    for i in list_of_month:
        if i == 1 :
            month_start_date= this_month_first_date
            number_of_day_in_month = days_in_this_month
        elif i == 2:
            month_start_date = m_plus_1_month_first_date
            number_of_day_in_month = days_in_m_plus_1_month
        elif i == 3:
            month_start_date = m_plus_2_month_first_date
            number_of_day_in_month = days_in_m_plus_2_month
        elif i == 4:
            month_start_date = m_plus_3_month_first_date
            number_of_day_in_month = days_in_m_plus_3_month

        # read inputs file to get parameters
        logger.info('reading input file to get parameters')
        params_table_query = """
            select
                "param-name" as param,
                value
            from
                "prod2-generico"."wh-goodaid-forecast-input"
            where
                "param-name" not in ('drug_lvl_fcst_inputs' , 's_and_op_factors')
        """
        logger.info('input parameters read')
        params_table = rs_db.get_df(params_table_query)
        params_table = params_table.apply(pd.to_numeric, errors='ignore')

        days = 84
        # days = int(params_table.where(params_table['param'] == 'days', axis=0).dropna()['value'])
        expected_new_stores = int(params_table.where(
            params_table['param'] == 'expected_new_stores',
            axis=0).dropna()['value'])
        wh_id = int(params_table.where(params_table['param'] == 'gaw_id',
                                       axis=0).dropna()['value'])
        revenue_min = int(params_table.where(
            params_table['param'] == 'revenue_min', axis=0).dropna()['value'])
        revenue_max = int(params_table.where(
            params_table['param'] == 'revenue_max', axis=0).dropna()['value'])

        # get active gaid drugs list

        drugs_query = '''
            select
                wssm."drug-id" as drug_id,
                d.composition,
                d."drug-name" as drug_name,
                d.company,
                d."type",
                d.category
            from
                "prod2-generico"."wh-sku-subs-master" wssm
            left join "prod2-generico".drugs d on
                d.id = wssm."drug-id"
            where
                wssm."add-wh" = 'Yes'
                and d."type" not in ('discontinued-products')
                and d.company = 'GOODAID'
            '''
        drugs = rs_db.get_df(drugs_query)
        logger.info('active drugs list pulled from wssm')



        # get 28 days sales for active gaid drugs
        drug_sales_query = '''
            select
                "drug-id" as drug_id,
                SUM("net-quantity") as drug_sales_quantity
            from
                "prod2-generico".sales
            where
                "drug-id" in {drug_ids}
                and date("created-at") >= '{this_month_first_date_str}' - {days}
                and date("created-at") < '{this_month_first_date_str}'
            group by
                "drug-id"
        '''.format(this_month_first_date_str=this_month_first_date_str,days=days, drug_ids=tuple(drugs['drug_id']))
        drug_sales = rs_db.get_df(drug_sales_query)
        logger.info('drug sales data pulled from rs')
        drug_sales['drug_sales_quantity'] = drug_sales[
                                                'drug_sales_quantity'] * number_of_day_in_month / days

        # get non-ethical composition level sale
        composition_sales_query = '''
            select
                composition as composition,
                SUM("net-quantity") as composition_sales_quantity
            from
                "prod2-generico".sales
            where
                composition in {compositions}
                and date("created-at") >='{this_month_first_date_str}' - {days}
                and date("created-at") < '{this_month_first_date_str}'
                and "type" <> 'ethical'
            group by
                composition
        '''.format(this_month_first_date_str=this_month_first_date_str,days=days, compositions=tuple(drugs['composition']))
        composition_sales = rs_db.get_df(composition_sales_query)
        logger.info('composition data pulled from rs')

        composition_sales['composition_sales_quantity'] = composition_sales[
                                                              'composition_sales_quantity'] * number_of_day_in_month / days
        #composition_sales['composition_sales_quantity'] = 0
        # merging data
        main_df = drugs.merge(drug_sales, on='drug_id', how='left')
        main_df['drug_sales_quantity'].fillna(0, inplace=True)
        main_df = main_df.merge(composition_sales, on='composition',
                                how='left')
        main_df['composition_sales_quantity'].fillna(0, inplace=True)

        # getting 50% of composition level sales
        main_df['composition_sales_quantity_50%'] = main_df[
                                                        'composition_sales_quantity'] * 0.5
        main_df['composition_sales_quantity_50%'] = main_df[
            'composition_sales_quantity_50%'].round(0)

        # calculate month-on-month sales growth
        # getting last-to-last 28 day sales for calcuating growth factor
        last_to_last_sales_query = '''
            select
                "drug-id" as drug_id,
                SUM("net-quantity")/3 as last_to_last_28_day_sales
            from
                "prod2-generico".sales
            where
                "drug-id" in {drug_ids}
                and date("created-at") >= '{this_month_first_date_str}' - 112
                and date("created-at") < '{this_month_first_date_str}' - 28
            group by
                "drug-id"
        '''.format(this_month_first_date_str=this_month_first_date_str,drug_ids=tuple(drugs['drug_id']))
        last_to_last_sales = rs_db.get_df(last_to_last_sales_query)
        logger.info('last-to-last 28 day sales data pulled from rs')

        # getting last 28 day sales
        last_sales_query = '''
            select
                "drug-id" as drug_id,
                SUM("net-quantity") as last_28_day_sales
            from
                "prod2-generico".sales
            where
                "drug-id" in {drug_ids}
                and date("created-at") >= '{this_month_first_date_str}' - 28
                and date("created-at") < '{this_month_first_date_str}'
            group by
                "drug-id"
        '''.format(this_month_first_date_str=this_month_first_date_str,drug_ids=tuple(drugs['drug_id']))
        last_sales = rs_db.get_df(last_sales_query)
        logger.info('last 28 day sales data pulled from rs')

        # getting avg sales
        drug_maturity_query = '''
                select
                    s."drug-id" as "drug_id" ,
                    datediff(day ,
                    min(s."created-at"),
                    current_date) as "drug-age-in-days",
                    case
                        when datediff(day ,min(s."created-at"),current_date)>= 180 then 'Mature'
                        else 'New'
                    end as "drug-maturity"
                from
                    "prod2-generico"."prod2-generico".sales s
                where
                    s."company-id" = 6984
                group by
                    s."drug-id"
            '''
        drug_maturity = rs_db.get_df(drug_maturity_query)
        logger.info('fetched drug maturity')

        # merge to main_df
        main_df = main_df.merge(drug_maturity, on='drug_id', how='left')
        main_df['drug-age-in-days'].fillna(0, inplace=True)
        main_df['drug-maturity'].fillna('New', inplace=True)



        # merging to main_df
        main_df = main_df.merge(last_to_last_sales, on='drug_id', how='left')
        main_df['last_to_last_28_day_sales'].fillna(0, inplace=True)
        main_df = main_df.merge(last_sales, on='drug_id', how='left')
        main_df['last_28_day_sales'].fillna(0, inplace=True)
        main_df['growth_factor'] = main_df['last_28_day_sales'] / main_df[
            'last_to_last_28_day_sales']
        main_df['growth_factor'].fillna(1, inplace=True)
        main_df['growth_factor'] = np.where(main_df[
                                                'growth_factor'] == np.inf, 1,
                                            main_df['growth_factor'])
        # growth factor capped at 150% - min at 100%
        main_df['growth_factor'] = np.where(main_df[
                                                'growth_factor'] > 1.02, 1.02,
                                            main_df['growth_factor'])
        main_df['growth_factor'] = np.where(main_df[
                                                'growth_factor'] < 1, 1,
                                            main_df['growth_factor'])
        #main_df['growth_factor']=1
        # # growth factor foreced to 1 when 50% comp sales > drug sales
        # #main_df['growth_factor'] = np.where(main_df[
        #                                         'composition_sales_quantity_50%'] >
        #                                     main_df[
        #                                         'drug_sales_quantity'], 1,
        #                                     main_df['growth_factor'])
        # growth factor foreced to 1 when 50% comp sales > drug sales

        condition = [main_df['drug-maturity'] == 'Mature',
                     (main_df['drug-maturity'] == 'New') & main_df['drug_sales_quantity'] >= main_df[
                         'composition_sales_quantity_50%'],
                     (main_df['drug-maturity'] == 'New') & main_df['drug_sales_quantity'] < main_df[
                         'composition_sales_quantity_50%']]
        choice = [main_df['growth_factor'], main_df['growth_factor'], 1]
        main_df['growth_factor'] = np.select(condition, choice, default=main_df['growth_factor'])

        #main_df['growth_factor']=1

        # get s&op factor
        logger.info('reading s&op factors table')
        input_table_query = """
            select
                "drug-id" as drug_id,
                value as s_op_factor,
                "start-date" as start_date,
                "end-date" as end_date
            from
                "prod2-generico"."wh-goodaid-forecast-input"
            where
                "param-name" = 's_and_op_factors'  
        """
        s_op_table = rs_db.get_df(input_table_query)
        logger.info('s&op factors table read')
        s_op_table = s_op_table.apply(pd.to_numeric, errors='ignore')
        s_op_table = s_op_table[
            s_op_table['start_date'] <= datetime.now().date()]
        s_op_table = s_op_table[
            s_op_table['end_date'] >= datetime.now().date()]
        s_op_table.drop('start_date', axis=1, inplace=True)
        s_op_table.drop('end_date', axis=1, inplace=True)
        main_df = main_df.merge(s_op_table, on='drug_id', how='left')
        main_df['s_op_factor'].fillna(1, inplace=True)

        # get avg gaid sales for 13-16 lakh revenue stores
        # getting stores lists to compare with

        stores_cmp_query = '''
            select
                "store-id" as store_id,
                round(sum("revenue-value")) as revenue
            from
                "prod2-generico".sales
            where
                date("created-at") >= '{this_month_first_date_str}' - 28
                and date("created-at") < '{this_month_first_date_str}'
            group by
                "store-id"
        '''.format(this_month_first_date_str=this_month_first_date_str)
        stores_cmp = rs_db.get_df(stores_cmp_query)
        stores_cmp = stores_cmp[stores_cmp['revenue'] > revenue_min]
        stores_cmp = stores_cmp[stores_cmp['revenue'] < revenue_max]
        stores_list_to_comp = tuple(stores_cmp['store_id'])
        logger.info('list of stores with revenue between 1.3 and 1.6 mil -->'
                    + str(stores_list_to_comp))

        # adding expected_new_stores column
        main_df['expected_new_stores'] = expected_new_stores

        # getting avg sales
        avg_store_sales_query = '''
               select
                   composition ,
                   sum("net-quantity")/ {count} as avg_drug_sales_quantity
               from
                   "prod2-generico".sales
               where
                   composition in {compositions}
                   and date("created-at") >= '{this_month_first_date_str}' - 28
                   and date("created-at") < '{this_month_first_date_str}'
                   and "type" <> 'ethical'
                   and "store-id" in {stores_list_to_comp}
               group by
                   composition
           '''.format(this_month_first_date_str=this_month_first_date_str,\
                      compositions=tuple(drugs['composition']), \
                      stores_list_to_comp=stores_list_to_comp, \
                      count=len(stores_list_to_comp))
        avg_store_sales = rs_db.get_df(avg_store_sales_query)
        logger.info('avg composition sales retrieved for sample stores')
        avg_store_sales['avg_drug_sales_quantity'] = avg_store_sales[
            'avg_drug_sales_quantity'].round()

        # merge to main_df
        main_df = main_df.merge(avg_store_sales, on='composition', how='left')
        main_df['avg_drug_sales_quantity'].fillna(0, inplace=True)

        # # get final forecast figures
        # main_df['forecast'] = main_df[[
        #     'drug_sales_quantity',
        #     'composition_sales_quantity_50%']].max(axis=1)

        condition = [main_df['drug-maturity'] == 'Mature',
                     (main_df['drug-maturity'] == 'New') & main_df['drug_sales_quantity'] >= main_df[
                         'composition_sales_quantity_50%'],
                     (main_df['drug-maturity'] == 'New') & main_df['drug_sales_quantity'] < main_df[
                         'composition_sales_quantity_50%']]
        choice = [main_df['drug_sales_quantity'], main_df['drug_sales_quantity'],
                  main_df['composition_sales_quantity_50%']]
        main_df['forecast'] = np.select(condition, choice, default=main_df['drug_sales_quantity'])


        main_df['forecast'] = main_df['forecast'] * (main_df['growth_factor']**i) * main_df['s_op_factor'] + main_df[
                                  'expected_new_stores'] * \
                              main_df['avg_drug_sales_quantity']
        main_df['forecast'] = main_df['forecast'].round()

        main_df['forecast_date'] = month_start_date
        main_df['days_in_this_month'] = number_of_day_in_month

        # get input table and merge with main_df
        logger.info('reading input table')
        input_table_query = """
            select
                "drug-id" as drug_id,
                lead_time_doh,
                safety_stock_doh,
                review_period
            from
                "prod2-generico"."wh-goodaid-forecast-input"
            where
                "param-name" = 'drug_lvl_fcst_inputs'
        """
        input_table = rs_db.get_df(input_table_query)
        logger.info('input table read')
        input_table = input_table.apply(pd.to_numeric, errors='ignore')
        input_table['reorder_point_doh'] = input_table['lead_time_doh'] + \
                                           input_table['safety_stock_doh']
        input_table['min_doh'] = input_table['safety_stock_doh']
        input_table['order_upto_point_doh'] = input_table['lead_time_doh'] + \
                                              input_table['safety_stock_doh'] + \
                                              input_table['review_period']
        main_df = main_df.merge(input_table, on='drug_id', how='left')

        # populating missing rows with defaults
        main_df['lead_time_doh'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'lead_time_doh'].item(), inplace=True)
        main_df['safety_stock_doh'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'safety_stock_doh'].item(), inplace=True)
        main_df['review_period'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'review_period'].item(), inplace=True)
        main_df['reorder_point_doh'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'reorder_point_doh'].item(), inplace=True)
        main_df['min_doh'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'min_doh'].item(), inplace=True)
        main_df['order_upto_point_doh'].fillna(
            input_table.loc[input_table['drug_id'] == 0,
                            'order_upto_point_doh'].item(), inplace=True)

        # calculate ss min max
        main_df['safety_stock'] = (main_df['forecast'] / number_of_day_in_month *
                                   main_df['safety_stock_doh']).round()
        main_df['reorder_point'] = (main_df['forecast'] / number_of_day_in_month *
                                    main_df['reorder_point_doh']).round()
        main_df['order_upto_point'] = (main_df['forecast'] / number_of_day_in_month *
                                       main_df['order_upto_point_doh']).round()

        final_df = pd.concat([final_df,main_df],sort=True)


        columns = ['forecast_date','days_in_this_month','drug_id', 'drug_name', 'composition',
               'drug_sales_quantity','composition_sales_quantity', 'composition_sales_quantity_50%',
               'expected_new_stores', 'avg_drug_sales_quantity','forecast',  'growth_factor','s_op_factor',
                'lead_time_doh','safety_stock_doh','review_period',
               'min_doh', 'order_upto_point_doh', 'reorder_point_doh', 'safety_stock', 'reorder_point','order_upto_point']
        final_df = final_df[columns]



    return final_df,drugs


# Getting Forecast and Drug ids


final_df,drugs=gaid_forecast()

print(final_df['forecast'].sum())

final_df.to_csv(r'D:\goodaid_purc_fcst\sept_forecast_2022.csv')