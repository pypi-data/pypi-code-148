


import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from dateutil.tz import gettz
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper


env = "dev"

os.environ['env'] = env

logger = get_logger()
logger.info("Scripts begins. Env = " + env)

rs_db = DB()

rs_db.open_connection()

s3=S3()


# =============================================================================
# Part-1 : Date Level Supply Chain Metrics
# =============================================================================


schema = 'prod2-generico'
table_name = 'supplychain-ops-metrics-date'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

date1= (datetime.today() + relativedelta(months=-1)).replace(day=1).strftime('%Y-%m-%d')
date2= (datetime.today() + relativedelta(days=-1)).strftime('%Y-%m-%d')


sm = """
      
select
    sm.id as "store-id"
from
    "prod2-generico"."stores-master" sm
inner join "prod2-generico"."stores" s on
    s.id = sm.id
where
    date(sm."opened-at") != '0101-01-01'
    and s."is-active" = 1
group by
    sm.id
union 
select 199
union 
select 343
union
select 342
"""
sm_data = rs_db.get_df(sm)
sm_data.columns = [c.replace('-', '_') for c in sm_data.columns]

sm_data['join']='A'

# =============================================================================
# Date range explode
# =============================================================================
d_date = pd.DataFrame({'join':['A']})
#d_date['join']='A'
d_date['start_date']= date1
d_date['end_date']= date2
d_date['date'] = [pd.date_range(s, e, freq='d') for s, e in
                         zip(pd.to_datetime(d_date['start_date']),
                             pd.to_datetime(d_date['end_date']))]
#d_date = d_date.explode('date')
d_date = pd.DataFrame({'date': np.concatenate(d_date.date.values)})
d_date['join']='A'

#d_date.drop(['start_date','end_date'],axis=1,inplace=True)

d_date['date'] = d_date['date'].astype('str')

m_data = pd.merge(left=sm_data,right=d_date,on=['join'],how='inner')
m_data.drop('join',axis=1,inplace=True)

as_dc_wh=f'''
select 
a."store-id",
a."created-at" as "date",
a."drug-type-group",
sum("wh-quantity") as "wh-quantity",
sum("wh-otif-quantity") as "wh-otif-quantity",
sum("wh-otif-required-quantity") as "wh-otif-required-quantity",
sum("wh-required-quantity") as "wh-required-quantity",
sum("dc-quantity") as "dc-quantity",
sum("dc-otif-quantity") as "dc-otif-quantity",
sum("dc-otif-required-quantity") as "dc-otif-required-quantity",
sum("dc-required-quantity") as "dc-required-quantity"
-- ("wh-otif-quantity"-"wh-otif-required-quantity")/"wh-quantity" - WH-OTIF
from (
select 
a."store-id",
a."created-at",
a."drug-type-group",
CASE WHEN a."distributor" =  'wh' THEN (a."quantity") END as "wh-quantity",
CASE WHEN a."distributor" =  'wh' THEN (case when "fullfilment on delivery" = 'ontime' then a."quantity" end) END as "wh-otif-quantity",
CASE WHEN a."distributor" =  'wh' THEN (case when "fullfilment on delivery" = 'ontime' then a."required-quantity" end) END as "wh-otif-required-quantity",
CASE WHEN a."distributor" =  'wh' THEN (a."required-quantity") END as "wh-required-quantity",
CASE WHEN a."distributor" !=  'dc' THEN (a."quantity") END as "dc-quantity",
CASE WHEN a."distributor" !=  'dc' THEN (case when "fullfilment on delivery" = 'ontime' then a."quantity" end) END as "dc-otif-quantity",
CASE WHEN a."distributor" !=  'dc' THEN (case when "fullfilment on delivery" = 'ontime' then a."required-quantity" end) END as "dc-otif-required-quantity",
CASE WHEN a."distributor" !=  'dc' THEN (a."required-quantity") END as "dc-required-quantity"
from (
select
   a."store-id",
   case when s."franchisee-id" != 1 then date(a."saved-at")
   else date(a."created-at") end as "created-at",
   (case
      when a."recieved-distributor-id" = 8105 then 'wh'
      else 'dc'
   end) as "distributor",
         case
         when sbol."status-log" in ('presaved,lost') then 'FOFO-partner-rejected'
         else a.status
      end as "status",
   case 
   when (date(a."store-delivered-at") = '0101-01-01' or a."store-delivered-at" is null) then 'Pending'
   when s."franchisee-id" != 1 and dateadd(hour, tat."delivery-time",(dateadd(day, tat."delivery-date", date(a."saved-at"))))>= a."store-delivered-at" then 'ontime'
   when s."franchisee-id" = 1 and dateadd(hour, tat."delivery-time",(dateadd(day, tat."delivery-date", date(a."created-at"))))>= a."store-delivered-at" then 'ontime'
   else 'delayed' 
   end as  "fullfilment on delivery",
   a."status"                            AS "sb-status",
       a."requested-quantity"                AS "requested-quantity",
       a."quantity"                          AS "quantity",
       a."required-quantity"                 AS "required-quantity",
         (case when a."type"='ethical' then 'ethical'
      when a."type" ='generic' then 'generic'
      else 'other' end ) as "drug-type-group"
from
   "prod2-generico"."as-ms" a
left join "prod2-generico".stores s 
               on
   s.id = a."store-id"
 left join( select
            sbol."short-book-id" ,
            listagg(distinct sbol.status,',') within group (order by sbol.id) as "status-log"
         from
            "prod2-generico"."short-book-order-logs" sbol
         left join "prod2-generico"."prod2-generico"."short-book-1" sb 
         on sbol."short-book-id" = sb.id 
         where Date(sb."created-at") >= date(date_trunc('month', current_date) - interval '2 month')
         group by
            sbol."short-book-id") sbol 
      on a.id = sbol."short-book-id"
left join "prod2-generico"."tat-sla" tat on
   (case
      when s."franchisee-id" = 1
         and extract('hour'
      from
         a."created-at")<14 then 1
         when s."franchisee-id" != 1
         and extract('hour'
      from
         a."saved-at")<14 then 1
         when s."franchisee-id" = 1
         and (extract('hour'
      from
         a."created-at")>= 14
         and extract('hour'
      from
         a."created-at")<23) then 2
         when s."franchisee-id" != 1
         and (extract('hour'
      from
         a."saved-at")>= 14
         and extract('hour'
      from
         a."saved-at")<23) then 2
         else 3
      end) = tat.round
   and
   (case
      when a."recieved-distributor-id" = 8105 then 'wh'
      else 'dc'
   end) = tat."distributor-type"
   and
        'as_ms' = tat."as-ms-pr-flag"
   and datepart(weekday,
   a."created-at") = tat.day
   and a."store-id" = tat."store-id"
where
   Date(a."created-at") >= '{date1}' 
   and Date(a."created-at") <= '{date2}'
   and  ((a."as-ms" ='AS' and s."franchisee-id" =1) or (a."as-ms"='MS' and a."patient-id"=4490
and s."franchisee-id"!=1))
   )a
where a."status" not in ('presaved','FOFO-partner-rejected'))a
where a."created-at" is not null
group by 
a."store-id",
a."created-at",
a."drug-type-group"
'''



as_dc_wh = rs_db.get_df(as_dc_wh)
as_dc_wh.columns = [c.replace('-', '_') for c in as_dc_wh.columns]
as_dc_wh['date'] =  as_dc_wh['date'].astype('str')


as_dc_wh_pivot = as_dc_wh.pivot_table(index=['store_id', 'date'], columns='drug_type_group',
                                      values=["wh_quantity","wh_otif_quantity",
                                              "wh_required_quantity","dc_quantity",
                                              "dc_otif_quantity","dc_required_quantity",
                                              "wh_otif_required_quantity","dc_otif_required_quantity"])


as_dc_wh_pivot.columns = ['_'.join(col).strip() for col in as_dc_wh_pivot.columns.values]



as_dc_wh_pivot.reset_index(inplace=True)



as_dc_wh_pivot=as_dc_wh_pivot.fillna(0)

