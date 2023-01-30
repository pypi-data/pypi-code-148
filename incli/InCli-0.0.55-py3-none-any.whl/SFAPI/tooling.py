from . import restClient,Sobjects,utils
import simplejson

v = 'v51.0'
def query(q):
    action = f"/services/data/{v}/tooling/query/?q={q}"
    call = restClient.callAPI(action)
    checkError()

    return call

def get(sobject,id):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action)
    return call

def checkError():
    call = restClient.lastCall()['response']
    if 'serverResponse' in call:
        sr = call.split('serverResponse:')[1]
        srj = simplejson.loads(str(sr))
        utils.raiseException(srj[0]['errorCode'],srj[0]['message'])  

def post(sobject,data):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}"
    call = restClient.callAPI(action,method='post',data=data)
    checkError()
    return call

def delete(sobject,id):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action,method='delete')
    return call

def patch(sobject,id,data):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action,method='patch',data=data)
    return call

def idF(object,fieldF,multiple=False):
    chunks = fieldF.split(":")
    if len(chunks)<2:
        utils.raiseException("fieldF error",f"Not a valid fieldF name:value  {fieldF}")
    q = f"select id from {object} where {chunks[0]} = '{chunks[1]}'"
    call = query(q)   
    if len(call['records']) == 0:
        return None
    if multiple:
        return call['records']
    return call['records'][0]['Id']

def describe(sobject):
    action =f"/services/data/{v}/tooling/sobjects/{sobject}/describe/"
    call = restClient.callAPI(action)
    utils.printFormated(call['fields'],"label:name:type")
  #  for field in call['fields']:
  #      print(f"{field['label']}  {field['name']} {field['type']}")
    print()
    

#def get():
#    action = "/services/data/v51.0/tooling/sobjects/TraceFlag/"

def queryTraceFlg(q):
    q = "select id, TracedEntityId,logtype, startdate, expirationdate, debuglevelid, debuglevel.apexcode, debuglevel.visualforce from TraceFlag limit 10"
    call = query(q)
    print()
    
