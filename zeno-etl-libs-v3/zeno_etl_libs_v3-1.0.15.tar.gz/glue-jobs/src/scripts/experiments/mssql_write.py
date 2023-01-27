import pandas as pd
from zeno_etl_libs.db.db import MSSql

mssql = MSSql(connect_via_tunnel=False, is_ob=True)
mssql = mssql.open_connection()
bhw1 = pd.read_csv('/Users/surbhi/Downloads/ob_location_master_202301231709.csv', header='infer')
# q1 = """select * from "ob-location-master";"""
# bhw = pd.read_sql(q1, mssql)
print(type(bhw1))
cursor=mssql.cursor()
for index,row in bhw1.iterrows():
    cursor.execute("""INSERT INTO dbo.[ob-location-master]([stock-location],[store-description],[store-type],[city], [reported-year],[reported-month],[reported-day],[updated-at]) values ({},'{}','{}','{}',{},{},{},'{}');""".format(row['stock-location'],row['store-description'],row['store-type'],row['city'],row['reported-year'], row['reported-month'], row['reported-day'], row['updated-at']))
    mssql.commit()
cursor.close()
mssql.close()