pr_ff=f'''
select 
a."store-id",
a."created-at" as "date",
a."drug-type-group",
sum(coalesce("wh-quantity",0)) as "pr-wh-quantity",
sum(coalesce("wh-otif-quantity",0)) as "pr-wh-otif-quantity",
sum(coalesce("wh-required-quantity",0)) as "pr-wh-required-quantity",
sum(coalesce("dc-quantity",0)) as "pr-dc-quantity",
sum(coalesce("dc-otif-quantity",0)) as "pr-dc-otif-quantity",
sum(coalesce("dc-required-quantity",0)) as "pr-dc-required-quantity"
-- (1 - (sum(a."required-quantity")/sum(a."quantity"))) as "in_full_percentage"
from (select a."store-id",
a."created-at",
a."drug-type-group",
case when a."distributor" = 'wh' then (a."quantity") end as "wh-quantity",
case when a."distributor" = 'wh' then (case when "fullfilment on delivery" = 'ontime' then a."quantity" end) end as "wh-otif-quantity",
case when a."distributor" = 'wh' then (a."required-quantity") end  as "wh-required-quantity",
case when a."distributor" = 'dc' then (a."quantity") end as "dc-quantity",
case when a."distributor" = 'dc' then (case when "fullfilment on delivery" = 'ontime' then a."quantity" end) end as "dc-otif-quantity",
case when a."distributor" = 'dc' then (a."required-quantity") end  as "dc-required-quantity"
from (select 
	a."store-id",
	case when s."franchisee-id" != 1 then date(sb3."saved-at")
	else date(a."created-at") end as "created-at",
	(case
		when a."ff-distributor"  = 8105 then 'wh'
		else 'dc'
	end) as "distributor",	    
		case 
		when (date(a."store-delivered-at") = '0101-01-01' or a."store-delivered-at" is null) then 'Pending'
		when s."franchisee-id" != 1 and dateadd(hour, tat."delivery-time",(dateadd(day, tat."delivery-date", date(sb3."saved-at"))))>= a."store-delivered-at" then 'ontime'
		when s."franchisee-id" = 1 and dateadd(hour, tat."delivery-time",(dateadd(day, tat."delivery-date", date(a."created-at"))))>= a."store-delivered-at" then 'ontime'
		else 'delayed' 
		end as  "fullfilment on delivery",
	-- -- Completed Issue -- -- 	
    case when DATE(a."invoiced-at") is null
            AND DATE(a."completed-at") is null
            AND date_part(hour, a."created-at") < '14'
            AND DATEDIFF(day, a."created-at", a."completed-at") = 0
            AND (date_part(hour, a."completed-at")) <= '21' then 
        'completed-early'
        when DATE(a."invoiced-at") is null
                AND DATE(a."completed-at") is not null
                AND (trim(' ' FROM to_char(a."created-at", 'Day'))) NOT IN ('Sunday' , 'Saturday')
                AND date_part(hour, a."created-at") > '23'
                AND DATEDIFF(day, a."created-at", a."completed-at") = 0 then
            'completed-early'
            when DATE(a."invoiced-at") is null
                    AND DATE(a."completed-at") is not null
                    AND (trim(' ' FROM to_char(a."created-at", 'Day'))) NOT IN ('Sunday' , 'Saturday')
                    AND date_part(hour, a."created-at") > '23'
                    AND DATEDIFF(day, a."created-at", a."completed-at") = 1
                    AND (date_part(hour, a."completed-at")) <= '21' then
                'completed-early'
                when DATE(a."invoiced-at") is null
                        AND DATE(a."completed-at") is not null
                        AND date_part(hour, a."created-at") >= '14'
                        AND DATEDIFF(day, a."created-at", a."completed-at") = 0 then
                    'completed-early'
                    when DATE(a."invoiced-at") is null
                            AND DATE(a."completed-at") is not null
                            AND date_part(hour, a."created-at") >= '14'
                            AND DATEDIFF(day, a."created-at", a."completed-at") = 1
                            AND (date_part(hour, a."completed-at")) <= '16' then 
                        'completed-early'
                        when DATE(a."invoiced-at") is null
                                AND DATE(a."completed-at") is not null
                                AND (trim(' ' FROM to_char(a."created-at", 'Day'))) = 'Saturday'
                                AND DATEDIFF(day, a."created-at", a."completed-at") = 0
                                AND date_part(hour, a."created-at") < '14'
                                AND (date_part(hour, a."completed-at")) <= '21' then
                            'completed-early'
                            when DATE(a."invoiced-at") is null
                                    AND DATE(a."completed-at") is not null
                                    AND (trim(' ' FROM to_char(a."created-at", 'Day'))) = 'Saturday'
                                    AND date_part(hour, a."created-at") >= '14'
                                    AND DATEDIFF(day, a."created-at", a."completed-at") <= 1 then
                                'completed-early'
                                when DATE(a."invoiced-at") is null
                                        AND DATE(a."completed-at") is not null
                                        AND (trim(' ' FROM to_char(a."created-at", 'Day'))) = 'Saturday'
                                        AND date_part(hour, a."created-at") >= '14'
                                        AND DATEDIFF(day, a."created-at", a."completed-at") = 2
                                        AND (date_part(hour, a."completed-at")) <= '16' then
                                    'completed-early'
                                    when DATE(a."invoiced-at") is null
                                            AND DATE(a."completed-at") is not null
                                            AND (trim(' ' FROM to_char(a."created-at", 'Day'))) = 'Sunday'
                                            AND DATEDIFF(day, a."completed-at", a."created-at") <= 1 then
                                        'completed-early'
                                        when DATE(a."invoiced-at") is null
                                                AND DATE(a."completed-at") is not null
                                                AND DATEDIFF(day, a."created-at", a."completed-at") = 2
                                                AND (date_part(hour, a."completed-at")) <= '16' then
                                            'completed-early'
                                                when a."sb-status" = 'completed' and 
                                                (a."store-delivered-at" is null or DATE(a."store-delivered-at")='0101-01-01')
                                                then 'competed-without-delivery'
                                                else
                                            'no issue' end AS "completed issues",
	a."pso-requested-quantity" as "requested-quantity",
	a."quantity" as "quantity",
	a."required-quantity" as "required-quantity",
	case
			when sbol."status-log" in ('presaved,lost') then 'FOFO-partner-rejected'
		else a."sb-status"
	end as "status",
	(case when a."type"='ethical' then 'ethical'
	when a."type" ='generic' then 'generic'
	else 'other' end ) as "drug-type-group"
from
	"prod2-generico"."prod2-generico"."patient-requests-metadata" a
left join "prod2-generico"."prod2-generico".stores s
      on
	s.id = a."store-id"
left join "prod2-generico"."prod2-generico"."short-book-1" sb3 
on a."sb-id" = sb3.id 
left join(
	select
					sbol."short-book-id" ,
					listagg(distinct sbol.status,',') within group (order by sbol.id) as "status-log"
	from
					"prod2-generico"."short-book-order-logs" sbol
	left join "prod2-generico"."prod2-generico"."short-book-1" sb 
				on
		sbol."short-book-id" = sb.id
	where
		Date(sb."created-at") >= date(date_trunc('month', current_date) - interval '2 month')
	group by
					sbol."short-book-id") sbol 
			on
	a."sb-id" = sbol."short-book-id"
left join "prod2-generico"."tat-sla" tat on
	(case
		when s."franchisee-id" = 1
			and extract('hour'
		from
			a."created-at")<14 then 1
			when s."franchisee-id" != 1
			and extract('hour'
		from
			sb3."saved-at")<14 then 1
			when s."franchisee-id" = 1
			and (extract('hour'
		from
			a."created-at")>= 14
			and extract('hour'
		from
			a."created-at")<23) then 2
			when s."franchisee-id" != 1
			and (extract('hour'
		from
			sb3."saved-at")>= 14
			and extract('hour'
		from
			sb3."saved-at")<23) then 2
			else 3
		end) = tat.round
	and
	(case
		when a."ff-distributor"  = 8105 then 'wh'
		else 'dc'
	end) = tat."distributor-type"
	and
        'pr' = tat."as-ms-pr-flag"
	and datepart(weekday,
	a."created-at") = tat.day
	and a."store-id" = tat."store-id"
where
	DATE(a."created-at") >= '{date1}'
	and DATE(a."created-at") <= '{date2}'
	-- and s.id  = 2
	and (a."quantity" > 0
		or a."completion-type" = 'stock-transfer')
	and a."sb-status" not in ('deleted', 'presaved'))a 
where 
a."status" not in ('presaved','FOFO-partner-rejected')
and a."completed issues" = 'no issue')a
	group by 
a."store-id",
a."created-at",
a."drug-type-group"
'''


pr_ff = rs_db.get_df(pr_ff)
pr_ff.columns = [c.replace('-', '_') for c in pr_ff.columns]
pr_ff['date'] =  pr_ff['date'].astype('str')


pr_ff_pivot = pr_ff.pivot_table(index=['store_id', 'date'], columns='drug_type_group',
                                      values=['pr_wh_quantity',
       'pr_wh_otif_quantity', 'pr_wh_required_quantity', 'pr_dc_quantity',
       'pr_dc_otif_quantity', 'pr_dc_required_quantity' ])


pr_ff_pivot.columns = ['_'.join(col).strip() for col in pr_ff_pivot.columns.values]

pr_ff_pivot.reset_index(inplace=True)


pr_ff_pivot=pr_ff_pivot.fillna(0)



#pr class wise demand


