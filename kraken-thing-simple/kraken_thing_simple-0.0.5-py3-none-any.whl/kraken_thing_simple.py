
import datetime
import copy
import uuid
import json

class Thing:

    def __init__(self, record_type=None, record_id=None):

        self.record = {}

        self.record_type = record_type
        self.record_id = record_id

        if not record_id:
            self.record_id == str(uuid.uuid4())


    def __str__(self):

        return str(self.record_type) + '/' + str(self.record_id)

    
    def __repr__(self):
        '''
        '''
        return json.dumps(self.dump(), indent=4, default=str)


    def __eq__(self, other):
        
        if self.record_type == other.record_type:
            if self.record_id == other.record_id:
                return True
        return False

    def set(self, key, value):
        '''
        '''
        # Convert to Thing
        if isinstance(value, dict) and '@type' in value.keys():
            value = Thing().load(value)
            
        if value:
            self.record[key] = value

    def append(self, key, value):
        '''
        '''
        
        if not value:
            return

        # Convert to Thing
        if isinstance(value, dict) and '@type' in value.keys():
            t = Thing()
            t.load(value)
            value = t

        # Deal with list
        if isinstance(value, list):
            for i in value:
                self.append(key, i)
            return
        
        current_value = self.get(key)
        
        if not current_value:
            current_value = []
            
        if not isinstance(current_value, list):
            current_value = [current_value]

        if value not in current_value:
            current_value.append(value)
            self.set(key, current_value)
            
        
    def get(self, key):
        '''
        '''
        value = self.record.get(key, None)
        
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        return value

    def load(self, record):
        '''
        '''
        for k, v in record.items():
            self.append(k, v)

    def dump(self):
        '''
        '''

        def norm_value(value):
            if isinstance(value, list):
                new_value = []
                for i in value:
                    new_value.append(norm_value(i))
                return new_value
            
            if isinstance(value, Thing):
                return value.dump()
            else:
                return value
            
        record = {}
        record['@type'] = self.record_type
        record['@id'] = self.record_id
        for k in sorted(self.record.keys()):
            v = self.get(k)
            record[k] = norm_value(v)
                
        return record


    '''properties
    ''' 
    #Name
    @property
    def name(self):
        '''
        '''
        return self.get('schema:name')

    @name.setter
    def name(self, value):
        '''
        '''
        return self.set('schema:name', value)

    # URL
    @property
    def url(self):
        '''
        '''
        return self.get('schema:url')

    @url.setter
    def url(self, value):
        '''
        '''
        return self.set('schema:url', value)

    # URL
    @property
    def email(self):
        '''
        '''
        return self.get('schema:email')

    @email.setter
    def email(self, value):
        '''
        '''
        return self.set('schema:email', value)


    #status
    @property
    def status(self):
        '''
        '''
        return self.get('schema:actionStatus')

    @status.setter
    def status(self, value):
        '''
        '''
        return self.set('schema:actionStatus', value)

    #object
    @property
    def object(self):
        '''
        '''
        return self.get('schema:object')

    @object.setter
    def object(self, value):
        '''
        '''
        return self.set('schema:object', value)

    #object
    @property
    def instrument(self):
        '''
        '''
        return self.get('schema:instrument')

    @instrument.setter
    def instrument(self, value):
        '''
        '''
        return self.set('schema:instrument', value)

    #result
    @property
    def result(self):
        '''
        '''
        return self.get('schema:result')

    @result.setter
    def result(self, value):
        '''
        '''
        return self.append('schema:result', value)
        
        
    #record_type
    @property
    def record_type(self):
        '''
        '''
        return self.get('@type')

    @record_type.setter
    def record_type(self, value):
        '''
        '''
        if value == 'schema:action':
            # action
            self.set('schema:object', Thing())
            self.set('schema:instrument', Thing())
        
        return self.set('@type', value)

    #record_id
    @property
    def record_id(self):
        '''
        '''
        return self.get('@id')

    @record_id.setter
    def record_id(self, value):
        '''
        '''
        return self.set('@id', value)




    '''calculated properties
    '''

    @property
    def duration(self):
        '''
        '''
        if not self.get('schema:startTime'):
            return None

        if not self.get('schema:endTime'):
            return (datetime.datetime.now() - self.get('schema:startTime')).total_seconds()
        else:
            return (self.get('schema:endTime') - self.get('schema:startTime') ).total_seconds()
                    
    
    
    '''Action status
    '''

    # active
    def set_active(self):
        '''
        '''
        self.set('schema:actionStatus', 'ActiveActionStatus')
        self.set('schema:startTime', datetime.datetime.now())

    def is_active(self):
        '''
        '''
        return True if self.status == 'ActiveActionStatus' else False

    # completed
    def set_completed(self):
        '''
        '''
        self.set('schema:actionStatus', 'CompletedActionStatus')
        if not self.get('schema:startTime'):
            self.set('schema:startTime', datetime.datetime.now())
        self.set('schema:endTime', datetime.datetime.now())

    def is_completed(self):
        '''
        '''
        return True if self.status == 'CompletedActionStatus' else False
        

    # failed
    def set_failed(self):
        '''
        '''
        self.set('schema:actionStatus', 'FailedActionStatus')
        if not self.get('schema:endTime'):
            self.set('schema:endTime', datetime.datetime.now())

    def is_failed(self):
        '''
        '''
        
        return True if self.status == 'FailedActionStatus' else False


    # potential
    def set_potential(self):
        '''
        '''
        self.set('schema:actionStatus', 'PotentialActionStatus')

    def is_potential(self):
        '''
        '''
        return True if self.status == 'PotentialActionStatus' else False
