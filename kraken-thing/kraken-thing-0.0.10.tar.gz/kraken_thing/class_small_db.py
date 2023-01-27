

class Small_db:


    def __init__(self):

        self.db = {}


    def __len__(self):
        '''
        '''
        records = self.get()
        return len(records)


    def __iter__(self):
        '''
        '''
        for i in self.get():
            yield i

    def post(self, param1, param2, value):
        '''
        '''
        if not self.db.get(param1, None):
            self.db[param1] = {}
                
        self.db[param1][param2] = value
        
    def get(self, param1 = None, param2 = None, default = None):
        '''
        '''

        if param1 and param2:
            return self.db.get(param1, {}).get(param2, default)
        elif param1:
            records = []
            for k, v in self.db.get(param1, {}).items():
                records.append(v)
            return records
        else:
            records = []
            for k1, v1 in self.db.items():
                for k2, v2 in v1.items():
                    records.append(v2)
            return records

    def delete(self, param1 = None, param2 = None):
        '''
        '''
        if not param1 and param2:
            return

        elif not param2:
            self.db[param1] = {}

        else:
            self.db[param1].pop(param2, None)


    
    @property
    def param1(self):
        '''returns the values in param1
        '''

        return self.db.keys()

    @property
    def param2(self, param1):
        '''returns the values in param1
        '''

        return self.db.get(param1, {}).keys()