pr_class_wise_demand=f'''
 select a."date",
a."store-id",
a."bucket",
SUM(a."net-quantity") as "class-wise-demand-net-quantity",
SUM(a."pr-net-quantity") as "class-wise-demand-pr-net-quantity",
SUM(a."revenue") as "class-wise-demand-revenue",
SUM(a."pr-revenue") as "class-wise-revenue-pr-revenue"
FROM (select
	date(s."created-at") as "date" ,
	s."store-id" ,
	b."bucket",
	SUM(s."net-quantity") as "net-quantity",
	SUM(case when s."pr-flag" is true then s."net-quantity" 
	else 0 end ) as "pr-net-quantity",
	SUM(s."revenue-value") as "revenue",
	SUM(case when s."pr-flag" is true then s."revenue-value" 
	else 0 end ) as "pr-revenue"
from
	"prod2-generico"."prod2-generico".sales s
left join (select
        iss."store-id" ,
        iss."drug-id" ,
        (case when iss."bucket" in ('AW','AX','AY','AZ') then 'A'
        when iss."bucket" in ('BW','BX','BY','BZ') then 'B'
        when iss."bucket" in ('CW','CX','CY','CZ') then 'C'
        end ) as "bucket"
    from
        "prod2-generico"."ipc2-segmentation" iss
    inner join (
        select
            "store-id" ,
            max("reset-date") as latest_reset
        from
            "prod2-generico"."ipc2-segmentation" iss
        group by
            "store-id" 
    ) as sq
    on
        iss."store-id" = sq."store-id"
        and iss."reset-date" = sq.latest_reset ) b on s."store-id" =b."store-id"
        and s."drug-id" =b."drug-id"
where
	s."store-b2b" = 'Store'
	and date(s."created-at")>= '{date1}'
	and date(s."created-at")<= '{date2}' 
group by
	1,
	2,3
union
select
	"attributed-loss-date" as "date",
	cpr."store-id" ,
	b."bucket",
	SUM("loss-quantity") as "losss-quantity",
	0 as "loss-quantity",
	SUM(cpr."final-lost-sales") as "lost-sales",
	0
from
	"prod2-generico"."prod2-generico"."cfr-patient-request" cpr 
left join (select
        iss."store-id" ,
        iss."drug-id" ,
        (case when iss."bucket" in ('AW','AX','AY','AZ') then 'A'
        when iss."bucket" in ('BW','BX','BY','BZ') then 'B'
        when iss."bucket" in ('CW','CX','CY','CZ') then 'C'
        end ) as "bucket"
    from
        "prod2-generico"."ipc2-segmentation" iss
    inner join (
        select
            "store-id" ,
            max("reset-date") as latest_reset
        from
            "prod2-generico"."ipc2-segmentation" iss
        group by
            "store-id" 
    ) as sq
    on
        iss."store-id" = sq."store-id"
        and iss."reset-date" = sq.latest_reset ) b on cpr."store-id" =b."store-id"
        and cpr."drug-id" =b."drug-id"
where
	"shortbook-date" >= '{date1}'
	and "shortbook-date" <= '{date2}'
	and cpr."drug-id" <> -1
	and "loss-quantity" > 0
group by
1,2,3) a
where a."bucket" is not null
group by a."date",a."store-id",a."bucket";
'''



pr_class_wise_demand = rs_db.get_df(pr_class_wise_demand)
pr_class_wise_demand.columns = [c.replace('-', '_') for c in pr_class_wise_demand.columns]
pr_class_wise_demand['date'] =  pr_class_wise_demand['date'].astype('str')


pr_class_wise_demand=pr_class_wise_demand.fillna(0)


pr_class_wise_demand[['class_wise_demand_net_quantity','class_wise_demand_pr_net_quantity']]=\
    pr_class_wise_demand[['class_wise_demand_net_quantity','class_wise_demand_pr_net_quantity']].astype('int')


pr_class_wise_demand[[ 'class_wise_demand_revenue','class_wise_revenue_pr_revenue']]=\
    pr_class_wise_demand[['class_wise_demand_revenue','class_wise_revenue_pr_revenue']].astype('float')



pr_class_wise_demand_pivot = pr_class_wise_demand.pivot_table(index=['store_id', 'date'], columns='bucket',values=[ 'class_wise_demand_net_quantity',
       'class_wise_demand_pr_net_quantity', 'class_wise_demand_revenue',
       'class_wise_revenue_pr_revenue'])



pr_class_wise_demand_pivot.columns = ['_'.join(col).strip() for col in pr_class_wise_demand_pivot.columns.values]



pr_class_wise_demand_pivot.reset_index(inplace=True)

pr_class_wise_demand_pivot=pr_class_wise_demand_pivot.fillna(0)

#Sufficiency

sufficiency=f'''
select
a."store-id",
a."created-at" as "date",
sum("goodaid-oos-count") as "goodaid-oos-count",
sum("goodaid-oos-min-count") as "goodaid-oos-min-count",
sum("goodaid-drug-count") as "goodaid-drug-count",
sum("ethical-oos-count") as "ethical-oos-count",
sum("ethical-oos-min-count") as "ethical-oos-min-count",
sum("ethical-drug-count") as "ethical-drug-count",
sum("generic-oos-count") as "generic-oos-count",
sum("generic-oos-min-count") as "generic-oos-min-count",
sum("generic-drug-count") as "generic-drug-count",
sum("other-oos-count") as "other-oos-count",
sum("other-oos-min-count") as "other-oos-min-count",
sum("other-drug-count") as "other-drug-count",
SUM("ethical-a-class-oos-count") as "ethical-a-class-oos-count",
SUM("ethical-a-class-oos-min-count") as "ethical-a-class-oos-min-count" ,
SUM("ethical-a-class-drug-count") as "ethical-a-class-drug-count"
from (
select
	oosdl."store-id" ,
	oosdl."closing-date" as "created-at" ,
	case when d."company-id" = 6984 then ("oos-count") end as "goodaid-oos-count",
	case when d."company-id" = 6984 then ("oos-min-count") end as "goodaid-oos-min-count",
	case when d."company-id" = 6984 then ("drug-count") end as "goodaid-drug-count",
	case when d."type" = 'ethical' then ("oos-count") end as "ethical-oos-count",
	case when d."type" = 'ethical' then ("oos-min-count") end as "ethical-oos-min-count",
	case when d."type" = 'ethical' then ("drug-count") end as "ethical-drug-count",
	case when d."type" = 'generic' then ("oos-count") end as "generic-oos-count",
	case when d."type" = 'generic' then ("oos-min-count") end as "generic-oos-min-count",
	case when d."type" = 'generic' then ("drug-count") end as "generic-drug-count",
	case when d."type" not in ('generic','generic') then ("oos-count") end as "other-oos-count",
	case when d."type" not in ('generic','generic') then ("oos-min-count") end as "other-oos-min-count",
	case when d."type" not in ('generic','generic') then ("drug-count") end as "other-drug-count",
	case when d."type" = 'ethical' and b."bucket"='A' then ("oos-count") end as "ethical-a-class-oos-count",
	case when d."type" = 'ethical' and b."bucket"='A' then ("oos-min-count") end as "ethical-a-class-oos-min-count",
	case when d."type" = 'ethical' and b."bucket"='A' then ("drug-count") end as "ethical-a-class-drug-count"
from
	"prod2-generico"."out-of-shelf-drug-level" oosdl
left join "prod2-generico"."prod2-generico".drugs d 
on
	oosdl."drug-id" = d.id
left join (
select
        iss."store-id" ,
        iss."drug-id" ,
        (case when iss."bucket" in ('AW','AX','AY','AZ') then 'A'
        when iss."bucket" in ('BW','BX','BY','BZ') then 'B'
        when iss."bucket" in ('CW','CX','CY','CZ') then 'C'
        end ) as "bucket"
    from
        "prod2-generico"."ipc2-segmentation" iss
    inner join (
        select
            "store-id" ,
            max("reset-date") as latest_reset
        from
            "prod2-generico"."ipc2-segmentation" iss
        group by
            "store-id" 
    ) as sq
    on
        iss."store-id" = sq."store-id"
        and iss."reset-date" = sq.latest_reset) b on oosdl."drug-id" =b."drug-id"
        and oosdl."store-id" =b."store-id"
where
	"closing-date" >= '{date1}'
	and "closing-date" <= '{date2}'
	and "max-set" = 'Y' and "mature-flag" = 'Y'
	)a	
group by
	a."store-id" ,
	a."created-at"
'''

sufficiency = rs_db.get_df(sufficiency)
sufficiency.columns = [c.replace('-', '_') for c in sufficiency.columns]
sufficiency['date'] =  sufficiency['date'].astype('str')



wh_availability=f'''
select
	199 as "store-id",
	m."drug-type-group",
	date(m."snapshot-date") as "date",
	SUM(m."not-available") as "not-available-drug-count-wh",
	SUM(m."available") as "available-drug-count-wh"
from 
(
	select
		wssm."drug-id" ,
		(case
			when d."type" = 'ethical' then 'ethical'
			when (d."type" = 'generic'
			and d."company-id" != 6984) then 'generic(non-gaid)'
			when (d."company-id" = 6984) then 'goodaid'
			else 'other'
		end ) as "drug-type-group",
		date(a."snapshot-date") as "snapshot-date",
		coalesce (a."current-inventory",
		0) as "current-inventory",
		coalesce (a."safety-stock",
		0) as "safety-stock",
		(case
			when coalesce (a."current-inventory",
			0) <coalesce (a."safety-stock",
			0) then 1
			else 0
		end ) as "not-available",
		(case
			when coalesce (a."current-inventory",
			0) >= coalesce (a."safety-stock",
			0) then 1
			else 0
		end ) as "available"
	from
		"prod2-generico"."prod2-generico"."wh-sku-subs-master" wssm
	left join "prod2-generico"."prod2-generico".drugs d on
		wssm."drug-id" = d.id
	left join 
(
		select
			wis."drug-id" ,
			SUM(wis."balance-quantity") as "current-inventory" ,
			wis."snapshot-date" as "snapshot-date" ,
			avg(wis."safety-stock") as "safety-stock"
		from
			"prod2-generico"."prod2-generico"."wh-inventory-ss" wis
		where
			date(wis."snapshot-date") >='{date1}' and date(wis."snapshot-date")<='{date2}'
				and wis."wh-id" in (199)
			group by
				wis."drug-id",
				"snapshot-date" ) a on
		wssm."drug-id" = a."drug-id"
	where
		d."type" not in ('banned', 'discontinued-products')
		and wssm."add-wh" = 'Yes') m
group by
	"store-id",
	m."drug-type-group",
	m."snapshot-date" 
'''



wh_availability = rs_db.get_df(wh_availability)
wh_availability.columns = [c.replace('-', '_') for c in wh_availability.columns]
wh_availability['date'] =  wh_availability['date'].astype('str')


