from json import dumps, dump, load
from os import listdir
from ast import literal_eval
from cryptography.fernet import Fernet
from time import sleep
#import threading  This lib is imported when server mode is initialized!
#import socket     This lib is importef when server mode or client mode is initialized!

# ajustar close do servidor para não perder dados!
# criar tag editando nas operações de crud

class ServerError(Exception):
    pass

def send_msg_sock(msg, sock, key_f=None):
    if key_f == None:
        global key_db
    else:
        key_db = key_f
    fernet = Fernet(key_db)
    sock.send(fernet.encrypt(msg.encode('utf-8')))
    sock.recv(512) # recive confirmation

def recvall(sock, key_f=None):
    if key_f == None:
        global key_db
    else:
        key_db = key_f
    fernet = Fernet(key_db)
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    sock.send(b'Confirmation message')
    return fernet.decrypt(data)

def encripta(binario):
    global key_db
    return Fernet(key_db).encrypt(binario)

def decripta(binario):
    global key_db
    return Fernet(key_db).decrypt(binario)

def messagesTreatment(client):
    global server_is_running, editando
    path_client = []
    while True:
        try:
            msg = str(recvall(client, key_db).decode('utf-8'))
            if msg[:16] == 'update-infodb;/;':
                msg = msg[16:].split(';/;')
                dici = msg[0]
                if dici[0] in ['[', '{']:
                    dici = literal_eval(dici)
                patht = literal_eval(msg[1])
                if patht == []:
                    update_infodb(dici, path_client)
                else:
                    update_infodb(dici, patht)
            elif msg[:8] == 'cdadd;/;':
                msg = msg[8:].split(';/;')
                parm = msg[0]
                if parm[0] in ['{', '[']:
                    parm = literal_eval(parm)
                if msg[1] in ['True', True]:
                    replc = True
                elif msg[1] in ['False', False]:
                    replc = False
                path_client = cdadd(parm, replc, path_client, True)
            elif msg[:13] == 'remove-infodb':
                if ';/;' in msg:
                    remove_infodb(literal_eval(msg.split(';/;')[1]))
                else:
                    remove_infodb(path_client)
            elif msg[:15] == 'salva-infodb;/;':
                msg = msg[15:]
                if msg[0] == '{':
                    salva_infodb(literal_eval(msg))
            elif msg[:6] == 'dirfdb':
                msg = msg[6:]
                if ';/;' in msg:
                    msg = literal_eval(msg[3:])
                    send_msg_sock(str(dirfdb(msg)), client)
                else:
                    send_msg_sock(str(dirfdb(path_client)), client)
            elif msg[:5] == 'cdmin':
                if msg == 'cdmin-tot':
                    path_client = []
                else:
                    path_client = path_client[:-1]
            elif msg[:13] == 'verify_key;/;':
                key_recived = msg.replace('verify_key;/;', '').encode('utf-8')
                if key_recived == key_db:
                    send_msg_sock('Autorizado', client)
                
                    break
                else:
                    send_msg_sock('Não autorizado', client)
                
                    break
                break
            elif msg[:15] == 'users-at-moment':
                send_msg_sock(f'Clients at moment: {threading.active_count()-1}', client)
            elif msg == 'shutdown-server':
                while editando:
                    pass
                server_is_running = False
                break
            elif msg == 'close':
                close()
                
                break
            elif msg == 'formata-db':
                formata_db()
            elif msg == 'pwdb':
                send_msg_sock(str(pwdb(path_client)), client)

        except:
            break



def update_infodb(valor, path_temp=None): 
    global editando
    if usemode == 'C':
        if path_temp == None:
            path_temp = []
        if type(path_temp) != list:
            raise ValueError('Path_temp must be a list!')

        send_msg_sock(f'update-infodb;/;{valor};/;{path_temp}', client)
        return
    while editando:
        pass
    editando = True
    global dados
    if path_temp == None:
        path_temp = path[:]
    elif type(path_temp) != list:
        editando = False
        raise ValueError('Path_temp must be a list!')
    temp = dados
    if len(path_temp) > 0:
        for item in path_temp[:-1]:
            if item not in temp or type(temp[item]) != dict:
                temp[item] = {}
            temp = temp[item]
        if type(valor) == dict:
            if path_temp[-1] not in temp:
                temp[path_temp[-1]] = dict()
            for k, v in valor.items():
                temp[path_temp[-1]][k] = v
        else:
            temp[path_temp[-1]] = valor
    else:
        if type(valor) != dict:
            editando = False
            raise ValueError('Value to update without path must be a dict!')
        for k, v in valor.items():
            temp[k] = v
    editando = False


    with open(nome_json, 'wb') as db:
        db.write(encripta(str(dados).encode('utf-8')))

