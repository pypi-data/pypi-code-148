# -*- coding: utf-8 -*-
"""

@author: akshay.bhutada@zeno.health

Purpose: To generate goodaid purchase forecast at warehouse for the next  4 months
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

    date=datetime.strptime('2023-01-01', '%Y-%m-%d')

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
                and "store-b2b" ='Store'
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
                and "type" <> 'ethical' and "store-b2b" ='Store'
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
                and "store-b2b" ='Store'
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
                and "store-b2b" ='Store'
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
                    s."company-id" = 6984 and "store-b2b" ='Store'
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
                     ((main_df['drug-maturity'] == 'New') & (main_df['drug_sales_quantity'] >= main_df[
                         'composition_sales_quantity_50%'])),
                     ((main_df['drug-maturity'] == 'New') & (main_df['drug_sales_quantity'] < main_df[
                         'composition_sales_quantity_50%']))]
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
                and date("created-at") < '{this_month_first_date_str}' and "store-b2b" ='Store'
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
                   and "store-id" in {stores_list_to_comp} and "store-b2b" ='Store'
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
                     ((main_df['drug-maturity'] == 'New') & (main_df['last_28_day_sales'] * number_of_day_in_month / 28.0 >= main_df[
                         'composition_sales_quantity_50%'])),
                     ((main_df['drug-maturity'] == 'New') & (main_df['last_28_day_sales'] * number_of_day_in_month / 28.0 < main_df[
                         'composition_sales_quantity_50%']))]
        choice = [main_df['drug_sales_quantity'], main_df['last_28_day_sales'] * number_of_day_in_month / 28.0,
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


final_df.to_csv(r'D:\goodaid_purc_fcst\new_11_jan\Sales_forecast_Jan_feb_march_april_new_1_2022.csv')

logger.info(" Goodaid forecast is generated")

#Getting drug'is

drug_ids=list(drugs['drug_id'])


rs_db = DB()
rs_db.open_connection()


forecast=final_df[['forecast_date','days_in_this_month','drug_id','forecast','safety_stock','reorder_point',
                   'order_upto_point']]

forecast['daily_demand']=forecast['forecast']/forecast['days_in_this_month']


forecast[['safety_stock','reorder_point','order_upto_point','daily_demand']]=\
forecast[['safety_stock','reorder_point','order_upto_point','daily_demand']].astype('int64')

df_all=pd.DataFrame()  # Empty data frame


# creating calendar date for four months for each drug
def gaid_purchase_forecast():

    #first_date_of_month=date(datetime.today().replace(day=1))

    first_date_of_month='2023-01-01'

    calendar_dates = """
        select
                c."date" as "calendar-date" ,
                m."drug_id",
                date(date_trunc('month',c."date"))  as "month-begin-date"
        from
                "prod2-generico"."prod2-generico".calendar c
        cross join (
            select
                d.id as "drug_id"
            from
                    "prod2-generico"."prod2-generico".drugs d
            where
                    d."company-id" = 6984 
         ) m
        where
                date(c."date") <= date('2023-01-01') + interval '4 months'
            and date(c."date")>= '2023-01-01'
    """.format(first_date=first_date_of_month)


    calendar_date = rs_db.get_df(calendar_dates)

    calendar_date['drug_id'] = pd.to_numeric(calendar_date['drug_id'])

    calendar_date = calendar_date.astype(int, errors='ignore')

    moq='''
    select
        pd."drug-id" as "drug_id",
        pd.moq
    from
        "prod2-generico"."prod2-generico"."preferred-distributor" pd
    left join "prod2-generico"."prod2-generico".drugs d on
        pd."drug-id" = d.id
    where
        d."company-id" = 6984
    '''

    moq=pd.read_csv("D:\goodaid_purc_fcst\gaid_moq.csv")

    #moq = rs_db.get_df(moq)

    moq=moq.fillna(1)  #Fill with 1 where moq is not available

    moq['drug_id'] = pd.to_numeric(moq['drug_id'])

    moq = moq.astype(int, errors='ignore')

    calendar_date = pd.merge(calendar_date,moq, how='left', left_on=[ 'drug_id'],
                        right_on=[ 'drug_id'])  # Merging moq with calendar dates

    calendar_date['moq']=calendar_date['moq'].fillna(1)

    # Inventory @ First date of month along with MOQ

    # inventory = """
    # select
    #     date("snapshot-date") as "snapshot_date",
    #     wis."drug-id" as "drug_id",
    #     SUM(wis."balance-quantity" + wis."locked-quantity") as "total_inv_quantity"
    # from
    #     "prod2-generico"."prod2-generico"."wh-inventory-ss" wis
    # left join "prod2-generico"."prod2-generico".drugs d on
    #     wis."drug-id" = d.id
    # where
    #     date(wis."snapshot-date")= '{first_date}'
    #     and wis."wh-id" in (199, 343)
    #     and d."company-id" = 6984
    # group by
    #     date("snapshot-date"),
    #     wis."drug-id"
    #     """.format(first_date=first_date_of_month)

    q1='''
    select
        a."drug_id",
        '2023-01-01' as "snapshot_date",
        SUM(a."bhw_barcoded_quantity" + a."bhw_non_barcoded_quantity" + a."ga_barcoded_quantity"
    + a."ga_non_barcoded_quantity"+coalesce (b."Forward-in-transit-inventory",0)) as "total_inv_quantity"
    from
    (
        select
            b.Barcode as drug_id,
            SUM(case
            when a.Vno >= 0 and a.warehouseid = 199 then coalesce(a.bqty,
            0)
            else 0
        end ) as bhw_barcoded_quantity,
            SUM(case
            when a.Vno <0 and a.warehouseid = 199 then coalesce(a.tqty,
            0)
            else 0
        end ) as bhw_non_barcoded_quantity,
            SUM(case
            when a.Vno >= 0 and a.warehouseid = 343 then coalesce(a.bqty,
            0)
            else 0
        end ) as ga_barcoded_quantity,
            SUM(case
            when a.Vno <0 and a.warehouseid = 343 then coalesce(a.tqty,
            0)
            else 0
        end ) as ga_non_barcoded_quantity
        from
            "prod2-generico"."public"."fifo-gaid_forecast-2022-12-31" a
        left join "prod2-generico"."prod2-generico".item b on
            a.itemc = b.code
        left join "prod2-generico"."prod2-generico".drugs d2 on
            cast(b.barcode as int) = d2.id
        where
            b.code > 0
            and a.Psrlno in (
            select
                Psrlno
            from
                "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31")
            and b.Barcode not like '%[^0-9]%'
            and (b.compname in ('GOODAID', 'PURE & C')
                or d2."company-id" = 6984)
            and REGEXP_COUNT(b.barcode ,
            '^[0-9]+$') > 0
        group by
            b.barcode) a
    left join (
    select
        convert(int,i.Barcode) as "drug_id" ,
        coalesce (SUM(sp.qty),
        0) as "Forward-in-transit-inventory"
    from
        "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31" sp
    left join "prod2-generico"."prod2-generico".item i on
        sp.Itemc = i.code
    left join "prod2-generico"."prod2-generico".acm a on
        sp.Acno = a.code
    right join "prod2-generico"."prod2-generico".drugs d on i.barcode =d.id
    where
        sp.Vtype = 'BT'
        and sp.warehouseid = 343 and d."company-id" =6984
        and
        (concat('U02BT', concat( '-', concat('22', concat('-', sp.Vno)))))
        not in (
        select
            sp1.pbillno
        from
            "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31" sp1
        left join "prod2-generico"."prod2-generico".acm a2 on
            sp1.Acno = a2.code
        where
            sp1.Vtype = 'BR'
            and sp1.warehouseid = 199
            and a2.code = 59442)
        and
            (concat('UO2BT', concat( '-', concat('22', concat('-', sp.Vno)))))
        not in (
        select
            sp1.pbillno
        from
            "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31" sp1
        left join "prod2-generico"."prod2-generico".acm a2 on
            sp1.Acno = a2.code
        where
            sp1.Vtype = 'BR'
            and sp1.warehouseid = 199
            and a2.code = 59442)
    group by
        convert(int,i.Barcode)) b on a."drug_id"=b."drug_id"
    group by 1,2
    '''


    wh_inventory = rs_db.get_df(q1)

    wh_inventory['drug_id'] = pd.to_numeric(wh_inventory['drug_id'])

    wh_inventory = wh_inventory.astype(int, errors='ignore')

    wh_inventory.snapshot_date = pd.to_datetime(wh_inventory.snapshot_date).dt.date

    wh_inventory['total_inv_quantity']=wh_inventory['total_inv_quantity'].astype('int')

    # Merging the calendar date with wh_inventory

    df_merge = pd.merge(calendar_date, wh_inventory, how='left', left_on=['calendar-date', 'drug_id'],
                        right_on=['snapshot_date', 'drug_id'])

    df_merge = df_merge.rename(columns={'snapshot_date': 'reset_date'})

    df_merge = df_merge.rename(columns={'calendar-date': 'calendar_date'})

    df_merge = df_merge.rename(columns={'month-begin-date': 'month_begin_date'})

    # Merging forecast

    forecast.forecast_date = pd.to_datetime(forecast.forecast_date).dt.date

    df_merge.month_begin_date = pd.to_datetime(df_merge.month_begin_date).dt.date

    df_merge_new = pd.merge(df_merge, forecast, how='left', left_on=['month_begin_date', 'drug_id'],
                            right_on=['forecast_date', 'drug_id'])


    # Expected purchase date and quantity of open po's

    expected_purchase = """
      select
             (case when date(s.vdt +60)<='2023-01-01' then 
            date(s.vdt+63) else date(s.vdt+60) end ) as "expected_purchase_date",
            i.barcode as "drug_id" ,
            s.flag ,
            SUM(s.qty) as "purchase_qty"
        from
            "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31" s
        left join "prod2-generico"."prod2-generico".item i on
            s.itemc = i.code
        left join "prod2-generico"."prod2-generico".drugs d on
            i.barcode = d.id
        where
            d."company-id" = 6984
             and s.flag != '*'
            and s.vtype = 'PO'
            and s.vdt >= '2023-01-01'-60 and s.vdt<='2023-01-01'
            and s.chlnqty =0
        group by 1,2,3
    """.format(first_date=first_date_of_month)

    purchase_qty = rs_db.get_df(expected_purchase)

    purchase_qty['drug_id'] = pd.to_numeric(purchase_qty['drug_id'])

    purchase_qty = purchase_qty.astype(int, errors='ignore')

    purchase_qty.expected_purchase_date = pd.to_datetime(purchase_qty.expected_purchase_date).dt.date

    purchase_qty[['drug_id', 'purchase_qty']] = purchase_qty[['drug_id', 'purchase_qty']].astype('int64')

    # open Po as on First date on month

    open_po = """
     select
        '2023-01-01' as "po_date",
        i.barcode as "drug_id" ,
        SUM(s.qty) as "po_qty"
    from
         "prod2-generico"."public"."salepurchase2-gaid_forecast-2022-12-31" s
    left join "prod2-generico"."prod2-generico".item i on
        s.itemc = i.code
    left join "prod2-generico"."prod2-generico".drugs d on
        i.barcode = d.id
    where
        d."company-id" = 6984
        and s.flag != '*'
        and s.vtype = 'PO'
        and s.vdt >= '2023-01-01'-60  and s.vdt<='2023-01-01'
        and  s.chlnqty =0
    group by 1,2 
    """.format(first_date=first_date_of_month)

    po_qty = rs_db.get_df(open_po)

    po_qty['drug_id'] = pd.to_numeric(po_qty['drug_id'])

    po_qty = po_qty.astype(int, errors='ignore')

    po_qty.po_date = pd.to_datetime(po_qty.po_date).dt.date

    df_merge_new.calendar_date = pd.to_datetime(df_merge_new.calendar_date).dt.date

    df_merge_new_1 = pd.merge(df_merge_new, purchase_qty, how='left', left_on=['drug_id', 'calendar_date'],
                              right_on=['drug_id', 'expected_purchase_date'])

    po_qty[['drug_id', 'po_qty']] = po_qty[['drug_id', 'po_qty']].astype('int64')

    df_merge_new_2 = pd.merge(df_merge_new_1, po_qty, how='left', left_on=['drug_id', 'calendar_date'],
                              right_on=['drug_id', 'po_date'])

    df_merge_new_2['total_qty_inv_po'] = 0

    df_merge_new_2[['po_qty', 'purchase_qty', 'total_inv_quantity']] = \
        df_merge_new_2[['po_qty', 'purchase_qty', 'total_inv_quantity']].fillna(0)  #Fillna with zero

    # Total inv po qty= total inv quantity+po qty available at First of month

    df_merge_new_2['total_qty_inv_po'] = df_merge_new_2['total_inv_quantity'] + df_merge_new_2['po_qty']

    # Review will be at every 14 days

    df_merge_3=df_merge_new_2


    for k in drug_ids:

        logger.info("Drug is =" + str(k))

        df_merge_new_2 = df_merge_3[df_merge_3['drug_id'] == k].reset_index().drop(['index'], axis=1)

        for i in range(0, len(df_merge_new_2), 14):
            df_merge_new_2['reset_date'].iloc[i] = df_merge_new_2['calendar_date'].iloc[i]

        df_merge_new_2 = df_merge_new_2.drop(len(df_merge_new_2)-1, axis=0)

        df_merge_new_2['pending_po_qty'] = 0

        df_merge_new_2['pending_po_qty'].iloc[0] = df_merge_new_2['po_qty'].iloc[0]

        df_merge_new_2['moq'] = df_merge_new_2['moq'].fillna(1)

        moq = df_merge_new_2['moq'].iloc[0]

        df_merge_new_2['new_po_qty'] = 0

        for j in range(0, len(df_merge_new_2), 14):

            # j=0 is first date of month where review is done

            if j > 0:
                for i in range(j - 14, j):

                    df_merge_new_2['total_inv_quantity'].iloc[i + 1] = \
                        df_merge_new_2['total_inv_quantity'].iloc[i] + df_merge_new_2['purchase_qty'].iloc[i] \
                        - df_merge_new_2['daily_demand'].iloc[i]

                    if i == 0:

                        # logic for first days

                        df_merge_new_2['pending_po_qty'].iloc[i + 1] = df_merge_new_2['pending_po_qty'].iloc[i]

                        df_merge_new_2['total_qty_inv_po'].iloc[i + 1] = df_merge_new_2['total_qty_inv_po'].iloc[i] \
                                                                         - df_merge_new_2['daily_demand'].iloc[i]
                    else:

                        # Logic for rest of the days

                        df_merge_new_2['pending_po_qty'].iloc[i + 1] = df_merge_new_2['pending_po_qty'].iloc[i] \
                                                                       + df_merge_new_2['po_qty'].iloc[i] - \
                                                                       df_merge_new_2['purchase_qty'].iloc[i]

                        df_merge_new_2['total_qty_inv_po'].iloc[i + 1] = df_merge_new_2['pending_po_qty'].iloc[i] \
                                                                         + df_merge_new_2['total_inv_quantity'].iloc[i]

            if df_merge_new_2['total_inv_quantity'].iloc[j] < df_merge_new_2['reorder_point'].iloc[j]:
                if df_merge_new_2['total_qty_inv_po'].iloc[j] < df_merge_new_2['reorder_point'].iloc[j]:
                    if j == 0:
                        # For first date
                        # Condition for MOQ

                        if int(df_merge_new_2['order_upto_point'].iloc[j] - df_merge_new_2['total_qty_inv_po'].iloc[
                            j]) < moq:

                            df_merge_new_2['new_po_qty'].iloc[j] = math.ceil((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                              df_merge_new_2['total_qty_inv_po'].iloc[
                                                                                  j]) / moq) * moq

                            df_merge_new_2['po_qty'].iloc[j] = math.ceil((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                          df_merge_new_2['total_qty_inv_po'].iloc[
                                                                              j]) / moq) * moq + \
                                                               df_merge_new_2['po_qty'].iloc[0]

                        else:

                            df_merge_new_2['new_po_qty'].iloc[j] = round((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                          df_merge_new_2['total_qty_inv_po'].iloc[
                                                                              j]) / moq) * moq

                            df_merge_new_2['po_qty'].iloc[j] = round((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                          df_merge_new_2['total_qty_inv_po'].iloc[\
                                                                              j]) / moq) * moq+df_merge_new_2['po_qty'].iloc[0]

                        df_merge_new_2['pending_po_qty'].iloc[j] = df_merge_new_2['po_qty'].iloc[j]

                        df_merge_new_2['total_qty_inv_po'].iloc[j] = df_merge_new_2['pending_po_qty'].iloc[j] \
                                                                     + df_merge_new_2['total_inv_quantity'].iloc[j]

                    else:

                        # Condition for MOQ
                        if int(df_merge_new_2['order_upto_point'].iloc[j] - df_merge_new_2['total_qty_inv_po'].iloc[
                            j]) < moq:
                            df_merge_new_2['po_qty'].iloc[j] = math.ceil((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                          df_merge_new_2['total_qty_inv_po'].iloc[
                                                                              j]) / moq) * moq
                        else:
                            df_merge_new_2['po_qty'].iloc[j] = round((df_merge_new_2['order_upto_point'].iloc[j] - \
                                                                      df_merge_new_2['total_qty_inv_po'].iloc[
                                                                          j]) / moq) * moq

                    if (j + 60) < len(df_merge_new_2):

                        if j == 0:
                            df_merge_new_2['purchase_qty'].iloc[j + 60] = df_merge_new_2['new_po_qty'].iloc[j]
                        else:
                            df_merge_new_2['purchase_qty'].iloc[j + 60] = df_merge_new_2['po_qty'].iloc[j]

        # Simulation For remaining days

        for m in range(j, len(df_merge_new_2) - 1):
            df_merge_new_2['total_inv_quantity'].iloc[m + 1] = \
                df_merge_new_2['total_inv_quantity'].iloc[m] + df_merge_new_2['purchase_qty'].iloc[m] \
                - df_merge_new_2['daily_demand'].iloc[m]

            df_merge_new_2['pending_po_qty'].iloc[m + 1] = df_merge_new_2['pending_po_qty'].iloc[m] \
                                                           + df_merge_new_2['po_qty'].iloc[m] - \
                                                           df_merge_new_2['purchase_qty'].iloc[m]

            df_merge_new_2['total_qty_inv_po'].iloc[m + 1] = df_merge_new_2['pending_po_qty'].iloc[m] \
                                                             + df_merge_new_2['total_inv_quantity'].iloc[m]

        df_all = df_all.append(df_merge_new_2)   #Appending for all the drugs in df_all

    #Lastest Purchase Rate

    latest_purchase_rate = """
    select 
    a."drug-id" as "drug_id",
    a."purchase-rate" 
    from (
    select
        i2."drug-id" ,
        i2."purchase-rate" ,
        row_number() over (partition by i2."drug-id" 
            order by
                i2."created-at" desc) as "row"
    from
        "prod2-generico"."prod2-generico"."inventory-1" i2 
    left join "prod2-generico"."prod2-generico".drugs d on i2."drug-id"=d.id
    where
        i2."franchisee-inventory"=0 and d."company-id" =6984
    ) a 
    where a."row"=1 
    """
    latest_purchase_rate=rs_db.get_df(latest_purchase_rate)

    logger.info("data pulled from RS")

    latest_purchase_rate['drug_id'] = pd.to_numeric(latest_purchase_rate['drug_id'])

    df_all=pd.merge(df_all,latest_purchase_rate,how='left',on='drug_id')

    actual_po_qty=po_qty

    actual_po_qty=actual_po_qty.rename(columns={'po_date':'open_po_date','po_qty':
                                            'open_po_qty'})


    df_all=pd.merge(df_all,actual_po_qty,how='left',left_on=['drug_id','calendar_date'],
                   right_on=['drug_id','open_po_date'])

    df_all['open_po_qty']=df_all['open_po_qty'].fillna(0)

    df_all['actual_po_qty']=df_all['po_qty']-df_all['open_po_qty']


    df_all['actual_po_value']=df_all['actual_po_qty']*(df_all['purchase-rate'].astype('float'))

    df_all['purchase_value']=df_all['purchase_qty']*(df_all['purchase-rate'].astype('float'))

    df_all.to_csv(r"D:\goodaid_purc_fcst\new_11_jan\purchase_forecast_new_updated.csv")

    return df_all












