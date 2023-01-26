from . import restClient,query,digitalCommerceUtil,file,utils,objectUtil,Sobjects,traceFlag
import simplejson,logging

import colorama
import sys,time,os
import ansi2html,re
import threading,traceback
from queue import Queue

def get_apexLog_records(logUserId=None,limit=50,whereClause=None):
    where = f" where {whereClause} " if whereClause != None else ''
    where = f" where logUserId='{logUserId}' " if logUserId is not None else where

    call = query.query(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog  {where} order by LastModifiedDate desc limit {limit}")
    return call

def get_apexLog_record_and_body(logId):
    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog where Id ='{logId}' limit 1")

    if logRecords == None or len(logRecords)==0:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLogwith Id {logId}")    
    logRecord = logRecords[0]

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
    return logRecord,logbody

userCache = {}
def get_username_and_cache(Id):
    username_query = f"select Username from User where Id='{Id}'"
    if username_query not in userCache: userCache[username_query] = query.queryField(username_query) 
    return userCache[username_query]

def apexLog_record_to_string(logRecord):
    log = logRecord
    username = get_username_and_cache(log['LogUserId'])

    logLine = f"""LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']} ({username})   Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}    lenght: {log['LogLength']}    duration: {log['DurationMilliseconds']} 
LOGDATA:      startTime: {log['StartTime']}    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}
    """     
    return logLine

def do_parse_storage(pc):  
    search_dir = restClient.logFolder()

    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    fileNames = [os.path.basename(f) for f in files]
    fileNames = [f for f in fileNames if '.log' in f]

    ids = [f.split('.')[0] for f in fileNames]
    print(f"Parsing {len(ids)} files in {search_dir}")

    try:
        parse_apexlogs_by_Ids(ids,pc,printProgress=True,printNum=False)

    except KeyboardInterrupt:
        print('Interrupted')
    
    print_parsing_results(pc)

def do_parse_tail(pc):
    def auto_renew_traceFlag(traceFlagId):
        try:
            while True:
                traceFlag.update_trace_flag_incli(traceFlagId,minutes=5)
                time.sleep(10)
        except Exception as e:
            print()

    def deleteRecords(delete_queue):
        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]
            
        while True:
            logIds = delete_queue.get()

            try :
                logIdsList= list(divide_chunks(logIds,200))
                for l in logIdsList:
                    res = Sobjects.deleteMultiple('ApexLog',l)
                restClient.glog().debug(f"deleted records {logIds}")
                delete_queue.task_done()
            except Exception as e:
                print(logIds)
                print(e)

    timefield = "LastModifiedDate"

    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog order by {timefield} desc limit 1")
    time0 = logRecords[0][timefield] if len(logRecords) > 0 else None
    timez = time0.split('.')[0] + "Z" if time0 != None else '2000-12-12T17:19:35Z'

    delete_queue= None
    restClient.glog().debug(f"deleteLogs-->{pc['deleteLogs']}")

    if (pc['deleteLogs'] or pc['auto']) and pc['loguser'] == None:  
        pc['loguser'] = f"username:{pc['connection']['Username']}"
    logUserId = get_loguser_id(pc['loguser']) if pc['loguser'] != None else None

    if pc['deleteLogs']==True:       
        restClient.glog().debug("Starting delete queue")
        delete_queue = Queue(maxsize=0)
        for x in range(0,1):
            threading.Thread(target=deleteRecords,args=(delete_queue,), daemon=True).start()
        restClient.glog().info(f"Auto delete Apexlog records for user {pc['loguser']} {logUserId} set to Auto")

    if pc['auto']:
       # logUserId = get_loguser_id(f"username:{pc['loguser']}") if logUserId == None else logUserId
        traceFlagId = traceFlag.set_incli_traceFlag_for_user(f"Id:{logUserId}")
        restClient.glog().info(f"TraceFlag for user {pc['loguser']} {logUserId} set to Auto")

        threading.Thread(target=auto_renew_traceFlag,args=(traceFlagId,), daemon=True).start()

    try:
        waitingPrinted = False
        procesed = []
        greater = True
        while (True):
            if greater:    where = f" {timefield} > {timez} "
            else:          where = f" {timefield} >= {timez} "

            where = f" {pc['whereClause']} and {where}" if pc['whereClause'] is not None else where
            where = f" logUserId='{logUserId}'and {where} " if logUserId is not None else where

            fields = "Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier,SystemModstamp"
            logRecords = query.queryRecords(f"Select {fields} FROM ApexLog where {where} order by {timefield} asc")
            if len(logRecords) > 0:
                waitingPrinted = False

                prelogIds = [record['Id'] for record in logRecords]
                logIds = [id for id in prelogIds if id not in procesed]
                if len(logIds) == 0:
                    greater = True
                    continue
                greater = False
                procesed.extend(logIds)

                parse_apexlogs_by_Ids(logIds=logIds,pc=pc,raiseKeyBoardInterrupt=True)

                time0 = logRecords[-1][timefield]
                timez = time0.split('.')[0] + "Z"

                if delete_queue!=None:
                    delete_queue.put(logIds)
                    restClient.glog().debug(f"{logIds} into queue...")

            elif  waitingPrinted == False:
                print()
                print(f"waiting for debug logs for user {pc['loguser']}")  if pc['loguser'] != None  else print(f"waiting for debug logs ")
                waitingPrinted = True

            time.sleep(2)
    except KeyboardInterrupt as e:
        print()
        print_parsing_results(pc)
        print("Terminating -tail..., cleaning up")
        traceFlag.update_trace_flag_incli(traceFlagId,minutes=1,start=-15)
        if delete_queue != None: 
            while delete_queue.empty()==False:    time.sleep(1)
        print('Terminated')
        return