def cdadd(p, replace_all=False, path_dir=None, just_return=False): 
    if usemode == 'C':
        if type(p) != dict:
            send_msg_sock(f'cdadd;/;{p};/;{replace_all}', client)
        return
    if just_return == False:
        global path
        tipo = type(p)
        if tipo == list:
            if replace_all:
                path = p[:]
            else:
                for item in p:
                    path.append(item)
        elif tipo == dict:
            raise ValueError("Object to add to path can't be a dict!")
        else:
            if p == '-' or p == '/':
                path = []
                return
            if '/' in p:
                p = p.split('/')
                if replace_all:
                    path = p[:]
                else:
                    for item in p:
                        path.append(item)
            else:
                if replace_all:
                    path = [p]
                else:
                    path.append(p)
    else:
        try:
            path1 = path[:]
        except:
            path1 = []
        if type(path_dir) == list:
            path1 = path_dir[:]
        tipo = type(p)
        if tipo == list:
            if replace_all:
                path1 = p[:]
            else:
                for item in p:
                    path1.append(item)
        elif tipo == dict:
            raise ValueError("Object to add to path can't be a dict!")
        else:
            if '/' in p:
                p = p.split('/')
                if replace_all:
                    path1 = p[:]
                else:
                    for item in p:
                        path1.append(item)
            else:
                if replace_all:
                    path1 = [p]
                else:
                    path1.append(p)

        return path1

def remove_infodb(path_temp=None): 
    global editando
    if usemode == 'C':
        if type(path_temp) == list:
            send_msg_sock(f'remove-infodb;/;{path_temp}', client)
        else:
            send_msg_sock('remove-infodb', client)
        return
    while editando:
        pass
    editando = True
    global dados
    if path_temp == None:
        path_temp = path[:]
    elif type(path_temp) != list:
        editando = False
        raise ValueError('Path_temp must be a list!')
    elif len(path_temp) == 0:
        editando = False
        raise ValueError('List of path cannot be empty!')
    temp = dados
    for item in path_temp[:-1]:
        if item in temp:
            temp = temp[item]
    if path_temp[-1] in temp:
        temp.pop(path_temp[-1])
    editando = False


    with open(nome_json, 'wb') as db:
        db.write(encripta(str(dados).encode('utf-8')))

def salva_infodb(valor): 
    global editando
    if type(valor) != dict:
        raise ValueError('Value of "salva_infodb" must be a dict!')
    if usemode == 'C':
        send_msg_sock(f'salva-infodb;/;{valor}', client)
        return
    while editando:
        pass
    editando = True
    global dados
    dados = valor
    with open(nome_json, 'wb') as db:
        db.write(encripta(str(dados).encode('utf-8')))
    editando = False

def formata_db(): 
    global editando
    if usemode == 'C':
        send_msg_sock('formata-db', client)
        return
    while editando:
        pass
    editando = True
    global dados
    dados = {}

    with open(nome_json, 'wb') as db:
        db.write(encripta(str(dados).encode('utf-8')))
    editando = False

def pwdb(path_temp=None): 
    if usemode == 'C':
        send_msg_sock('pwdb', client)
        return recvall(client).decode('utf-8')
    if type(path_temp) != list:
        path_temp = path[:]
    if len(path_temp) > 0:
        return '/'.join(path_temp)
    else:
        return '/'

