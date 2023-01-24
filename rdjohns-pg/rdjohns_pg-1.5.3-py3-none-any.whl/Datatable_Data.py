#******************************************************************************************************************************************
#*******************                                                                                                    *******************
#*******************                        Créer le 23-09-2022 Par Rakotonindriana Johns David                         *******************
#*******************                                                                                                    *******************
#******************************************************************************************************************************************
from django.db import models
from .InsertComand import Select
import pandas as pd
import json
class Datatable_Data:
    def __init__(self,params):
        self.database       = params['db']
        self.select         = params['select']
        self.from_          = params['from']
        self.column_search  = params['column_search']
        self.column_order   = params['column_order']
        self.order          = params['order']
    
    def get_json(self,request):
        request = dict(request.data)
        draw       = request['draw'] if 'draw' in request else None
        length     = request['length'][0] if 'length' in request else None
        start      = request['start'][0] if 'start' in request else None
        search     = request['search[value]'][0] if 'search[value]' in request else None

        arr = self.get_datatables(length,start,search)
        data = json.loads(arr.to_json(orient='records'))
        output = {
            "draw"            : int(draw[0]) if draw[0] else 1,
            "recordsTotal"    : self.count_all(),
            "recordsFiltered" : self.count_all(),
            "data"            : data,
        }
        return output
    def get_datatables(self, length,start,search):
        SQL = self.get_datatable_sql(search)
        if start and length:
            if length != '-1':
                SQL += " OFFSET {} LIMIT {}".format(start,length) 
        return Select(SQL )
    
    def count_all(self):
        SQL = "SELECT COUNT(*) as nb FROM ({}) as tab WHERE 1=1".format(self.from_)
        res = Select(SQL)
        if len(res)>0:
            return res['nb'][0]
        return 0
    
    def get_datatable_sql(self,search):
        if(self.from_):
            SQL = "SELECT {} FROM ({}) as tab WHERE 1=1".format(",".join(self.select),self.from_)
            inc = 0
            for item in self.column_search:
                if search:
                    if inc ==0:
                        SQL += " AND {}::TEXT ilike '%{}%'".format(item,search)
                    else:
                        SQL += " OR {}::TEXT ilike '%{}%'".format(item,search)
                    inc += 1
            
            SQL += " ORDER BY "
            ORDER = ""
            if self.order:
                for order_ in self.order:
                    concat = ''
                    if len(ORDER)==0:
                        concat = ''
                    else:
                        concat = ','
                    ORDER += "{} {} {}".format(concat,order_,self.order[order_])
            SQL +=  ORDER
            return SQL
            

    
        