def do_parse_logs_lastN(pc):
    whereClause = pc['whereClause']
    loguser = pc['loguser']
    lastN = pc['lastN']

    where = f" where {whereClause} " if whereClause is not None else ''
    where = f" where logUserId='{get_loguser_id(loguser)}' " if loguser is not None else where

    if lastN == None: lastN = 1
    q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
    logIds = query.queryFieldList(q)
    if logIds == None or len(logIds)==0:   utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)

    parse_apexlogs_by_Ids(logIds,pc)
    print_parsing_results(pc)

def do_parse_from_file(parseContext):
    parseContext['body'] = file.read(parseContext['filepath'])
    parseContext['operation'] = 'parsefile'
    name = os.path.basename(parseContext['filepath']).split('.')[0]
    parseContext['logId']=name
    context =  parse_apexlog_body(parseContext)
    print_parsed_lines_to_output(parseContext)
    return context

def do_parse_logId(logId,parseContext):
    set_apexlog_body_in_pc(parseContext)
    context =  parse_apexlog_body(parseContext)
    print_parsed_lines_to_output(parseContext)

    return context

def parse_apexlogs_by_Ids(logIds,pc,raiseKeyBoardInterrupt=False,printProgress=False,threads=10,printNum=True):
    def readBody(q):
      while True:
        Id = q.get()
        get_apexLog_body_from_file_or_db(Id)
        restClient.glog().debug(f"Read body for Id {Id}")
        q.task_done()

    if 'total_parsed'       not in pc:   pc['total_parsed'] = 0
    if 'parsed_Id_status'   not in pc:   pc['parsed_Id_status'] = []
    if 'errors' not in pc:   pc['errors'] = []
    if 'queue'  not in pc:   pc['queue'] = None

    if threads >0 and pc['queue'] == None:
        pc['queue'] = Queue(maxsize=0)
        for x in range(0,threads):
            threading.Thread(target=readBody,args=(pc['queue'],), daemon=True).start()
    if threads>0:
        for logid in logIds:
            pc['queue'].put(logid)
            
    num = 0
    for num,logId in enumerate(logIds):
        if printProgress:
            sys.stdout.write("\r%d%%" % int(100*num/len(logIds)))
        try:
            parsed={ 'logId':logId, 'status':'ok' }
            pc['parsed_Id_status'].append(parsed)
            pc['logId'] = logId
            set_apexlog_body_in_pc(pc)
            parse_apexlog_body(pc)
            print_parsed_lines_to_output(pc)
            if printNum:    print( pc['total_parsed']+num+1)
            if pc['context']['exception'] == True:    parsed['status'] = pc['context']['exception_msg'][0:200]

        except KeyboardInterrupt:
            if raiseKeyBoardInterrupt:        raise
            break
        except utils.InCliError as e:
             parsed['status'] = f"Parse error: {e.args[0]['errorCode']}  "
             utils.printException(e)
             pc['errors'].append(e)
        except Exception as e:
            parsed['status'] = f"Unknown: {e}"
            pc['errors'].append(e)
            print(traceback.format_exc())

    pc['total_parsed'] = pc['total_parsed'] + num + 1
    
def print_parsing_results(pc):
    print()

    if 'parsed_Id_status' not in pc:
        print("No files parsed.")
        return 
    parsed = pc['parsed_Id_status']
    errors = pc['errors']

    print(f"{pc['total_parsed']} logs parsed")
    parsed = [par for par in parsed if par['status']!='ok']

    if len(parsed) == 0:  print("No errors.")
    if len(parsed)>0:
        utils.printFormated(parsed)
        errors = list({error.args[0]['errorCode']:error for error in errors}.values())
        for error in errors:    utils.printException(error)  

def get_loguser_id(loguser):
    id = Sobjects.IdF('User',loguser)
    return id if id!= None else utils.raiseException('QUERY',f"User with field {loguser} does not exist in the User Object.") 

def get_apexLog_body_from_file_or_db(logId):
    filename = f"{restClient.logFolder()}{logId}.log"

    if file.exists(filename) == True:
        body = file.read(filename)

        if len(body)==0:
            print("The file seems corrupted. Getting log from server.")
            file.delete(filename)
            return get_apexLog_body_from_file_or_db(logId)
        return None,body,filename
    else:
        logRecord,body = get_apexLog_record_and_body(logId) 
        body = apexLog_record_to_string(logRecord) + body  
        save_to_store(logId,body)
        return logRecord,body,filename

def set_apexlog_body_in_pc(pc):
    pc['logRecord'],pc['body'],pc['filepath'] = get_apexLog_body_from_file_or_db(pc['logId'])
    if pc['body'] == None :   utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')

def save_to_store(logId,body):
    filename = f"{restClient.logFolder()}{logId}.log"
    file.write(filename,body) 

def printLogRecords(loguser=None,limit=50,whereClause=None):
    logUserId = get_loguser_id(loguser) if loguser != None else None
    if loguser != None:
        print(f'Logs for user {loguser}:')
    logs = get_apexLog_records(logUserId,limit=limit,whereClause=whereClause)
    logs = utils.deleteNulls(logs,systemFields=False)
    logs1 = []
    for log in logs:
        log['LastModifiedDate'] = log['LastModifiedDate'].split('.')[0]
        log['StartTime'] = log['StartTime'].split('.')[0]
        log['LogUserId'] =  f"{log['LogUserId']} ({get_username_and_cache(log['LogUserId'])})"

        logs1.append(log)

    utils.printFormated(logs1,rename="LogLength%Len:DurationMilliseconds%ms:Application%App")
    return logs

