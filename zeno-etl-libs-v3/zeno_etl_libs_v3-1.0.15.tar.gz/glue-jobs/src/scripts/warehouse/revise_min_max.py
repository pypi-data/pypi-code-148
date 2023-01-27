
import numpy as np
import pandas as pd
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.tz import gettz

from zeno_etl_libs.db.db import MSSql
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.utils.warehouse.data_prep.wh_data_prep import get_launch_stock_per_store
mssql = MSSql(connect_via_tunnel=False)
cnxn = mssql.open_connection()
cursor = cnxn.cursor()

# Reading lead time data
# Last 90 days
# excluding TEPL distributor
# Diff between PO created date and Purchase confirm date

sql_bhw = '''
      SELECT
	*
FROM
	(
	SELECT
		199 as "wh_id",
		i.Barcode as "drug_id" ,
		i.name as "drug_name",
		a.Altercode as "distributor_id",
		a.Name as "distributor_name",
		a2.vdt as "gate-pass-date",
		--sp.Vdt as "purchase_date",
		--sp.RefVdt as "po_opend_date",
		s.PBillDt as "po_created_date",
		s.UpdatedOn as "purchase_confirm_date",
		sp.Qty as "quantity" ,
		DATEDIFF(day, s.PBillDt , a2.vdt) as "lead_time"
	FROM
		SalePurchase2 sp
	left join Item i on
		sp.Itemc = i.code
	left join Salepurchase1 s on
		sp.Vtype = s.Vtyp
		and sp.Vno = s.Vno
		and sp.Vdt = s.Vdt
	left join Acknow a2 on sp.Pbillno =a2.Pbillno 
	left join acm a on
		sp.Acno = a.code
	Where
		sp.Vtype = 'PB'
		and sp.Vdt >= cast(DATEADD(day, -91, GETDATE()) as date)
		and sp.Vdt <= cast(DATEADD(day, -1, GETDATE()) as date)
		and i.Compname NOT IN ('GOODAID', 'PURE & C')
		and i.Barcode NOT LIKE '%[^0-9]%'
		and isnumeric(i.Barcode) = 1
		and a.code NOT IN (59468, 59489)) a
Where
	(a."lead_time">0
		and a."lead_time"<7);
'''

data_bhw = pd.read_sql(sql_bhw, cnxn)

data_bhw[['drug_id']] \
    = data_bhw[['drug_id']] \
    .apply(pd.to_numeric, errors='ignore').astype('Int64')


#TEPL Data

mssql_tepl = MSSql(connect_via_tunnel=False, db='Esdata_TEPL')
cnxn = mssql_tepl.open_connection()
cursor = cnxn.cursor()

sql_tepl = '''                  
   SELECT
	*
FROM
	(
	SELECT
		342 as "wh_id",
		i.Barcode as "drug_id" ,
		i.name as "drug_name",
		a.Altercode as "distributor_id",
		a.Name as "distributor_name",
		a2.vdt as "gate-pass-date",
		--sp.Vdt as "purchase_date",
		--sp.RefVdt as "po_opend_date",
		s.PBillDt as "po_created_date",
		s.UpdatedOn as "purchase_confirm_date",
		sp.Qty as "quantity" ,
		sp.Pbillno ,
		DATEDIFF(day, s.PBillDt , a2.vdt) as "lead_time"
	FROM
		SalePurchase2 sp
	left join Item i on
		sp.Itemc = i.code
	left join Salepurchase1 s on
		sp.Vtype = s.Vtyp
		and sp.Vno = s.Vno
		and sp.Vdt = s.Vdt
	left join Acknow a2 on sp.Pbillno =a2.Pbillno 
	left join acm a on
		sp.Acno = a.code
	Where
		sp.Vtype = 'PB'
		and sp.Vdt >= cast(DATEADD(day, -91, GETDATE()) as date)
		and sp.Vdt <= cast(DATEADD(day, -1, GETDATE()) as date)
		and i.Compname NOT IN ('GOODAID', 'PURE & C')
		and i.Barcode NOT LIKE '%[^0-9]%'
		and isnumeric(i.Barcode) = 1) a
Where
	(a."lead_time">0
		and a."lead_time"<7);
   '''

data_tepl = pd.read_sql(sql_tepl, cnxn)

data_tepl[['drug_id']] \
    = data_tepl[['drug_id']] \
    .apply(pd.to_numeric, errors='ignore').astype('Int64')

data=pd.concat([data_bhw,data_tepl],sort=False,ignore_index=False)
run_date = str(datetime.now(tz=gettz('Asia/Kolkata')))

lead_time_data = 'warehouse_lead_time/lead_time_data_dump_{}.csv'.format(run_date)
s3 = S3()

s3.save_df_to_s3(df=data, file_name=lead_time_data)

data=data.drop(["wh_id"],axis=1)


# Reading Preferred distributor from S3
s3 = S3()
preferred_distributor = pd.read_csv(s3.download_file_from_s3(file_name="warehouse/preferred_distributors.csv"))

df_new = pd.merge(data, preferred_distributor, how='left', on='drug_id')

