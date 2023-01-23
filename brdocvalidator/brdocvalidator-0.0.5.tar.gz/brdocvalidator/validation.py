import re
from itertools import cycle
from datetime import datetime
import bcrypt
import re

def check_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' 
    if(re.search(regex,email)):  
        #print("Valid Email")  
        return email
    else:  
        #print("Invalid Email")  
        return False
def check_doc(document):
    document = re.findall('[0-9]+', document)
    document = ''.join(document)
    if len(document)==14:
        return check_cnpj(document)
    elif len(document)==11:
        return check_cpf(document)
    return False
def check_cnpj(cnpj: str) -> bool:
    cnpj = re.findall('[0-9]+', cnpj)
    cnpj = ''.join(cnpj)
    LENGTH_CNPJ = 14
    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False
    return cnpj
def check_cpf(numbers):
    numbers = re.findall('[0-9]+', numbers)
    numbers = ''.join(numbers)

    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return numbers
def check_birth_date(data: str):
    parts = []
    if len(data) > 10:
        return False
    y = ''
    m = ''
    d = ''
    new_date = ''
    if '-' in data:
        parts = data.split('-')
        if len(parts)!= 3 :return False
        y = parts[2] if len(parts[2]) ==4 else parts[0]
        m = parts[1]
        d = parts[0] if len(parts[0])==2 else parts[2]
    elif '/' in data:
        parts = data.split('/')
        if len(parts)!= 3 :return False
        y = parts[2] if len(parts[2]) ==4 else parts[0]
        m = parts[1]
        d = parts[0] if len(parts[0])==2 else parts[2]
    elif ' ' in data:
        parts = data.split(' ')
        if len(parts)!= 3 :return False
        y = parts[2] if len(parts[2]) ==4 else parts[0]
        m = parts[1]
        d = parts[0] if len(parts[0])==2 else parts[2]
    else:
        return False
    
    ## Converto to format
    new_date = f'{y}-{m}-{d}'
    format = '%Y-%m-%d'
    
    ## Check the format
    try:
        dt_start = datetime.strptime(new_date, format)
        return new_date
    except ValueError:
        return False
def encodePass(password):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]" 
    if type(password)!= str or len(password)< 6 :
        return False
    if not re.search('[a-z]', password): 
        return False
    if not re.search('[A-Z]', password): 
        return False
    if not re.search('[0-9]', password): 
        return False
    if not re.search(special_characters, password): 
        return False
    
    password = password.encode('utf-8')
    salt = bcrypt.gensalt(10)
    passwordhashed=bcrypt.hashpw(password, salt)
    return passwordhashed   
def comparePass(old_passwd, new_passwd):
    new_passwd = new_passwd.encode('utf-8')
    if bcrypt.checkpw(new_passwd, old_passwd):
        return True
    return False