def delta(obj,field):
    return obj[field][1] - obj[field][0] if len(obj[field]) > 1 else 0

def setTimes(context,line,obj=None,field=None,value=None,chunkNum=None,type=None):
    def addList(obj,field,val):
        if field in obj:
            obj[field].append(val)
        else:
            obj[field] = [val]

    chunks = line.split('|')

    if obj == None:
        obj = {
            'type' : type,
            'ident' : context['ident'],
            'exception' :False
        }
       
        if len(chunks)>3:  obj['Id'] = chunks[3]

    addList(obj,'lines',line)
    addList(obj,'CPUTime',context['DEF:CPU time'])
    addList(obj,'SOQLQueries',context['DEF:SOQL queries'])
    addList(obj,'cmtCPUTime',context['CMT:CPU time'])
    addList(obj,'cmtSOQLQueries',context['CMT:SOQL queries'])
    addList(obj,'totalQueries',context['totalQueries'])
    addList(obj,'time',chunks[0].split(' ')[0])
    if len(chunks)>1:  addList(obj,'timeStamp',int ((chunks[0].split('(')[1]).split(')')[0]))
    else:  addList(obj,'timeStamp',0)

    if obj['type'] is None:
        print()

    if field is not None:  obj[field] = chunks[chunkNum] if value is None else value

    if context['timeZero'] == 0:  context['timeZero'] = obj['timeStamp'][0]

    obj['elapsedTime'] = obj[f'timeStamp'][0] #- _context['timeZero']

    return obj

def createContext():
    context = {
        'totalQueries' : 0,
        'timeZero':0,
        'ident':0,
        'DEF:SOQL queries' : 0,
        'DEF:CPU time' : 0,
        'CMT:SOQL queries' : 0,
        'CMT:CPU time' : 0,
        "exception":False
    }
    context['totalQueries'] = 0
    context['timeZero'] = 0
    context['ident'] = 0
    context['DEF:SOQL queries'] = 0
    context['DEF:CPU time']=0
    context['CMT:SOQL queries'] = 0
    context['CMT:CPU time']=0
    context['exception'] = False
    context['file_exception'] = False
    context['previousElapsedTime'] = 0
    context['previousCPUTime'] = 0
    context['previousIsLimit'] = False
    context['prevTimes'] = {
        0:[0,0]
    }
    context['prevLevel'] = 0
    context['firstLineIn'] = True
    context['firstLineOut'] = True
    return context

def parse_apexlog_body(pc):
    if pc['body'] == None :  utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')

    try:
        context = createContext()
        pc['context'] = context

        logData = pc['body']
        context['lines'] = logData.splitlines()
        debugList = []

        context['parsedLines'] = debugList
        context['openItemsList'] = []

        for num,line in enumerate(context['lines']):
            chunks = line.split('|')
            context['chunks'] = chunks
            context['lenChunks'] = len(chunks)

            context['line'] = line
            context['num'] = num

            if '16994953586' in chunks[0]:
                a=1

            if context['firstLineIn'] == True:
                if 'APEX_CODE' in line:
                    context['firstLineIn'] = False
                    levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                    obj = {
                        'type':'LOGDATA',
                        'output':levels
                    }
                    debugList.append(obj)

                    continue      
                else:
                    obj = {
                        'type':'LOGDATA',
                        'output':line
                    }
                    debugList.append(obj)
                    continue

            if context['lenChunks'] == 1:     continue

            if len(chunks)>1 and chunks[1] in ['HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_BEGIN','HEAP_ALLOCATE','SYSTEM_METHOD_ENTRY','SYSTEM_METHOD_EXIT','SOQL_EXECUTE_EXPLAIN','ENTERING_MANAGED_PKG','SYSTEM_CONSTRUCTOR_ENTRY','SYSTEM_CONSTRUCTOR_EXIT']:    continue

            if '|SYSTEM_MODE_EXIT|' in line:      nop=1
            if parseVariableAssigment(context):      continue
            if parseLimits(context):     continue
            if parseUserDebug(context):  continue
            if parseUserInfo(context):   continue
        #  parseUserDebug(context)
            if parseExceptionThrown(context):   continue
            if parseSOQL(context)==True:        continue
            if parseMethod(context):            continue
            if parseDML(context):               continue
            if parseConstructor(context):       continue
            if parseCodeUnit(context):          continue
            if parseConstructor(context):       continue

            parseNamedCredentials(context)
            parseCallOutResponse(context)
            parseWfRule(context)
            parseFlow(context)
            
        if len(context['openItemsList']) > 0:
            a=1
        appendEnd(context)

        return context

    except KeyboardInterrupt as e:
        print(f"Parsing for logI {pc['logId']} interrupted.")
        raise e
    except Exception as e:
        print(f"Exception while parsing for logI {pc['logId']} ")
        raise e

def append_and_increaseIdent(context,obj,increase=True):
    context['openItemsList'].append(obj)
    if increase == True: context['ident'] = context['ident'] + 1
    context['parsedLines'].append(obj)