wh_availability_pivot = wh_availability.pivot_table(index=['store_id', 'date'], columns='drug_type_group', values=['not_available_drug_count_wh', 'available_drug_count_wh'])

wh_availability_pivot.columns = ['_'.join(col).strip() for col in wh_availability_pivot.columns.values]


wh_availability_pivot.reset_index(inplace=True)




# Store near expiry

store_near_expiry=f'''
select
	date(si."snapshot-date")  as "date",
	si."entity-id" as "store-id" ,
	SUM(case when si."inventory-sub-type-1" = 'near-expiry'
	then si."value-with-tax" end ) as "near-expiry-value-store",
	SUM(si."value-with-tax") as "total-value-store"
from
	"prod2-generico"."prod2-generico"."system-inventory" si
where
	si."entity-type" = 'store'
	and si."franchise-id" = 1 and date(si."snapshot-date") >= '{date1}'
	and date(si."snapshot-date") <= '{date2}'
group by
	si."snapshot-date" ,
	si."entity-id" 
'''


store_near_expiry = rs_db.get_df(store_near_expiry)
store_near_expiry.columns = [c.replace('-', '_') for c in store_near_expiry.columns]
store_near_expiry['date'] =  store_near_expiry['date'].astype('str')


wh_near_expiry=f'''
select
	a."wh-id" as "store-id",
	a."snapshot-date" as "date",
	coalesce (a."total-near-expiry-value-wh",0) as "total-near-expiry-value-wh",
	a."total-value-wh"
from
	(
	select
		wis."wh-id" ,
		date(wis."snapshot-date") as "snapshot-date",
		SUM(case
			when (DATEDIFF('days',
			wis."snapshot-date" ,
			date(wis.expiry))<= 30
			and DATEDIFF('days',
			wis."snapshot-date" ,
			date(wis.expiry)) >0) then wis."balance-value" + wis."locked-value"
		end ) as "total-near-expiry-value-wh",
		SUM(wis."balance-value" + wis."locked-value") as "total-value-wh"
	from
		"prod2-generico"."prod2-generico"."wh-inventory-ss" wis
	where
	 date(wis."snapshot-date") >= '{date1}'
	and date(wis."snapshot-date") <= '{date2}'
		and wis."wh-id" IN (199,343,342)
	group by date(wis."snapshot-date"),"wh-id" 
) a 
'''

wh_near_expiry = rs_db.get_df(wh_near_expiry)
wh_near_expiry.columns = [c.replace('-', '_') for c in wh_near_expiry.columns]
wh_near_expiry['date'] =  wh_near_expiry['date'].astype('str')

# PR Control

# Pr data

pr_contributiton = f'''
select
	date(s."created-at") as "date" ,
	s."store-id" ,
	SUM(s."net-quantity") as "pr-control-total-net-quantity",
	SUM(s."revenue-value") as "pr-control-total-revenue",
	SUM(case when s."pr-flag" is true then s."net-quantity" 
	else 0 end ) as "pr-control-net-quantity",
	SUM(case when s."pr-flag" is true then s."revenue-value"
	else 0 end ) as "pr-control-revenue-value"
from
	"prod2-generico"."prod2-generico".sales s
where
	s."store-b2b" = 'Store'
	and date(s."created-at")>= '{date1}'
	and date(s."created-at")<= '{date2}'
group by
	1,
	2 
'''


pr_contributiton = rs_db.get_df(pr_contributiton)
pr_contributiton.columns = [c.replace('-', '_') for c in pr_contributiton.columns]
pr_contributiton['date'] =  pr_contributiton['date'].astype('str')


# A-class pr contribution

a_class_pr=f'''
select
	date(s."created-at") as "date" ,
	s."store-id" ,
	SUM(s."net-quantity") as "pr-control-total-net-quantity-a-class",
	SUM(case when s."pr-flag" is true then s."net-quantity" 
	else 0 end ) as "pr-control-net-quantity-a-class",
	SUM(s."revenue-value") as "pr-control-total-revenue-a-class",
	SUM(case when s."pr-flag" is true then s."revenue-value" 
	else 0 end ) as "pr-control-revenue-a-class"
from
	"prod2-generico"."prod2-generico".sales s
left join (select
        iss."store-id" ,
        iss."drug-id" ,
        iss.bucket 
    from
        "prod2-generico"."ipc2-segmentation" iss
    inner join (
        select
            "store-id" ,
            max("reset-date") as latest_reset
        from
            "prod2-generico"."ipc2-segmentation" iss
        group by
            "store-id" 
    ) as sq
    on
        iss."store-id" = sq."store-id"
        and iss."reset-date" = sq.latest_reset ) b on s."store-id" =b."store-id"
        and s."drug-id" =b."drug-id"
where
	s."store-b2b" = 'Store'
	and date(s."created-at")>= '{date1}'
	and date(s."created-at")<= '{date2}' and b.bucket in (
	'AW','AX','AY','AZ')
group by
	1,
	2 
'''

a_class_pr = rs_db.get_df(a_class_pr)
a_class_pr.columns = [c.replace('-', '_') for c in a_class_pr.columns]
a_class_pr['date'] =  a_class_pr['date'].astype('str')


#Input Margin

input_margin=f'''
select
	i."store-id",
	(case
		when d."type" = 'ethical' then 'ethical'
		when (d."type" = 'generic'
		and d."company-id" != 6984) then 'generic(non-gaid)'
		when (d."company-id" = 6984) then 'goodaid'
		when (d."type" = 'ayurvedic' ) then 'ayurvedic'
		when (d."type" = 'surgical') then 'surgical'
		when (d."type" in ('baby-food', 'baby-product')) then 'baby-food and baby-product'
		else 'other'
	end ) as "drug-type-group",
	date(i."approved-at") as "date" ,
	SUM(ii."net-value") as "wc-value-margin" ,
	SUM(ii.mrp*ii."actual-quantity") as "mrp-value-margin"
from
	"prod2-generico"."prod2-generico"."invoice-items" ii
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" = i.id
left join "prod2-generico"."prod2-generico".stores s on
	i."store-id" = s.id
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
where
	s."franchisee-id" = 1
	and i."franchisee-invoice" = 0 and date(i."approved-at")>='{date1}' and date(i."approved-at")
	<='{date2}'
group by i."store-id", "drug-type-group",date(i."approved-at")
'''



input_margin = rs_db.get_df(input_margin)
input_margin.columns = [c.replace('-', '_') for c in input_margin.columns]
input_margin['date'] =  input_margin['date'].astype('str')


input_margin_pivot = input_margin.pivot_table(index=['store_id', 'date'], columns='drug_type_group',
                                      values=['wc_value_margin',
       'mrp_value_margin'])




input_margin_pivot.columns = ['_'.join(col).strip() for col in input_margin_pivot.columns.values]
input_margin_pivot.reset_index(inplace=True)



input_margin_pivot=input_margin_pivot.fillna(0)



#oos

oos=f'''
  select
	oos."closing-date" as "date",
	oos."store-id" ,
	sum(oos."drug-count") as "total_drug_count_oos_overall",
	sum(oos."oos-count") as "total_oos_drug_count_oos_overall"
from
	"prod2-generico"."out-of-shelf-drug-level" oos
inner join "prod2-generico"."drugs" d on
	oos."drug-id" = d."id"
inner join "prod2-generico"."prod2-generico".stores s on oos."store-id" =s.id 
where
	oos."max-set" = 'Y'
    and oos."mature-flag" = 'Y'
    and date(oos."closing-date") >='{date1}'
    and date(oos."closing-date") <='{date2}'
    and s."franchisee-id" =1
group by
	1,2
'''


oos = rs_db.get_df(oos)
oos.columns = [c.replace('-', '_') for c in oos.columns]
oos['date'] =  oos['date'].astype('str')

ps_ratio=f'''
select a."store-id",
a."approved-date" as "date",
a."purchase-value" as "purchase-value-ps-ratio",
b."cogs-wc" as "cogs-wc-ps-ratio"
from 
(select
	psm."entity-id" as "store-id",
	date(psm."approved-date") as  "approved-date",
	SUM(psm."net-value") as "purchase-value"
from
	"prod2-generico"."prod2-generico"."purchase-sales-meta" psm 
where psm."type-1" ='store' and psm."sub-type-1" ='PB' and 
psm."approved-date">='{date1}'and psm."approved-date"<='{date2}'
group by psm."entity-id",date(psm."approved-date")) a
left join  (select
	s."store-id",
	date(s."created-at") as "sales-date",
	SUM(s."net-quantity" * s."purchase-rate") as "cogs-wc"
from
	"prod2-generico"."prod2-generico".sales s
where
	s."franchisee-id" = 1 
	and s."store-b2b" = 'Store' and date(s."created-at")>='{date1}'
		and date(s."created-at")<='{date2}'
group by s."store-id",date(s."created-at") )b on a."store-id"=b."store-id"
	and a."approved-date"=b."sales-date"
'''

ps_ratio = rs_db.get_df(ps_ratio)
ps_ratio.columns = [c.replace('-', '_') for c in ps_ratio.columns]
ps_ratio['date'] =  ps_ratio['date'].astype('str')