df_new[["lead_time", "distributor_1"]] = df_new[["lead_time", "distributor_1"]].fillna(0)

df_new[["distributor_1"]] = df_new[["distributor_1"]].astype('int')

# function for weighted mean
def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()

df_new_1 = df_new.groupby(["drug_id", "distributor_id"]).apply(w_avg, 'lead_time', 'quantity').rename(
    'weighted_lead_time').reset_index()
df_std = df_new.groupby(["drug_id", "distributor_id"])[["lead_time"]].std().reset_index()
df_std.rename(columns={'lead_time': 'lead_time_std'}, inplace=True)
df_drug_distributor = pd.merge(df_new_1, df_std, how='left', on=['drug_id', 'distributor_id'])
df_drug_distributor = pd.merge(df_drug_distributor, preferred_distributor, how='left', on=["drug_id"])
df_drug_distributor[["distributor_1", "lead_time_std"]] = df_drug_distributor[
    ["distributor_1", "lead_time_std"]].fillna(0)
df_drug_distributor[["distributor_1"]] = df_drug_distributor[["distributor_1"]].astype('int')
# lead time mean Capping 7 days.
df_drug_distributor['weighted_lead_time'] = np.where(df_drug_distributor['weighted_lead_time'] > 7, 7,
                                                     df_drug_distributor['weighted_lead_time'])
# minimum lead time 2 days
df_drug_distributor['weighted_lead_time'] = np.where(df_drug_distributor['weighted_lead_time'] < 2, 2,
                                                     df_drug_distributor['weighted_lead_time'])
# Lead time Std  capping of 2 days
df_drug_distributor['lead_time_std'] = np.where(df_drug_distributor['lead_time_std'] > 2, 2,
                                                df_drug_distributor['lead_time_std'])
# Minimum Lead time std is 1 day
df_drug_distributor['lead_time_std'] = np.where(df_drug_distributor['lead_time_std'] < 1, 1,
                                                df_drug_distributor['lead_time_std'])
df_drug_distributor[["distributor_id"]] = df_drug_distributor[["distributor_id"]].astype('int')
df_drug_distributor['same_distributor'] = np.where(
    df_drug_distributor['distributor_id'] == df_drug_distributor["distributor_1"], True, False)
preferred_distributor_drug = df_drug_distributor[df_drug_distributor["same_distributor"] == True]
other_distributor_drug = df_drug_distributor[df_drug_distributor["same_distributor"] == False]

# Drugs not in preferred distributor
drugs_not_in_preferred_distributor = df_drug_distributor[
    ~df_drug_distributor['drug_id'].isin(preferred_distributor_drug['drug_id'])]
drugs_not_in_preferred_distributor_mean = drugs_not_in_preferred_distributor.groupby(["drug_id"])[
    ["weighted_lead_time"]].mean().reset_index()
drugs_not_in_preferred_distributor_std = drugs_not_in_preferred_distributor.groupby(["drug_id"])[
    ["weighted_lead_time"]].std().reset_index()
drugs_not_in_preferred_distributor_1 = pd.merge(drugs_not_in_preferred_distributor_mean,
                                                drugs_not_in_preferred_distributor_std, how='left', on='drug_id')
drugs_not_in_preferred_distributor_1 = drugs_not_in_preferred_distributor_1.fillna(0)

# Capping
drugs_not_in_preferred_distributor_1['weighted_lead_time_x'] = np.where(
    drugs_not_in_preferred_distributor_1['weighted_lead_time_x'] > 7, 7,
    drugs_not_in_preferred_distributor_1['weighted_lead_time_x'])
drugs_not_in_preferred_distributor_1['weighted_lead_time_x'] = np.where(
    drugs_not_in_preferred_distributor_1['weighted_lead_time_x'] < 2, 2,
    drugs_not_in_preferred_distributor_1['weighted_lead_time_x'])
drugs_not_in_preferred_distributor_1['weighted_lead_time_y'] = np.where(
    drugs_not_in_preferred_distributor_1['weighted_lead_time_y'] > 2, 2,
    drugs_not_in_preferred_distributor_1['weighted_lead_time_y'])
drugs_not_in_preferred_distributor_1['weighted_lead_time_y'] = np.where(
    drugs_not_in_preferred_distributor_1['weighted_lead_time_y'] < 1, 1,
    drugs_not_in_preferred_distributor_1['weighted_lead_time_y'])
drugs_not_in_preferred_distributor_1.rename(
    columns={'weighted_lead_time_x': 'weighted_lead_time', 'weighted_lead_time_y': 'lead_time_std'}, inplace=True)
drug_in_preferred_distributor = preferred_distributor_drug.drop(
    ['drug_name', 'distributor_id', 'distributor_1', 'distributor_name_1', 'same_distributor'], axis=1)
drug_lead_time_std = pd.concat([drug_in_preferred_distributor, drugs_not_in_preferred_distributor_1], sort=False,
                               ignore_index=True)
weighted_lead_time_mean = drug_lead_time_std[["drug_id", "weighted_lead_time"]]
weighted_lead_time_std = drug_lead_time_std[["drug_id", "lead_time_std"]]
barcoding_lead_time = 2
barcoding_lead_time_std = 0.5