def decreaseIdent_pop_setFields(context,type,value,key='key',endsWith=None,decrease=True):
    obj = popFromList(context,type=type,key=key,value=value,endsWith=endsWith)
    if obj == None:
        a=1
    else:
        if decrease == True:   context['ident'] = obj['ident']
        setTimes(context,context['line'],obj)
    return obj

def parseUserInfo(context):
    if '|USER_INFO|' in context['line']:
        obj = setTimes(context,context['line'],field='output',value=context['chunks'][4],type='USER_INFO')
        context['parsedLines'].append(obj)
        return True
    return False

def appendEnd(context):
    for line in reversed(context['lines']):
        if '|' in line:
            break
    lastline = line
    obj = setTimes(context,lastline,type="END")
    obj['output'] = 'Final Limits'
    context['parsedLines'].append(obj)

def parseSOQL(context):
    line = context['line']
    chunks = context['chunks']
    if is_in_operation(context,'SOQL_EXECUTE_BEGIN'):
        obj = setTimes(context,line,type="SOQL")
        obj['query'] = chunks[4]
        obj['object'] = chunks[4].lower().split(' from ')[1].strip().split(' ')[0]
        obj['apexline'] = chunks[2][1:-1]

        soql = obj['query'].lower()
        _from = soql.split(' from ')[-1].strip()
        _from = _from.split(' ')[0]

        obj['from'] = _from
        obj['output'] = f"Select: {obj['from']} --> No SOQL_EXECUTE_END found"

        append_and_increaseIdent(context,obj,increase=False)
        return True

    if context['lenChunks']>1 and chunks[1] == 'SOQL_EXECUTE_END':
        context['totalQueries'] = context['totalQueries'] + 1
        obj = decreaseIdent_pop_setFields(context,type="SOQL",key='type',value='SOQL',decrease=False)
        obj['rows'] = chunks[3].split(':')[1]
        obj['output'] = f"Select: {obj['from']} --> {obj['rows']} rows"
        return True

    return False

def parseLimits(context):
    line = context['line']
    chunks = context['chunks'] 

    if '|LIMIT_USAGE|' in line and '|SOQL|' in line: context[f'DEF:SOQL queries'] = chunks[4]

    if '|LIMIT_USAGE_FOR_NS|' in line:
        obj = setTimes(context,line,type='LIMIT')
        obj['output'] = f"{chunks[1].lower()}  {chunks[2]}"
        context['parsedLines'].append(obj)

        limits = chunks[2]
        if limits == '(default)':         limitsNS = 'DEF:'
        elif limits == 'vlocity_cmt':     limitsNS = 'CMT:'
        else:                             limitsNS = f"{limits}:"

        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if 'SOQL queries' in nextline:
                nlchunks = nextline.split(' ')
                if int(context[f'{limitsNS}SOQL queries']) < int(nlchunks[6]):
                    context[f'{limitsNS}SOQL queries'] = nlchunks[6]
            if 'CPU time' in nextline:
                nlchunks = nextline.split(' ')

                if int(context[f'{limitsNS}CPU time']) < int(nlchunks[5]):
                    context[f'{limitsNS}CPU time'] = nlchunks[5]
            next = next + 1
            nextline = context['lines'][context['num']+next]

def parseUserDebug(context):
    line = context['line']
    chunks = context['chunks']

    if '|USER_DEBUG|' in line:
        obj = setTimes(context,line,type='DEBUG')
        obj['type'] = 'DEBUG'
        obj['subType'] = chunks[3]
        obj['string'] = chunks[4]
        obj['output'] = obj['string'] 
        if obj['subType'] == 'ERROR':
            context['exception'] = True
            context['exception_msg'] = obj['output']
        obj['apexline'] = chunks[2][1:-1]
        context['parsedLines'].append(obj)
        if context['num']<(len(context['lines'])-1):
            next = 1
            nextline = context['lines'][context['num']+next]
            while '|' not in nextline:
                obj = context['parsedLines'][-1].copy()
                context['parsedLines'].append(obj)
                obj['string'] = nextline
                obj['output'] = nextline
                next = next + 1
                nextline = context['lines'][context['num']+next]

        if '*** getCpuTime() ***' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:CPU time'] = chs[4]
        if 'CPU Time:' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:CPU time'] = chs[2]    
        if '*** getQueries() ***' in line:
            chs = chunks[4].split(' ')
            context[f'DEF:SOQL queries'] = chs[4]

        return True

    return False
def parseUserDebugX(context):
    line = context['line']
    chunks = context['chunks']

    if '|' in line:   #This is a new line always. 
        if 'debug_multiLine' in context and context['debug_multiLine'] == True:
            a=1
        context['debug_multiLine'] = False

    if '|USER_DEBUG|' in line:  context['debug_multiLine'] = True

    if 'debug_multiLine' in context and context['debug_multiLine'] == True:
        if '|' in line:
            obj = setTimes(context,line,type='DEBUG')
            obj['type'] = 'DEBUG'
            obj['subType'] = chunks[3]
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1]
            if obj['subType'] == 'ERROR':  context['file_exception']=True

        else:
            obj = context['parsedLines'][-1].copy()
            obj['string'] = line

        context['parsedLines'].append(obj)
        obj['output'] = obj['string'] 