lp_pr = f"""
    select
	lp."store-id" ,
	lp."received-date" as "date",
	sum(lp."lp-sales-sum") as "lp-sales-sum",
	sum(lp."lp-value") as "lp-value",
	sum(s."lp_pr_sales") as "lp_pr_sales"
from
	(
	select
		lp."store-id" ,
		lp."received-date",
		sum(lp."lp-sales-sum") as "lp-sales-sum",
		sum(lp."lp-value-sum") as "lp-value"
	from
		"prod2-generico"."lp-liquidation" lp
	where
		date(lp."received-date")>= '{date1}'
		and date(lp."received-date")<= '{date2}'
	group by
		lp."store-id" ,
		date(lp."received-date")) lp
inner join (
	select
		"store-id" ,
		"created-date",
		sum(case when "pr-flag" = true then "revenue-value" end) as "lp_pr_sales"
	from
		"prod2-generico"."sales"
	where
		date("created-at")>= '{date1}'
		and date("created-at")<= '{date2}'
	group by
		1,
		2) s on
	s."store-id" = lp."store-id"
	and s."created-date" = lp."received-date"
where
	date(lp."received-date")>= '{date1}'
	and date(lp."received-date")<= '{date2}'
group by
	lp."store-id" ,
	date(lp."received-date")
"""



lp_liq = rs_db.get_df(lp_pr)
lp_liq.columns = [c.replace('-', '_') for c in lp_liq.columns]
lp_liq['date'] = lp_liq['date'].astype('str')



m_data = pd.merge(left=m_data,right=as_dc_wh_pivot,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=pr_ff_pivot,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=pr_contributiton,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=pr_class_wise_demand_pivot,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=sufficiency,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=wh_availability_pivot,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=store_near_expiry,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=wh_near_expiry,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=a_class_pr,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=input_margin_pivot,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=oos,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=ps_ratio,how='left',on=['store_id','date'])

m_data = pd.merge(left=m_data,right=lp_liq,how='left',on=['store_id','date'])


m_data=m_data.fillna(0)



m_data[['dc_otif_quantity_ethical',
       'dc_otif_quantity_generic', 'dc_otif_quantity_other',
       'dc_quantity_ethical', 'dc_quantity_generic', 'dc_quantity_other',
       'dc_required_quantity_ethical', 'dc_required_quantity_generic',
       'dc_required_quantity_other', 'wh_otif_quantity_ethical',
       'wh_otif_quantity_generic', 'wh_otif_quantity_other',
       'wh_quantity_ethical', 'wh_quantity_generic', 'wh_quantity_other',
       'wh_required_quantity_ethical', 'wh_required_quantity_generic',
       'wh_required_quantity_other', 'pr_dc_otif_quantity_ethical',
       'pr_dc_otif_quantity_generic', 'pr_dc_otif_quantity_other',
       'pr_dc_quantity_ethical', 'pr_dc_quantity_generic',
       'pr_dc_quantity_other', 'pr_dc_required_quantity_ethical',
       'pr_dc_required_quantity_generic', 'pr_dc_required_quantity_other',
       'pr_wh_otif_quantity_ethical', 'pr_wh_otif_quantity_generic',
       'pr_wh_otif_quantity_other','pr_control_total_net_quantity','pr_control_net_quantity',
        'pr_wh_quantity_ethical',
       'pr_wh_quantity_generic', 'pr_wh_quantity_other',
       'pr_wh_required_quantity_ethical', 'pr_wh_required_quantity_generic',
       'pr_wh_required_quantity_other', 'class_wise_demand_pr_net_quantity_A',
       'class_wise_demand_pr_net_quantity_B',
       'class_wise_demand_pr_net_quantity_C', 'goodaid_oos_count',
       'goodaid_oos_min_count', 'goodaid_drug_count', 'ethical_oos_count',
       'ethical_oos_min_count', 'ethical_drug_count', 'generic_oos_count',
       'generic_oos_min_count', 'generic_drug_count', 'other_oos_count',
       'other_oos_min_count', 'other_drug_count',
       'available_drug_count_wh_ethical',
       'available_drug_count_wh_generic(non-gaid)',
       'available_drug_count_wh_other', 'not_available_drug_count_wh_ethical',
       'not_available_drug_count_wh_generic(non-gaid)',
       'not_available_drug_count_wh_other',
       'pr_control_total_net_quantity_a_class',
       'pr_control_net_quantity_a_class',
       'total_drug_count_oos_overall', 'total_oos_drug_count_oos_overall',
        'available_drug_count_wh_goodaid','not_available_drug_count_wh_goodaid',
        'wh_otif_required_quantity_ethical','wh_otif_required_quantity_generic',
        'wh_otif_required_quantity_other','dc_otif_required_quantity_ethical',
        'dc_otif_required_quantity_generic','dc_otif_required_quantity_other',
        'ethical_a_class_oos_count',
        'ethical_a_class_oos_min_count',
        'ethical_a_class_drug_count']]=m_data[['dc_otif_quantity_ethical',
       'dc_otif_quantity_generic', 'dc_otif_quantity_other',
       'dc_quantity_ethical', 'dc_quantity_generic', 'dc_quantity_other',
       'dc_required_quantity_ethical', 'dc_required_quantity_generic',
       'dc_required_quantity_other', 'wh_otif_quantity_ethical',
       'wh_otif_quantity_generic', 'wh_otif_quantity_other',
       'wh_quantity_ethical', 'wh_quantity_generic', 'wh_quantity_other',
       'wh_required_quantity_ethical', 'wh_required_quantity_generic',
       'wh_required_quantity_other', 'pr_dc_otif_quantity_ethical',
       'pr_dc_otif_quantity_generic', 'pr_dc_otif_quantity_other',
       'pr_dc_quantity_ethical', 'pr_dc_quantity_generic',
       'pr_dc_quantity_other', 'pr_dc_required_quantity_ethical',
       'pr_dc_required_quantity_generic', 'pr_dc_required_quantity_other',
       'pr_wh_otif_quantity_ethical', 'pr_wh_otif_quantity_generic',
       'pr_wh_otif_quantity_other', 'pr_control_total_net_quantity','pr_control_net_quantity',
       'pr_wh_quantity_ethical',
       'pr_wh_quantity_generic', 'pr_wh_quantity_other',
       'pr_wh_required_quantity_ethical', 'pr_wh_required_quantity_generic',
       'pr_wh_required_quantity_other', 'class_wise_demand_pr_net_quantity_A',
       'class_wise_demand_pr_net_quantity_B',
       'class_wise_demand_pr_net_quantity_C', 'goodaid_oos_count',
       'goodaid_oos_min_count', 'goodaid_drug_count', 'ethical_oos_count',
       'ethical_oos_min_count', 'ethical_drug_count', 'generic_oos_count',
       'generic_oos_min_count', 'generic_drug_count', 'other_oos_count',
       'other_oos_min_count', 'other_drug_count',
       'available_drug_count_wh_ethical',
       'available_drug_count_wh_generic(non-gaid)',
       'available_drug_count_wh_other', 'not_available_drug_count_wh_ethical',
       'not_available_drug_count_wh_generic(non-gaid)',
       'not_available_drug_count_wh_other',
       'pr_control_total_net_quantity_a_class',
       'pr_control_net_quantity_a_class',
       'total_drug_count_oos_overall', 'total_oos_drug_count_oos_overall','available_drug_count_wh_goodaid',
        'not_available_drug_count_wh_goodaid','wh_otif_required_quantity_ethical','wh_otif_required_quantity_generic',
        'wh_otif_required_quantity_other','dc_otif_required_quantity_ethical',
        'dc_otif_required_quantity_generic','dc_otif_required_quantity_other',
        'ethical_a_class_oos_count',
        'ethical_a_class_oos_min_count',
        'ethical_a_class_drug_count']].astype('int64')



m_data[['class_wise_demand_revenue_A',
       'class_wise_demand_revenue_B', 'class_wise_demand_revenue_C',
       'class_wise_revenue_pr_revenue_A', 'class_wise_revenue_pr_revenue_B',
       'class_wise_revenue_pr_revenue_C', 'near_expiry_value_store',
       'total_value_store', 'total_near_expiry_value_wh', 'total_value_wh', 'mrp_value_margin_ayurvedic',
       'mrp_value_margin_baby-food and baby-product',
       'mrp_value_margin_ethical', 'mrp_value_margin_generic(non-gaid)',
       'mrp_value_margin_goodaid', 'mrp_value_margin_other',
       'mrp_value_margin_surgical', 'wc_value_margin_ayurvedic',
       'wc_value_margin_baby-food and baby-product', 'wc_value_margin_ethical',
       'wc_value_margin_generic(non-gaid)', 'wc_value_margin_goodaid',
       'wc_value_margin_other', 'wc_value_margin_surgical',
       'purchase_value_ps_ratio', 'cogs_wc_ps_ratio', 'lp_sales_sum',
       'lp_value', 'lp_pr_sales','pr_control_total_revenue','pr_control_revenue_value',
        'pr_control_revenue_a_class','pr_control_total_revenue_a_class']]=m_data[['class_wise_demand_revenue_A',
       'class_wise_demand_revenue_B', 'class_wise_demand_revenue_C',
       'class_wise_revenue_pr_revenue_A', 'class_wise_revenue_pr_revenue_B',
       'class_wise_revenue_pr_revenue_C', 'near_expiry_value_store',
       'total_value_store', 'total_near_expiry_value_wh', 'total_value_wh', 'mrp_value_margin_ayurvedic',
       'mrp_value_margin_baby-food and baby-product',
       'mrp_value_margin_ethical', 'mrp_value_margin_generic(non-gaid)',
       'mrp_value_margin_goodaid', 'mrp_value_margin_other',
       'mrp_value_margin_surgical', 'wc_value_margin_ayurvedic',
       'wc_value_margin_baby-food and baby-product', 'wc_value_margin_ethical',
       'wc_value_margin_generic(non-gaid)', 'wc_value_margin_goodaid',
       'wc_value_margin_other', 'wc_value_margin_surgical',
       'purchase_value_ps_ratio', 'cogs_wc_ps_ratio', 'lp_sales_sum',
       'lp_value', 'lp_pr_sales','pr_control_total_revenue','pr_control_revenue_value',
       'pr_control_revenue_a_class','pr_control_total_revenue_a_class']].astype('float')