weighted_lead_time_mean['barcoding_lead_time'] = barcoding_lead_time

weighted_lead_time_std['barcoding_lead_time_std'] = barcoding_lead_time_std

weighted_lead_time_mean['weighted_lead_time'] = weighted_lead_time_mean['weighted_lead_time'] + \
                                                weighted_lead_time_mean['barcoding_lead_time']

weighted_lead_time_std['lead_time_std'] = np.sqrt(
    weighted_lead_time_std['lead_time_std'] * weighted_lead_time_std['lead_time_std'] +
    weighted_lead_time_std['barcoding_lead_time_std'] * weighted_lead_time_std['barcoding_lead_time_std'])

weighted_lead_time_mean = weighted_lead_time_mean.drop(['barcoding_lead_time'], axis=1)

weighted_lead_time_std = weighted_lead_time_std.drop(['barcoding_lead_time_std'], axis=1)

#Review Time

s3 = S3()
df_1 = pd.read_csv(s3.download_file_from_s3(file_name="warehouse/review_time_warehouse_distributor.csv"))

# Preferred distributor
df_2 = pd.read_csv(s3.download_file_from_s3(file_name="warehouse/preferred_distributors.csv"))

# If null then take 4 days of review time

df_1 = df_1.fillna(4)

df_1['review_time'] = df_1['review_time'].astype('int')
review_time_new = pd.merge(df_2, df_1, left_on='distributor_1', right_on='distributor_id', how='left')
review_time_new = review_time_new.drop(
    ["drug_name", "distributor_1", "distributor_name_1", "distributor_id", "distributor_name"], axis=1)

service_level=0.95
ordering_freq=1

repln=pd.read_csv("D:\min max reset\wh_forecast_dec.csv")
repln.columns = [c.replace('-', '_') for c in repln.columns]

repln = pd.merge(repln, weighted_lead_time_mean, how='left', on='drug_id')  # merge lead time mean
repln = pd.merge(repln, weighted_lead_time_std, how='left', on='drug_id')  # merge lead time std
repln = pd.merge(repln, review_time_new, how='left', on='drug_id')  # merge review time

repln.rename(columns={'weighted_lead_time': 'lead_time_mean', 'review_time': 'max_review_period'}, inplace=True)
repln['lead_time_mean'] = repln['lead_time_mean'].fillna(4)
repln['lead_time_std'] = repln['lead_time_std'].fillna(2)
repln['max_review_period'] = repln['max_review_period'].fillna(4)

repln['ordering_freq'] = 1
repln['service_level'] = 0.95
repln['z_value'] = 1.64


repln['ss_wo_cap'] = np.round(repln['z_value'] * np.sqrt(
    (
            repln['lead_time_mean'] *
            repln['demand_daily_deviation'] *
            repln['demand_daily_deviation']
    ) +
    (
            repln['lead_time_std'] *
            repln['lead_time_std'] *
            repln['demand_daily'] *
            repln['demand_daily']
    )))

cap_ss_days=15
num_days=30

repln['expected_nso']=0

repln['safety_stock_days'] = np.round(
    repln['ss_wo_cap'] * 30 / repln['fcst'], 1)
# calculate capping days

repln['cap_ss_days'] = np.round(repln['lead_time_mean'] +
                                repln['z_value'] * repln['lead_time_std'] +
                                repln['max_review_period'])
repln['cap_ss_days'] = np.where(repln['cap_ss_days'] > cap_ss_days, cap_ss_days, repln['cap_ss_days'])
# capping SS days based in forecasted sales
repln['safety_stock'] = np.where(repln['safety_stock_days'] > repln['cap_ss_days'],
                                 np.round(repln['cap_ss_days'] * repln['fcst'] / num_days),
                                 repln['ss_wo_cap'])
# setting min SS at 2 days based on forecasted sales
repln['safety_stock'] = np.where(repln['safety_stock_days'] < 2, np.round(2 * repln['fcst'] / num_days),
                                 repln['safety_stock'])
# capping SS days based on last month's sales
repln['safety_stock'] = np.where(repln['safety_stock'] * num_days / repln['last_month_sales'] > cap_ss_days,
                                 np.round(cap_ss_days * repln['last_month_sales'] / num_days),
                                 repln['safety_stock'])
repln['rop_without_nso'] = np.round(repln['safety_stock'] + repln['demand_daily'] * (repln['lead_time_mean'] +
                                                                                     repln['max_review_period']))

#repln['reorder_point'] = repln['rop_without_nso'] + \
                         #np.round((repln['lead_time_mean'] + repln['max_review_period']) *
                                  #repln['expected_nso'] / num_days) * \
                         #repln['launch_stock_per_store']

#repln['reorder_point'] = np.round(repln['reorder_point'])


repln['oup_without_nso'] = np.round(
    repln['rop_without_nso'] +
    repln['demand_daily'] * repln['ordering_freq'])

#repln['order_upto_point'] = np.round(
    #repln['reorder_point'] +
    #repln['demand_daily'] * repln['ordering_freq'])

repln.to_csv(r"D:\min max reset\revised_min_max_dec_1.csv")