def parseExceptionThrown(context):
    line = context['line']
    chunks = context['chunks']

    if context['lenChunks']>1 and chunks[1] == 'EXCEPTION_THROWN':
        obj = setTimes(context,line,type='EXCEPTION',field='output',value=chunks[3])
        context['exception'] = True
        context['exception_msg'] = obj['output']

        context['parsedLines'].append(obj)
        context['file_exception'] = True
        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if nextline != '':
                obj = context['parsedLines'][-1].copy()
                context['parsedLines'].append(obj)
                obj['output'] = nextline
            next = next + 1
            nextline = context['lines'][context['num']+next]
        return True

    if context['lenChunks']>1 and chunks[1] == 'FATAL_ERROR':
        obj = setTimes(context,line,type='EXCEPTION',field='output',value=chunks[2])
        context['exception'] = True
        context['exception_msg'] = obj['output']

        context['parsedLines'].append(obj)
        context['file_exception'] = True
        next = 1
        nextline = context['lines'][context['num']+next]
        while '|' not in nextline:
            if nextline != '':
                obj = context['parsedLines'][-1].copy()
                context['parsedLines'].append(obj)
                obj['output'] = nextline
            next = next + 1
            nextline = context['lines'][context['num']+next]
        return True

    return False

def is_in_operation(context,text,contains=False):
    if context['lenChunks']<2: return False
    if contains and text in context['chunks'][1]: return True
    elif context['chunks'][1] == text: return True
    return False

def parseWfRule(context):
    line = context['line']
    chunks = context['chunks'] 

    if is_in_operation(context,'WF_RULE_EVAL',contains=True):
        if 'BEGIN' in chunks[1]:
            obj = setTimes(context,line,field='output',value='Workflow',type='RULE_EVAL')
            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            decreaseIdent_pop_setFields(context,type='RULE_EVAL',key='output',value='Workflow')

    if is_in_operation(context,'WF_CRITERIA',contains=True):
        if 'BEGIN' in chunks[1]:
            obj = setTimes(context,line,type='WF_CRITERIA')
            obj['nameId'] = chunks[2]
            obj['rulename'] = chunks[3]
            obj['rulenameId'] = chunks[4]
            obj['output'] = obj['rulename']

            append_and_increaseIdent(context,obj)

        if 'END' in chunks[1]:
            obj =decreaseIdent_pop_setFields(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
            obj['result'] = chunks[2]
            obj['output'] = f"{obj['rulename']} --> {obj['result']}"
  
    if is_in_operation(context,'WF_RULE_NOT_EVALUATED'):
        obj =decreaseIdent_pop_setFields(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
        obj['output'] = f"{obj['rulename']} --> Rule Not Evaluated"

    if is_in_operation(context,'WF_ACTION'):
        obj = getFromList(context['openItemsList'],'output','Workflow',delete=False)
        obj['action'] = chunks[2]

def parseMethod(context):
    line = context['line']
    chunks = context['chunks'] 
    if context['lenChunks']>1 and 'METHOD_' in  chunks[1]:
        if len(chunks)<4:
            print(line)
            return

        operation = chunks[1]
       ## method = getMethod(line)
        method = chunks[3] if len(chunks) == 4 else chunks[4]
        if '(' in method:
            method = method.split('(')[0]

        if 'ENTRY' in operation:
            obj = setTimes(context,line,type='METHOD')
            obj['method'] = method
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
            obj['output'] = obj['method']
            context['parsedLines'].append(obj)

            if '.getInstance' in obj['method']:
                pass
            else:
                context['openItemsList'].append(obj)
                context['ident'] = context['ident'] + 1
            return True

        else:
            obj = getFromList(context['openItemsList'],'method',method)
            if obj == None:
                obj = getFromList(context['openItemsList'],'method',f"{method}",endsWith=True)
                apexline = chunks[2][1:-1]
                if obj != None and apexline != obj['apexline']:
                    obj == None
            if obj == None:
                obj = getFromList(context['openItemsList'],'method',f"{method}",startsWith=True)
                apexline = chunks[2][1:-1]
                if obj != None and apexline != obj['apexline']:
                    obj == None
            if obj is not None:
                context['ident'] = obj['ident']
                setTimes(context,line,obj)

            else:
                obj = setTimes(context,line,type='NO_ENTRY')
                obj['method'] = chunks[-1]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
                context['parsedLines'].append(obj)

            if 'method' in obj:
                obj['output']=obj['method']
            else:
                obj['output']=obj['Id']
            return True

    return False

def parseVariableAssigment(context):
    line = context['line']
    chunks = context['chunks'] 

    if 'EXP_VAR' in context and context['EXP_VAR'] == True:
        if chunks[1] == 'VARIABLE_ASSIGNMENT' and chunks[2] == '[EXTERNAL]':
            obj = setTimes(context,line,type='VAR_ASSIGN')
            obj['type'] = 'VAR_ASSIGN'
            obj['subType'] = 'EXCEPTION'
            obj['string'] = chunks[4]
            obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

            context['parsedLines'].append(obj)         
            obj['output'] = obj['string'] 

        else:   context['EXP_VAR'] = False
        return False #why False???

    if is_in_operation(context,'VARIABLE_ASSIGNMENT'):
        if len(chunks) >= 5:
            if 'ExecutionException' in chunks[4] or 'ExecutionException' in chunks[4]:
                obj = setTimes(context,line,type='VAR_ASSIGN')
                obj['type'] = 'VAR_ASSIGN'
                obj['subType'] = 'EXCEPTION'
                obj['string'] = chunks[4]
                obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

                context['parsedLines'].append(obj)
                obj['output'] = obj['string'] 

                context['EXP_VAR'] = True
        return True
    return False
def parseDML(context):
    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'DML_BEGIN'):
        obj = setTimes(context,line,type="DML")
        obj['OP'] = chunks[3]
        obj['Type'] = chunks[4]
        obj['Id'] = chunks[2]
        obj['apexline'] = chunks[2][1:-1]
        obj['output'] = f"{obj['OP']} {obj['Type']}" 
        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'DML_END'):
        decreaseIdent_pop_setFields(context,'DML',key='Id',value=chunks[2])
        return True

    return False

