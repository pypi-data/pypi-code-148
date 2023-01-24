from redissimple.rediswrapper import RedisSimple
import psycopg2

def executeSimpleTest():
    RedisSimple.set(tenant_id="123", entity_name="ENTITY", entity_id="456", data={'message': 'success'})
    print('out')
    print(RedisSimple.get(tenant_id="123", entity_name="ENTITY", entity_id="456"))
    print(RedisSimple.get(tenant_id="123", entity_name="ENTITY", entity_id="456"))

def executeQueryTest():
    connection = psycopg2.connect(host='dev-amplify.crbsauxeopkz.us-east-1.rds.amazonaws.com', database='amplify_dev',
                                user='postgres', password='PigRaSENTErc')
    print(connection)
    cursor = connection.cursor()
    print(cursor)
    sql = "select * from config_franchisor where id = '8e79d9b6-7a9d-4c53-9462-eea081725679'"
    cursor.execute(sql)
    results = cursor.fetchall()
    #RedisSimple.set(tenant_id="123", entity_name="ENTITY", entity_id="456", data={'message': 'success'})
    print('results')
    #print(RedisSimple.get(tenant_id="123", entity_name="ENTITY", entity_id="456"))
    #print(RedisSimple.get(tenant_id="123", entity_name="ENTITY", entity_id="456"))

if __name__ == '__main__':
    executeQueryTest()