m_data['date'] = pd.to_datetime(m_data['date'])


# =============================================================================
# store info
# =============================================================================

s_info = f"""
select
	sm.id as "store-id",
	sm.store  as "store-name",
	sm."franchisee-id" ,
	sm."franchisee-name" ,
	sm.abo ,
	sm."line-manager" ,
	sm."cluster-name" ,
	sm.city ,
	sm.acquired ,
	sm."old-new-static" 
from
	"prod2-generico"."prod2-generico"."stores-master" sm
"""
store_info = rs_db.get_df(s_info)
store_info.columns = [c.replace('-', '_') for c in store_info.columns]

m_data = pd.merge(left=m_data,right=store_info,on=['store_id'],how='left')


m_data.columns = [c.replace('_', '-') for c in m_data.columns]

m_data.columns = m_data.columns.str.lower()


created_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

m_data['etl-created-at']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

updated_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

m_data['etl-updated-at']=datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")
m_data['etl-created-by'] = 'etl-automation'
m_data['etl-updated-by'] = 'etl-automation'

truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''

rs_db.execute(truncate_query)

<<<<<<< HEAD
#Writing to db

=======
>>>>>>> ee45da78b8b4214f070db360930bf4e0dacf1008
s3.write_df_to_db(df=m_data[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)


                                    # ***  Part-1 Ends Here *** #


# =============================================================================
# Part-2 : Month Level Supply Chain Metrics  (NPI, Returns, PR & MS Liquidation)
# =============================================================================



schema_1 = 'prod2-generico'
table_name_1 = 'supplychain-ops-metrics-month'
table_info_1 = helper.get_table_info(db=rs_db, table_name=table_name_1, schema=schema_1)


date1= (datetime.today() + relativedelta(months=-7)).replace(day=1).strftime('%Y-%m')
date2= (datetime.today() + relativedelta(days=-1)).strftime('%Y-%m')

d_date = pd.DataFrame({'join':['A']})

#d_date['join']='A'

d_date['start_month']= date1

d_date['end_month']= date2

d_date['date'] = [pd.date_range(s, e, freq='MS') for s, e in
                         zip(pd.to_datetime(d_date['start_month']),
                             pd.to_datetime(d_date['end_month']))]


d_date = pd.DataFrame({'date': np.concatenate(d_date.date.values)})
d_date['join']='A'


d_date['date'] = d_date['date'].astype('str')

sc_data = pd.merge(left=sm_data,right=d_date,on=['join'],how='inner')

sc_data.drop('join',axis=1,inplace=True)

# NPI

npi = '''
select
	dead."store-id",
	dead."year",
	dead."month",
	dead."rotate-quantity" as "npi-quantity",
	inv."inventory-quantity" as "inventory-quantity-store",
	dead."rotate-value" as "npi-inventory-value-store",
	inv."inventory-value" as "inventory-value-store"
from
	(
	(
	select
		dsis."store-id" ,
		date_part('month', dsis."snapshot-date") as "month",
		date_part('year', dsis."snapshot-date") as "year",
		sum(dsis.quantity + dsis."locked-quantity") as "rotate-quantity",
		sum(dsis.value + dsis."locked-value") as "rotate-value"
	from
		"prod2-generico"."prod2-generico"."dead-stock-inventory-sns" dsis
	where
		dsis."inventory-type" = 'Rotate'
		and dsis."snapshot-date" >= date(date_trunc('month',date(current_date- interval '7 Months')))
		--	and dsis."store-id" = 2
		--	and dsis."snapshot-date" >= '{date1}'
		--	and dsis."snapshot-date" <= '{date2}'
	group by
		dsis."store-id" ,
		date_part('month', dsis."snapshot-date"),
		date_part('year', dsis."snapshot-date")) dead
left join 
	(
select
		si."entity-id" as "store-id",
		date_part('month', si."snapshot-date") as "month",
		date_part('year', si."snapshot-date") as "year",
		sum(si.quantity) as "inventory-quantity",
		sum(si."value-with-tax") as "inventory-value"
	from
		"prod2-generico"."prod2-generico"."system-inventory" si 
	left join "prod2-generico"."prod2-generico".stores s on
		si."entity-id" =s.id 
	where
		date_part('day', si."snapshot-date") = 1 and si."entity-type" ='store'
		 -- and i."store-id" = 2  
		and date(si."snapshot-date") >= date(date_trunc('month',date(current_date- interval '7 Months')))
		group by
			si."entity-id" ,
			date_part('month', si."snapshot-date"),
			date_part('year', si."snapshot-date"))inv
on
	dead."store-id" = inv."store-id"
	and dead."month" = inv."month"
	and dead."year" = inv."year")
'''



npi = rs_db.get_df(npi)
npi.columns = [c.replace('-', '_') for c in npi.columns]


npi['date'] = pd.to_datetime(npi[['year', 'month']].assign(day=1))
npi['date'] = npi['date'].astype('str')
npi=npi.drop(['year','month'],axis=1)

sc_data=pd.merge(sc_data,npi,how='left',on=['store_id','date'])

non_saleable_returns='''
SELECT
	extract (year from rtd1."created-at") as "year",
	extract(month from rtd1."created-at") as "month",
	s.id as "store-id",
	CASE
		WHEN ri1.status = 'saved' THEN 'Store Return Saved'
		WHEN ri1.status = 'approved'
		AND dn1.status = 'saved' THEN 'Store DN Saved'
		WHEN ri1.status = 'approved'
		AND dn1.status = 'dispatched' THEN 'DN Dispatched'
		WHEN ri1.status = 'approved'
		AND dn1.status = 'received' THEN 'DN Received'
		WHEN( ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND (ri.status = 'settled'
		OR ri.status = 'approved')
		AND dn.status = 'saved'
		AND pb.id is not NULL)
		OR ((ri.status = 'settled'
		OR ri.status = 'approved')
		AND dn.status = 'saved'
		AND pb.id is not NULL)THEN 'PDN Box Created'
		WHEN (ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status = 'approved'
		AND dn.status = 'saved' )
		OR (ri.status = 'approved'
		AND dn.status = 'saved' )THEN 'PDN Saved'
		WHEN( ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND (ri.status = 'settled'
		OR ri.status = 'approved')
		AND dn.status = 'dispatched' )
		OR ((ri.status = 'settled'
		OR ri.status = 'approved')
		AND dn.status = 'dispatched' )THEN 'PDN Dispatched'
		WHEN (ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status = 'approved'
		AND dn.status = 'approved' )
		OR (ri.status = 'approved'
		AND dn.status = 'approved' )THEN 'PDN Approved'
		WHEN (ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status = 'settled'
		AND (dn.status = 'settled'
		OR dn.status = 'accounted' ))
		OR (ri.status = 'settled'
		AND (dn.status = 'settled'
		OR dn.status = 'accounted' ))THEN 'PDN Settled'
		WHEN ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status = 'discarded' THEN 'Non Salable/Expiry Discarded'
		WHEN ri1."return-item-reference" is NULL
		AND ri1.status = 'settled'
		AND ((dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		OR dn1.status = 'accounted')
		AND ri.status IS NULL
		AND dn.status IS NULL THEN 'Yet To create PDN'
		WHEN salebletononsaleblecheck.status in ('amended', 'settled')
		AND salebletononsaleblecheck."return-reason" = 'reason-npi-saleable'
		AND ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status IS NULL
		AND dn.status IS NULL THEN 'S-NS Debit Note Settled'
		WHEN salebletononsaleblecheck.status in ('amended', 'settled')
		AND salebletononsaleblecheck."return-reason" = 'reason-npi-saleable'
		AND ri1.status = 'settled'
		AND dn1.status = 'transferred'
		AND ri.status IS NULL
		AND dn.status IS NULL THEN 'S-NS Debit Note Transferref'
		ELSE 'Status Issue'
	END AS "Comprehensive status",
	SUM(ri1."returned-quantity") AS "return-qty",
	SUM(CASE
		WHEN ri.status is NULL THEN ri1.net
		WHEN ri1.status = 'settled'
		AND (dn1.status = 'settled' or dn1.status = 'franchisee-settled')
		AND ri.status = 'discarded'
		AND dn.status is NOT NULL THEN ri."discarded-quantity" * ri.rate
		ELSE ri.net
	end) AS "return-net-value"
FROM
	"prod2-generico"."returns-to-dc-1" rtd1
LEFT JOIN "prod2-generico"."return-items-1" ri1
ON
	rtd1.id = ri1."return-id"
LEFT JOIN "prod2-generico"."debit-note-items-1" dni1
ON
	ri1.id = dni1."item-id"
	AND dni1."is-active" != 0
LEFT JOIN "prod2-generico"."debit-notes-1" dn1 
ON
	dni1."debit-note-id" = dn1.id
LEFT JOIN "prod2-generico"."return-items" ri 
ON
	ri1.id = ri."return-item-reference"
LEFT JOIN "prod2-generico"."debit-note-items" dni 
ON
	ri.id = dni."item-id"
	AND dni."is-active" != 0
LEFT JOIN "prod2-generico"."debit-notes" dn
ON
	dni."debit-note-id" = dn.id
LEFT JOIN "prod2-generico"."returns-to-dc" rtd 
ON
	ri."return-id" = rtd.id
LEFT JOIN "prod2-generico"."inventory-1" i 
ON
	ri1."inventory-id" = i.id
LEFT JOIN "prod2-generico".stores s 
ON
	rtd1."store-id" = s.id
LEFT JOIN "prod2-generico"."zeno-city" zc 
ON
	s."city-id" = zc.id
LEFT JOIN "prod2-generico".drugs d 
ON
	i."drug-id" = d.id
LEFT JOIN "prod2-generico".invoices iv 
ON
	i."invoice-id" = iv.id
LEFT join "prod2-generico".distributors d2 
ON
	iv."distributor-id" = d2.id
LEFT JOIN "prod2-generico".stores rs
ON
	ri1."return-dc-id" = rs.id
LEFT JOIN "prod2-generico"."pdn-boxes" pb 
ON
	dn.id = pb."debit-note-id"
LEFT JOIN "prod2-generico".distributors dndist 
ON
	dn."dist-id" = dndist.id
LEFT JOIN "prod2-generico"."return-items-1" salebletononsaleblecheck 
ON
	ri1."return-item-reference" = salebletononsaleblecheck.id
LEFT JOIN "prod2-generico"."return-item-transfers" rit 
ON ri1.id = rit."return-item-id" 
LEFT JOIN "prod2-generico".franchisees f 
ON s."franchisee-id" = f.id 
left join "prod2-generico".bins bn1
on bn1.id = dni1."bin-id" 
WHERE
	(((ri.id is NULL
		AND ri1."return-reason" IN ( 'reason-product-expired', 'reason-over-expiry', 'reason-npi-non-saleable'))
		OR ri."return-reason" IN ( 'reason-product-expired', 'reason-over-expiry', 'reason-npi-non-saleable'))
		OR (((ri.id is NULL
			AND ri1."return-reason" IN ('reason-product-damaged', 'reason-near-expiry'))
			OR ri."return-reason" IN ('reason-product-damaged', 'reason-near-expiry'))
			AND (DATEDIFF(d,iv."invoice-date",rtd1."created-at")>= 30))
			OR (ri1."return-dc-id" in (199, 202, 175)))
	AND ri1.status != 'amended'
	AND ri1.status != 'discarded'
	AND ri1.status != 'reverted'
	-- Reason for this is return item reference was created in July 2021
	AND 
	(CASE
		WHEN ri."return-item-reference" is NULL THEN DATE(rtd1."created-at") > '2021-08-01'
		ELSE DATE(rtd1."created-at") > '1970-01-01'
	end)  and date(rtd1."created-at") >= date(date_trunc('month',date(current_date- interval '7 Months')))
group by 1,2,3,4
'''


non_saleable_return = rs_db.get_df(non_saleable_returns)
non_saleable_return.columns = [c.replace('-', '_') for c in non_saleable_return.columns]

non_saleable_return['return_net_value']=non_saleable_return['return_net_value'].fillna(0)


non_saleable_return_pivot = non_saleable_return.pivot_table(index=['store_id', 'year','month'], columns='comprehensive status',
                                      values=['return_net_value'])

non_saleable_return_pivot.columns = ['_'.join(col).strip() for col in non_saleable_return_pivot.columns.values]
non_saleable_return_pivot.reset_index(inplace=True)



non_saleable_return_pivot=non_saleable_return_pivot.fillna(0)


non_saleable_return_pivot['date'] = pd.to_datetime(non_saleable_return_pivot[['year', 'month']].assign(day=1))
non_saleable_return_pivot['date'] = non_saleable_return_pivot['date'].astype('str')
non_saleable_return_pivot=non_saleable_return_pivot.drop(['year','month'],axis=1)


sc_data=pd.merge(sc_data,non_saleable_return_pivot,how='left',on=['store_id','date'])



ms_liquidation='''
select
	a."store-id",
	Extract(year from a."received-date" ) as "year",
	Extract(month from a."received-date" ) as "month",
	SUM(a."sold-qty-in-same-month"+a."sold-qty-in-next-month") as "sold-qty-m-1-ms",
	SUM(a."sold-value-in-same-month"+a."sold-value-in-next-month") as "sold-value-m-1-ms",
	SUM(a."purchase-quantity") as "purchase-quantity-m-0-ms",
	SUM(a."purchase-value") as "purchase-value-m-0-ms"
from
	(
	select
		ii."invoice-item-reference",
		i."store-id" ,
		i."received-at" as "received-date",
		coalesce (SUM(case when to_char(DATE_TRUNC('month', f."created-at"), 'YYYY-MM') =to_char(DATE_TRUNC('month', i."received-at"), 'YYYY-MM')
		then f."sold-quantity" end ),0) as "sold-qty-in-same-month",
		coalesce (SUM(case when to_char(DATE_TRUNC('month', f."created-at"), 'YYYY-MM') =to_char(date_trunc('month',add_months(date(i."received-at"),1)),'YYYY-MM')
		then f."sold-quantity" end ),0) as "sold-qty-in-next-month",
		coalesce (SUM(case when to_char(DATE_TRUNC('month', f."created-at"), 'YYYY-MM') =to_char(DATE_TRUNC('month', i."received-at"), 'YYYY-MM')
		then f."sold-value" end ),0) as "sold-value-in-same-month",
		coalesce (SUM(case when to_char(DATE_TRUNC('month', f."created-at"), 'YYYY-MM') =to_char(date_trunc('month',add_months(date(i."received-at"),1)),'YYYY-MM')
		then f."sold-value" end ),0) as "sold-value-in-next-month",
		AVG(ii."actual-quantity") as "purchase-quantity",
		AVG(ii."net-value") as "purchase-value"
	from
		"prod2-generico"."prod2-generico"."invoice-items-1" ii
	left join "prod2-generico"."prod2-generico"."invoices-1" i on
		ii."franchisee-invoice-id" = i.id
	left join (
		select
			*
		from
			(
			select
				"invoice-item-id",
				"short-book-id",
				row_number() over(partition by "invoice-item-id"
			order by
				"short-book-id" desc) as count_new
			from
				"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii ) a
		where
			a.count_new = 1 ) g on
		ii."invoice-item-reference" = g."invoice-item-id"
	left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
	left join "prod2-generico"."prod2-generico".stores s on
		i."store-id" = s.id
	left join "prod2-generico"."prod2-generico".drugs d on
		ii."drug-id" = d.id
	left join (
		select
			s."invoice-item-reference",
			s."created-at" ,
			SUM(s."net-quantity") as "sold-quantity",
			SUM(s."net-quantity" * s.ptr) as "sold-value"
		from
			"prod2-generico"."prod2-generico".sales s
		group by
			s."invoice-item-reference",
			s."created-at") f on
		(f."invoice-item-reference" = ii."invoice-item-reference" )
	where
		date(i."received-at")  >= date(date_trunc('month',date(current_date- interval '7 Months')))
		and ii."invoice-item-reference" is not null 
		and i."franchisee-invoice" = 0  and sb."auto-short" =1 and sb."patient-id" !=4480
		and s."franchisee-id" =1
	group by
		ii."invoice-item-reference" ,
		ii."drug-id" ,
		d."drug-name" ,
		i."store-id" ,
		d."type" ,
		d."company-id" ,
		i."approved-at" ,
		i."received-at" ,
		sb."created-at" ,
		sb."created-by" 
) a
group by
	1,2,3
'''



ms_liquidation = rs_db.get_df(ms_liquidation)
ms_liquidation.columns = [c.replace('-', '_') for c in ms_liquidation.columns]



ms_liquidation['date'] = pd.to_datetime(ms_liquidation[['year', 'month']].assign(day=1))
ms_liquidation['date'] = ms_liquidation['date'].astype('str')
ms_liquidation=ms_liquidation.drop(['year','month'],axis=1)



sc_data=pd.merge(sc_data,ms_liquidation,how='left',on=['store_id','date'])


lp_liquidation='''
select 
	lp."store-id",
	Extract(year from lp."received-date" ) as "year",
	Extract(month from lp."received-date" ) as "month",
	SUM(lp."sold-value-in-same-month"+lp."sold-value-in-next-month") as "sold-value-m-1-lp",
	SUM(lp."purchase-value") as "purchase-value-m-0-lp" 
from (select
	a."store-id" ,
	a."received-date" ,
	coalesce (SUM(case when to_char(DATE_TRUNC('month', b."bill-date"), 'YYYY-MM') = to_char(DATE_TRUNC('month', a."received-date"), 'YYYY-MM')
then b."lp-sales" end ),
	0) as "sold-value-in-same-month",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', b."bill-date"), 'YYYY-MM') = to_char(date_trunc('month', add_months(date(a."received-date"), 1)), 'YYYY-MM')
then b."lp-sales" end ),
	0) as "sold-value-in-next-month",
	SUM(a."lp-value-sum") as "purchase-value"
from
	"prod2-generico"."prod2-generico"."lp-liquidation" a
left join (
	select
		i."invoice-item-id" ,
		max(date(s."created-at")) as "bill-date",
		SUM(s."net-quantity" * s.ptr) as "lp-sales"
	from
		"prod2-generico"."prod2-generico".sales s
	left join "prod2-generico"."prod2-generico"."inventory-1" i on
		s."inventory-id" = i.id
	where
		date(s."created-at") >= current_date -interval '8 months'
	group by
		i."invoice-item-id" ) b on
	a."invoice-item-id" = b."invoice-item-id"
group by
	a."store-id" ,
	a."received-date") lp
group by 1,2,3
'''



lp_liquidation = rs_db.get_df(lp_liquidation)


lp_liquidation.columns = [c.replace('-', '_') for c in lp_liquidation.columns]



lp_liquidation['date'] = pd.to_datetime(lp_liquidation[['year', 'month']].assign(day=1))

lp_liquidation['date'] = lp_liquidation['date'].astype('str')


lp_liquidation=lp_liquidation.drop(['year','month'],axis=1)



sc_data=pd.merge(sc_data,lp_liquidation,how='left',on=['store_id','date'])


pr_liq='''
select
<<<<<<< HEAD
	extract(year
from
	prm."received-at") as "year",
	extract(month
from
	prm."received-at") as "month",
	prm."store-id" ,
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	and prm."net-quantity">=(prm.quantity -prm."required-quantity" )
	then (prm.quantity -prm."required-quantity" )
	when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	and prm."net-quantity"<(prm.quantity-prm."required-quantity" )
	then prm."net-quantity" 
	end ),
	0) as "sold-qty-in-same-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(date_trunc('month', add_months(date(prm."received-at"), 1)), 'YYYY-MM')
	and prm."net-quantity" >=(prm.quantity -prm."required-quantity")
	then (prm.quantity -prm."required-quantity" )
	when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(date_trunc('month', add_months(date(prm."received-at"), 1)), 'YYYY-MM')
	and prm."net-quantity" <(prm.quantity -prm."required-quantity")
	then prm."net-quantity" 
	end ),
	0) as "sold-qty-in-next-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	and prm."net-quantity" >=(prm.quantity -prm."required-quantity") 
	then (prm.quantity -prm."required-quantity") * prm."selling-rate"
	when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	and prm."net-quantity" <(prm.quantity -prm."required-quantity") 
	then (prm."net-quantity") * prm."selling-rate"
	end ),
	0) as "sold-value-in-same-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(date_trunc('month', add_months(date(prm."received-at"), 1)), 'YYYY-MM')
	and prm."net-quantity" >=(prm.quantity -prm."required-quantity")
	then (prm.quantity -prm."required-quantity") * prm."selling-rate"
	when 
	to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') = to_char(date_trunc('month', add_months(date(prm."received-at"), 1)), 'YYYY-MM')
	and prm."net-quantity" <(prm.quantity -prm."required-quantity")
	then (prm."net-quantity") * prm."selling-rate"
	end ),
	0) as "sold-value-in-next-month-pr",
	SUM(prm.quantity-prm."required-quantity") as "dc-quantity-pr-liq",
	SUM((prm.quantity-prm."required-quantity") * prm."selling-rate") as "dc-value-pr-liq"
from
	"prod2-generico"."prod2-generico"."patient-requests-metadata" prm
where
	prm."patient-request-id" is not null
	and prm."order-raised-at-dc" = 1
	and prm."store-received-ff-time" is not null
	and prm.id != 361934323
	and date(prm."pr-created-at") >= date(date_trunc('month', date(current_date- interval '7 Months')))
group by
	1,
	2,
	3
=======
	extract(year from prm."received-at") as "year",
	Extract(month from prm."received-at") as "month",
	prm."store-id" ,
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') =to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	then prm."net-quantity" end ),0) as "sold-qty-in-same-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month',prm."billed-at"), 'YYYY-MM') =to_char(date_trunc('month',add_months(date(prm."received-at"),1)),'YYYY-MM')
	then prm."net-quantity" end ),0) as "sold-qty-in-next-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') =to_char(DATE_TRUNC('month', prm."received-at"), 'YYYY-MM')
	then prm.quantity*prm."selling-rate" end ),0) as "sold-value-in-same-month-pr",
	coalesce (SUM(case when to_char(DATE_TRUNC('month', prm."billed-at"), 'YYYY-MM') =to_char(date_trunc('month',add_months(date(prm."received-at"),1)),'YYYY-MM')
	then prm.quantity*prm."selling-rate" end ),0) as "sold-value-in-next-month-pr",
	SUM(prm.quantity) as "dc-quantity-pr-liq",
	SUM(prm.quantity*prm."selling-rate") as "dc-value-pr-liq"
from
	"prod2-generico"."prod2-generico"."patient-requests-metadata" prm
where prm."patient-request-id" is  not null and prm."order-raised-at-dc" =1
and prm."store-received-ff-time" is not null
and  prm.id!=361934323 and date(prm."pr-created-at") >= date(date_trunc('month',date(current_date- interval '7 Months')))
group by 1,2,3
>>>>>>> ee45da78b8b4214f070db360930bf4e0dacf1008
'''


pr_liq = rs_db.get_df(pr_liq)
pr_liq.columns = [c.replace('-', '_') for c in pr_liq.columns]

pr_liq['date'] = pd.to_datetime(pr_liq[['year', 'month']].assign(day=1))
pr_liq['date'] = ms_liquidation['date'].astype('str')
pr_liq=pr_liq.drop(['year','month'],axis=1)

sc_data=pd.merge(sc_data,pr_liq,how='left',on=['store_id','date'])

sc_data=sc_data.fillna(0)


sc_data[['npi_quantity', 'inventory_quantity_store',  'sold_qty_m_1_ms', 'purchase_quantity_m_0_ms', 'sold_qty_in_same_month_pr',
       'sold_qty_in_next_month_pr',  'dc_quantity_pr_liq']]=sc_data[['npi_quantity','inventory_quantity_store','sold_qty_m_1_ms', 'purchase_quantity_m_0_ms', 'sold_qty_in_same_month_pr',
       'sold_qty_in_next_month_pr',  'dc_quantity_pr_liq']].astype('int')


sc_data[['npi_inventory_value_store', 'inventory_value_store',  'sold_value_m_1_ms', 'purchase_value_m_0_ms',
         'sold_value_in_same_month_pr','sold_value_in_next_month_pr',  'dc_value_pr_liq','sold_value_m_1_lp',
         'purchase-value_m_0_lp','return_net_value_DN Dispatched','return_net_value_DN Received',
         'return_net_value_Non Salable/Expiry Discarded', 'return_net_value_PDN Approved',
         'return_net_value_PDN Box Created', 'return_net_value_PDN Dispatched',
         'return_net_value_PDN Saved', 'return_net_value_PDN Settled',
         'return_net_value_S-NS Debit Note Settled',
         'return_net_value_S-NS Debit Note Transferref', 'return_net_value_Status Issue',
         'return_net_value_Store DN Saved', 'return_net_value_Store Return Saved',
         'return_net_value_Yet To create PDN'
         ]]=sc_data[['npi_inventory_value_store', 'inventory_value_store', 'sold_value_m_1_ms', 'purchase_value_m_0_ms',
             'sold_value_in_same_month_pr','sold_value_in_next_month_pr',  'dc_value_pr_liq','sold_value_m_1_lp',
            'purchase_value_m_0_lp',
              'return_net_value_DN Dispatched','return_net_value_DN Received','return_net_value_Non Salable/Expiry Discarded',
              'return_net_value_PDN Approved',
             'return_net_value_PDN Box Created', 'return_net_value_PDN Dispatched',
             'return_net_value_PDN Saved', 'return_net_value_PDN Settled',
             'return_net_value_S-NS Debit Note Settled',
             'return_net_value_S-NS Debit Note Transferref', 'return_net_value_Status Issue',
             'return_net_value_Store DN Saved', 'return_net_value_Store Return Saved',
             'return_net_value_Yet To create PDN'
             ]].astype('float')

sc_data = sc_data.drop('purchase_value_m_0_lp', axis=1)



# =============================================================================
# store info
# =============================================================================

s_info = f"""
select
	sm.id as "store-id",
	sm.store  as "store-name",
	sm."franchisee-id" ,
	sm."franchisee-name" ,
	sm.abo ,
	sm."line-manager" ,
	sm."cluster-name" ,
	sm.city ,
	sm.acquired ,
	sm."old-new-static" 
from
	"prod2-generico"."prod2-generico"."stores-master" sm
"""
store_info = rs_db.get_df(s_info)
store_info.columns = [c.replace('-', '_') for c in store_info.columns]

sc_data = pd.merge(left=sc_data,right=store_info,on=['store_id'],how='left')




sc_data.columns = [c.replace('_', '-') for c in sc_data.columns]

sc_data.columns = sc_data.columns.str.lower()


created_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

sc_data['etl-created-at']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

updated_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

sc_data['etl-updated-at']=datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")
sc_data['etl-created-by'] = 'etl-automation'
sc_data['etl-updated-by'] = 'etl-automation'


sc_data['date'] = pd.to_datetime(sc_data['date'])

sc_data['year'] = sc_data['date'].dt.year
sc_data['month'] =sc_data['date'].dt.month


truncate_query = f''' DELETE FROM "{schema_1}"."{table_name_1}" '''

rs_db.execute(truncate_query)

<<<<<<< HEAD
# writing to db

s3.write_df_to_db(df=sc_data[table_info_1['column_name']], table_name=table_name_1, db=rs_db,
                  schema=schema_1)
=======
s3.write_df_to_db(df=sc_data[table_info_1['column_name']], table_name=table_name_1, db=rs_db,
                  schema=schema_1)



















>>>>>>> ee45da78b8b4214f070db360930bf4e0dacf1008