def parseCallOutResponse(context):
    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'CALLOUT_RESPONSE'):
        obj = setTimes(context,line,type='CALLOUT')
        obj['string'] = chunks[3]
        obj['apexline'] = chunks[2][1:-1]

        context['parsedLines'].append(obj)  
        obj['output'] = obj['string'] 

def parseConstructor(context):
    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'CONSTRUCTOR_ENTRY'):
        obj = setTimes(context,line,field='output',value=chunks[5],type='CONSTRUCTOR')
        obj['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'

        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'CONSTRUCTOR_EXIT'):
        decreaseIdent_pop_setFields(context,type='CONSTRUCTOR',key='output',value=chunks[5])
        return True

    return False

def parseCodeUnit(context):
    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'CODE_UNIT_STARTED'):
        obj = setTimes(context,line,type='CODE_UNIT')
        obj['output'] = chunks[4] if len(chunks)>4 else chunks[3]
        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'CODE_UNIT_FINISHED'):
        decreaseIdent_pop_setFields(context,'CODE_UNIT',key='output',value=chunks[2])
        return True

    return False

def parseNamedCredentials(context):
    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'NAMED_CREDENTIAL_REQUEST'):
        obj = setTimes(context,line,field='output',value=chunks[2],type='NAMED_CRD')
        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'NAMED_CREDENTIAL_RESPONSE'):
        obj = decreaseIdent_pop_setFields(context,type='NAMED_CRD',key='type',value='NAMED_CRD')
        return True

    return False

def parseFlow(context):
    line = context['line']
    chunks = context['chunks']
    debugList = context['parsedLines']

    if 1==2:
        if '|FLOW_START_INTERVIEWS_BEGINxx|' in line:
            obj = setTimes(context,line,type='FLOW_START_INTERVIEWS',field='output',value='FLOW_START_INTERVIEWS')
            append_and_increaseIdent(context,obj)

        if '|FLOW_START_INTERVIEWS_ENDxx|' in line:
            decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEWS',key='output',value='FLOW_START_INTERVIEWS')

    if is_in_operation(context,'FLOW_START_INTERVIEW_BEGIN'):
        obj = setTimes(context,line,type='FLOW_START_INTERVIEW')
        obj['interviewId'] = chunks[2]
        obj['Name'] = chunks[3]
        obj['output'] = obj['Name']
        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'FLOW_START_INTERVIEW_END'):
        interviewId = chunks[2]
        decreaseIdent_pop_setFields(context,'FLOW_START_INTERVIEW',key='interviewId',value=interviewId)
        return True

    if is_in_operation(context,'FLOW_ELEMENT_ERROR'):
        obj = setTimes(context,line,type='FLOW_ELEMENT_ERROR')
        obj['message'] = chunks[2]
        obj['elementType'] = chunks[3]
        obj['elementName'] = chunks[4]
        obj['output'] = utils.CRED+ f"{obj['message']} in {obj['elementType']}:{obj['elementName']}" + utils.CEND
        debugList.append(obj)
        context['exception'] = True
        context['exception_msg'] = obj['output']
        return True
    
    if is_in_operation(context,'FLOW_ELEMENT_BEGIN'):
        obj = setTimes(context,line,type='FLOW_ELEMENT')
        obj['interviewId'] = chunks[2]
        obj['elementType'] = chunks[3]
        obj['elementName'] = chunks[4]
        obj['output'] = f"{obj['elementType']}-{obj['elementName']}"
        append_and_increaseIdent(context,obj)
        return True

    if is_in_operation(context,'FLOW_ELEMENT_END'):
        interviewId = chunks[2]
        decreaseIdent_pop_setFields(context,'FLOW_ELEMENT',key='interviewId',value=interviewId)

    if is_in_operation(context,'FLOW_RULE_DETAIL'):
        values = {
            'type':'FLOW_ELEMENT',
            'elementType':'FlowDecision',
            'interviewId':chunks[2],
            'elementName':chunks[3]
        }
        obj = getFromDebugList(context,values)
        obj['ruleName'] = chunks[3]
        obj['result'] = chunks[4]
        obj['output'] = f"{obj['elementType']}-{obj['elementName']} -- {obj['ruleName']}->{obj['result']}"
        return True

    return False

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def print_parsed_lines_to_output(pc):
    pc['context']['parsedLines'] = processRepetition(pc['context']['parsedLines'])

    logId = pc['logId']
    toFile= pc['writeToFile'] if 'writeToFile' in pc else False

    if toFile == True:
        filename = f"{restClient.logFolder()}{logId}_ansi.txt"

        original_stdout = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f 
            print_parsed_lines(pc)
            sys.stdout = original_stdout 

        data = file.read(filename)
        html = ansi2html.Ansi2HTMLConverter().convert(data)
        filename = f"{restClient.logFolder()}{logId}.html"
        file.write(filename,html)
        print(f"Html file: {filename}")
        clean = escape_ansi(data)
        filename = f"{restClient.logFolder()}{logId}.txt"
        file.write(filename,clean)  
        print(f"Txt file: {filename}")
 
    else:
        colorama.just_fix_windows_console()
        print_parsed_lines(pc)