def dirfdb(path_temp=None): 
    if usemode == 'C':
        if type(path_temp) == list:
            send_msg_sock(f'dirfdb;/;{path_temp}', client)
        else:
            send_msg_sock('dirfdb', client)
        resp = str(recvall(client).decode('utf-8'))
        if resp[0] in ['{', '[']:
            resp = literal_eval(resp)
        return resp
    if path_temp == None:
        path_temp = path[:]
    elif type(path_temp) != list:
        raise ValueError('Path_temp must be a list!')
    temp = dados
    for item in path_temp:
        if item in temp:
            temp = temp[item]
        else:
            temp = {}
    return temp

def cdmin(param=''): 
    if usemode == 'C':
        if param == 0:
            send_msg_sock(f'cdmin-tot', client)
        else:
            send_msg_sock(f'cdmin', client)
        return
    global path
    if len(path) > 0:
        if param == 0:
            path = []
        else:
            path = path[:-1]

def dirfdbp():
    print(dumps(dirfdb(), indent=4, ensure_ascii=False))

def close(): 
    global editando
    if usemode == 'C':
        send_msg_sock('close', client)
        return
    while editando:
        pass
    editando = True
    with open(nome_json, 'wb') as db:
        db.write(encripta(str(dados).encode('utf-8')))
    editando = False

def shutdown_server(): 
    if usemode == 'C':
        send_msg_sock('shutdown-server', client)
        sleep(1)
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect((ip_s, port_s))
        client1.close()

def active_clients():
    send_msg_sock('users-at-moment', client)
    return str(recvall(client).decode('utf-8'))

def inicia_db(nome_banco, key=None, modo_uso='L', ip=None, porta=None):
    global path, dados, nome_json, key_db, usemode, ip_s, port_s, server_is_running, client, threading, socket, editando
    key_db = key
    data_escrever = None
    editando = False
    nome_json = nome_banco
    usemode = modo_uso
    ip_s = ip
    port_s = porta
    path = []
    dados = {}
    server_is_running = True
    if modo_uso in ['S', 'L']:
        if nome_json in listdir():
            with open(nome_json, 'rb') as db_encripted:
                data_db = db_encripted.read()
                try:
                    data_db1 = decripta(data_db)       
                except:
                    with open(nome_json, 'wb') as db:
                        db.write(encripta(data_db))
                else:
                    data_db = data_db1
                
            dados = literal_eval(data_db.decode('utf-8'))

        else:
            if key == None:
                key_db = Fernet.generate_key()
                print(f'New database detected! The key generated is: {key_db}')
            else:
                with open(nome_json, 'wb') as db:
                    db.write(encripta(str(dados).encode('utf-8')))
    if modo_uso == 'S':

        import threading
        import socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((ip, porta))
            server.listen()
        except:
            return ServerError('Server cant be initialized!')
        while True:
            if server_is_running:
                print('Clients at moment: ', threading.active_count()-1)
                client, addr = server.accept()
                thread = threading.Thread(target=messagesTreatment, args=[client])
                thread.start()
            else:
                print('Closing server...')
                break
    elif modo_uso == 'C':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((ip, porta))
        except:
            raise ServerError('Server probably is offline!')

def inicia_localdb(path_db_local_local, key_local_db_db=b''):
    inicia_db(path_db_local_local, key_local_db_db, 'L')

def inicia_client(ip_to_connect, port_to_connect, key_to_verify):
    global socket
    import socket
    key_decoded = key_to_verify.decode('utf-8')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip_to_connect, port_to_connect))
    except:
        raise ServerError('Server probably is offline!')
    send_msg_sock(f'verify_key;/;{key_decoded}', client, key_to_verify)
    try:
        resp = recvall(client, key_to_verify).decode('utf-8')
    except:
        raise ServerError('Key is incorrect!')
    if resp == 'Autorizado':
        inicia_db('', key_to_verify, 'C', ip_to_connect, port_to_connect)
    else:
        raise ServerError('Key is incorrect!')

def inicia_host(path_db_local_local, ip_to_connect, port_to_connect, key_local_db_db=b''):
    inicia_db(path_db_local_local, key_local_db_db, 'S', ip_to_connect, port_to_connect)


#inicia_host('Teste.json', 'localhost', 7777, b'ArlK6A7JCTnkffqzGvC5IzWTsts1YtDwmBCsRGXGjUc=')
#print('All process finalized!')