def print_parsed_lines(pc):
    logId = pc['logId'] if 'logId' in pc else None
    context = pc['context']
    print_only_errors = pc['print_only_errors'] if 'print_only_errors' in pc else False
    if context['exception'] == False and print_only_errors == True: return 
    print('___________________________________________________________________________________________________________________________________________________________________')
    if logId != None:  print(logId)
    print()
    if logId != None:  print(f"Parsing log Id {logId}    file: {restClient.logFolder()}{logId}.log")

    firstLines = True
    for num,parsedLine in enumerate(context['parsedLines']):
        if parsedLine['type'] == 'LOGDATA':
            print(parsedLine['output'])
            continue
        else:
            if firstLines == True:
                firstLines = False
                print()
                print()
        printLimits = pc['printLimits'] if 'printLimits' in pc else False

        if printLimits == False:
            if '*** getCpuTime() ***' in parsedLine['output']:   continue
            if '*** getQueries() ***' in parsedLine['output']:   continue
            if parsedLine['type'] == 'LIMIT':                    continue

        print_parsed_line(pc,parsedLine)    
    print()

def processRepetition(parsedLines):
    def isRep(repeatingSequences,parsedLineNum,parsedLine):
      if parsedLine['type'] not in ['METHOD','WF_CRITERIA','CONSTRUCTOR','DEBUG']:  return False,None

      for reps in repeatingSequences:
        chains = len(reps)
        sequenceStartPosition = reps[0]
        chainLenght = reps[1] - reps[0]
        sequenceLength = chains * chainLenght
        if sequenceStartPosition <= parsedLineNum <= sequenceStartPosition + sequenceLength - 1:
          if sequenceStartPosition <= parsedLineNum <= sequenceStartPosition + chainLenght-1:
            if 'output' not in parsedLine: 
                print()
            parsedLine['output'] = f"{parsedLine['output']}  *** {chains},  { parsedLineNum - sequenceStartPosition + 1 }"
            parsedLine['loop'] = chains
            
            if len(parsedLine['timeStamp']) > 1 and sequenceStartPosition <= parsedLineNum < sequenceStartPosition + chainLenght:
                total_time = 0
                for chainNum in range(0,chains):
                    pline = parsedLines[parsedLineNum+chainNum*chainLenght]
                    d = pline['timeStamp'][1] - pline['timeStamp'][0]
                    total_time = total_time + d

                parsedLine['totalLoopTime'] = total_time
 
            if len(parsedLine['timeStamp']) > 1 : 
                parsedLine['timeStamp'][1] = parsedLines[ parsedLineNum + (chains-1) * chainLenght ]['timeStamp'][1]
            return True,parsedLine
          else: return True,None

      return False,None

    for deb in parsedLines:
        if 'output' not in deb:  print()
    repeatingSequences = utils.get_repeating_sequences(parsedLines,"output")

    parsedX = []
    for parsedLineNum,parsedLine in enumerate(parsedLines):
        isrepe, obj = isRep(repeatingSequences,parsedLineNum,parsedLine)
        if isrepe == True and obj == None:   continue
        parsedX.append(parsedLine)

    return parsedX   

def getTime(line):
    chunks = line.split('|')
    return chunks[0].split(' ')[0]

def getTimeStamp(line):
    chunks = line.split('|')
    return int ((chunks[0].split('(')[1]).split(')')[0])

def emptyString(context,size,char=' ',ident=None):
    str = ''
    if ident is None:   ident = context['ident']
    length = ident * size
    for x in range(length):   str = str + char  
    return str       

def print_parsed_line(pc,d):
    context = pc['context']
    Cinit = utils.CEND

    if d['type'] == 'LIMITS':
        context['previousIsLimit'] = True
        return

    #levels
    if 'ident' not in d:
        print()
    level = d['ident']
    pcLevel = pc['level'] if 'level' in pc else None
    if pcLevel != None:
        if level > int(pc['level']):
            return

    #colors
    _type = d['type']
    if _type == 'DEBUG':
        _type = f"{d['type']}-{d['subType']}"
        Cinit = utils.CRED if d['subType'] == 'ERROR' else utils.CGREEN
    elif _type == 'VAR_ASSIGN' and d['subType'] == 'EXCEPTION':  Cinit = utils.CRED
    elif _type == 'VAR_ASSIGN' and d['subType'] != 'EXCEPTION':  return
    elif d['type'] == 'EXCEPTION':  Cinit = utils.CRED
    elif d['type'] == 'SOQL':   Cinit = utils.CCYAN
    elif d['type'] == 'DML':    Cinit =  utils.CYELLOW
    elif d['type'] == 'CODE_UNIT':  Cinit =  utils.CYELLOW

    identation = f"{emptyString(context,3,' ',level)}"

    if 'output' not in d:
        print()
    val = d['output']

    if val == '':
        a = 1 #print()
    
    _apexline = d['apexline'] if 'apexline' in d else ''

 #   _totalQueriesTrace = delta(d,'totalQueries') 
 #   spacer = '_' if d['type'] == 'SOQL' else '.'
 #   _totalQueriesTrace = f"{level:2}:{emptyString(context,1,spacer,level)}{_totalQueriesTrace}" if _totalQueriesTrace >0 else ' '

    _cpuTime0 = int(d['CPUTime'][0])
    _cpuTime1 = int(d['CPUTime'][1]) if len(d['CPUTime']) >1 else ''
    _timeStamp1 = d['timeStamp'][1] if len(d['timeStamp'])>1 else d['timeStamp'][0]

    _totalQueries0 = d['totalQueries'][0]
    _totalQueries1 = d['totalQueries'][1] if len(d['SOQLQueries']) >1 else _totalQueries0
    _totalQueriesD = _totalQueries1-_totalQueries0

    _cpuPrevD = _cpuTime0 - int(context['previousCPUTime'])

    if level<0:
        a=1
    if level == context['prevLevel']:  _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][1]
    if level >  context['prevLevel']:  _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][context['prevLevel']][0]
    if level <  context['prevLevel']:  _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][1]

    if _elapsedPrevD <0 and '***' in d['output']:   _elapsedPrevD = d['timeStamp'][0] - context['prevTimes'][level][0]

    context['prevTimes'][level] = [d['timeStamp'][0],_timeStamp1]

    _elapsedPrevD = f"{_elapsedPrevD/1000000:.0f}"
    if _elapsedPrevD == "0":  _elapsedPrevD =''

   # _elapsedPrevD = ms(_elapsedPrevD)

    context['prevLevel'] = level

   # _exp = "!" if d['exception'] == True else ''

    _sql1 = d['SOQLQueries'][0]
    _sql2 = d['SOQLQueries'][1] if len(d['SOQLQueries'])>1 else ''
    _sqlcmt2 = d['cmtSOQLQueries'][1] if len(d['cmtSOQLQueries'])>1 else d['cmtSOQLQueries'][0]

    context['previousCPUTime'] = _cpuTime0
    context['previousElapsedTime']  = d['elapsedTime']

    _typeColor =utils. CYELLOW  if d['type'] in ['SOQL','DML','VAR_ASSIGN'] and level == 0 else ''

    if _cpuPrevD == 0 and _type != 'END':
        _cpuPrevD = ''
        _cpuTime0 = ''

    if _totalQueriesD ==0: _totalQueriesD = ''
    if _totalQueries1 ==0: _totalQueries1 = ''

  #  Qmct_estimate = _totalQueries0 - _sql1
    Qmct_estimate = 0
    if _sql2 ==0:  _sql2=''
    if _sqlcmt2==0: _sqlcmt2=''
    _delta = f"{delta(d,'timeStamp')/1000000:.0f}"
    if 'totalLoopTime' in d:
        _delta = f"{ d['totalLoopTime']/1000000:.0f}"

    if _delta == "0":  _delta =''
    if _type == 'END':
        _sql2 = d['SOQLQueries'][0]
        _cpuTime0 = d['CPUTime'][0]
        _sqlcmt2 = d['cmtSOQLQueries'][0]

    if context['firstLineOut'] == True:
        valname = f"{'wait':>5}       time query "
        print(f"{'time(ms)':10}|{'time1(ns)':12}|{'time2(ns)':12}|{'Qt':4}|{'cpuD':6}|{'CPUin':6}|{'Q':3}|{'Qcm':3}|{'Q-e':3}|{'type':21}|{'line':4}|{valname:50}")
        context['firstLineOut'] = False

    val = utils.CFAINT +f"{_elapsedPrevD:>5}{identation}{_delta:>10}"+utils.CDARK_GRAY+f"{_totalQueriesD:>3}" +utils.CEND + Cinit +f"    {val}"

    if _type not in ['EXCEPTION','DEBUG-ERROR']:     val = val[:150]
    if _type == 'DEBUG-ERROR':
        a=1
    time_ms = f"{d['elapsedTime']/1000000:.0f}"
    print(f"{time_ms:>10}|{d['timeStamp'][0]:12}|{_timeStamp1:12}|{_totalQueries0:4}|{_cpuPrevD:6}|{_cpuTime0:>6}|{_sql1:>3}|{_sqlcmt2:>3}|{(Qmct_estimate):>3}|{_typeColor}{_type:21}{utils.CEND}|{_apexline:>4}|{val:50}"+utils.CEND)

def ms(val):
    return f"{val/1000000:5.0f}"

def popFromList(context,type,value,key='key',endsWith=False):
    openItemsList = context['openItemsList']
    try:
        for i,obj in enumerate(openItemsList):
            if obj['type'] == type:
                if endsWith == True:
                    if key not in obj:      continue
                    if obj[key].endswith(value) or obj[key].startswith(value):
                        openItemsList.pop(i)
                        return obj    
                else:
                    if key not in obj:     continue
                    if obj[key] == value:
                        openItemsList.pop(i)
                        return obj
    except Exception as e:    print(e) 

    return None

def getFromList(theList,field,value,endsWith=False,delete=True,startsWith=False):
    try:
        rvs = theList
        for i,obj in reversed(list(enumerate(rvs))):
            if field in obj:
                if startsWith == True:
                    if obj[field].startswith(value):
                        if delete == True:
                            rvs.pop(i)
                        return obj    
                if endsWith == True:
                    if obj[field].endswith(value):
                        if delete == True:
                            rvs.pop(i)
                        return obj    
                else:
                    if obj[field] == value:
                        if delete==True:
                            rvs.pop(i)
                        return obj
    except Exception as e:
        print(e) 
    return None

def getFromDebugList(context,values):
    for line in reversed(context['parsedLines']):
        for key in values.keys():
            if key not in line:
                break
            if line[key]!=values[key]:
                break
        return line
    return None    
                

