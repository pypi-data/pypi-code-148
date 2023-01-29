import logging
import os
from copy import deepcopy

import ldap

# LDAP_SERVER_URI = 'ldap://localhost:11389'
LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI', 'ldap://10.0.101.7:389')
LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', 'svc.ADreader.eSML')
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', 'xu#GnJNiPsc*kWeq2TDKQ')
# BASE_DN = os.getenv('LDAP_BASE_DN', 'OU=MZP,DC=ad,DC=mzp,DC=cz')
BASE_DN = os.getenv('LDAP_BASE_DN', 'OU=eSML,DC=ad,DC=mzp,DC=cz')
BASE_DN_GROUPS = 'OU=Groups,{}'.format(BASE_DN)
BASE_DN_USERS = 'OU=Users,{}'.format(BASE_DN)


class DirectoryException(Exception):
    """
    Chybová procedura modulu
    """
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DirectoryFactory(object, metaclass=Singleton):
    def __int__(self, uri=LDAP_SERVER_URI, bind_dn=LDAP_BIND_DN, bind_password=LDAP_BIND_PASSWORD, base_dn=BASE_DN):
        try:
            self.uri = uri
            self.bind_dn = bind_dn
            self.bind_password = bind_password
            self.base_dn = base_dn
            self.base_dn_groups = 'OU=Groups,{}'.format(self.base_dn)
            self.base_dn_users = 'OU=Users,{}'.format(self.base_dn)
            self.client = create_ldap_client(uri=self.uri, dn=self.bind_dn, password=self.bind_password)
            logging.info('DirectoryFactory created')
        except DirectoryException as e:
            logging.error('DirectoryFactory failed: {}'.format(e))

    def reset(self, uri=LDAP_SERVER_URI, bind_dn=LDAP_BIND_DN, bind_password=LDAP_BIND_PASSWORD, base_dn=BASE_DN):
        self.__int__(uri=uri, bind_dn=bind_dn, bind_password=bind_password, base_dn=base_dn)


    def get_group_raw(self, key=None):
        """Vrátí seznam skupin

        Pro klíčové slovo názvu skupiny vrací seznam odpovídajících skupin.
        Lze použít zástupné znaky. Např. '20*' nebo '*3'
        Návratová hodnota je stavová indoemace a data

        Použití:
        status, data = get_group_raw('*3')

        :param key:  Klíčové slovo pro skupinu
        :return:    status - stavová informace (int). 101, pokud OK
                    data - seznam (list) tuplů obsahujících název a vlastní data
        """
        search_filter = 'objectClass~=group'
        if key is not None:
            search_filter = '(&({})(CN={}))'.format(search_filter, key)
            # search_filter = '(&({})(CN~={}))'.format(search_filter, key)
        search_scope = ldap.SCOPE_SUBTREE
        retrieve_attributes = None
        try:
            l_search = self.client.search(self.base_dn_groups, search_scope, search_filter, retrieve_attributes)
            result_status, result_data = self.client.result(l_search)
            return result_status, result_data
        except ldap.LDAPError as e:
            raise DirectoryException('LDAPError: {}'.format(e))

    def get_user_raw(self, key=None):
        """
        Pro klíčové slovo osoby (email, jméno) vrací seznam odpovídajících osob.
        Lze použít zástupné znaky. Např. 'Sekce*' nebo '*Namestek'
        Návratová hodnota je stavová indoemace a data

        Použití:
        status, data = get_user_raw('*Namestek')

        :param key:  Klíčové slovo pro osobu
        :return:    status - stavová informace (int). 101, pokud OK
                    data - seznam (list) tuplů obsahujících název a vlastní data
        """
        search_filter = 'objectClass~=person'
        if key is not None:
            search_filter = '(&({0})(|(mail={1})(cn={1})(userPrincipalName={1})(title={1})))'.format(search_filter, key)
            # search_filter = '(&({})(mail~={}))'.format(search_filter, key)
        search_scope = ldap.SCOPE_SUBTREE
        retrieve_attributes = None
        try:
            l_search = self.client.search(self.base_dn_users, search_scope, search_filter, retrieve_attributes)
            result_status, result_data = self.client.result(l_search)
            return result_status, result_data
        except ldap.LDAPError as e:
            raise DirectoryException('LDAPError: {}'.format(e))

    def get_group(self, key=None):
        """Vrátí seznam skupin

        Pro klíčové slovo názvu skupiny vrací seznam odpovídajících skupin.
        Lze použít zástupné znaky. Např. '20*' nebo '*3'
        Návratová hodnota je seznam (list) slovníků (dict)

        :param key:  Klíčové slovo názvu skupiny
        :return:
        """
        status, data = self.get_group_raw(key=key)
        out = []
        for item in data:
            dn = item[0]
            m_from = item[1]['member']
            m_to = []
            for m in m_from:
                m_to.append(str(m, 'utf-8'))
            desc = _get_item_value_string(item[1], 'description')
            out.append({'dn': dn, 'member': m_to, 'description': desc})
        return out

    def get_user(self, key=None):
        """
        Pro klíčové slovo osoby (email, jméno) vrací seznam odpovídajících osob.
        Lze použít zástupné znaky. Např. 'Sekce*' nebo '*Namestek'
        Návratová hodnota je seznam (list) slovníků (dict)

        :param key: Klíčové slovo pro osobu
        :return:
        """
        status, data = self.get_user_raw(key=key)
        out = []
        for item in data:
            user = _user_to_dict(user_item=item)
            out.append(user)
        return out

    def get_all_users(self):
        return self.get_user()

    def get_all_groups(self):
        return self.get_group()

    def get_org_structure(self):
        """Vrátí organizační strukturu

        :return:
        """
        out = _extract_org_structure(self.get_all_users())
        return out


def create_ldap_client(uri=LDAP_SERVER_URI, dn=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD):
    """vytvoří klienta LDAP

    Vatvoří klienta LDAP serveru

    :param uri: URI serveru LDAP v podobě naoř. ldap://localhost:11389
    :type uri: str
    :param dn:  Ověřování totožnosti přístupu k serveru - uživatelské jméno nebo Bind DN
    :type dn: str
    :param password:    Ověřování totožnosti přístupu k serveru - heslo
    :type password: str
    :return:
    :rtype: ldap.ldapobject.SimpleLDAPObject
    """
    try:
        out = ldap.initialize(uri)
        out.protocol_version = ldap.VERSION3
    except ldap.SERVER_DOWN:
        raise DirectoryException('Cannot contact LDAP server: {}'.format(uri))
    try:
        out.simple_bind_s(dn, password)
    except ldap.INVALID_CREDENTIALS:
        raise DirectoryException('Invalid credentials to acces LDAP server: {}'.format(uri))
    return out


def _user_to_dict(user_item):
    dn = user_item[0]
    member = []
    if 'memberOf' in user_item[1]:
        for it in user_item[1]['memberOf']:
            member.append(str(it, 'utf-8'))
    title = _get_item_value_string(user_item[1], 'title')
    name = _get_item_value_string(user_item[1], 'displayName')
    mail = _get_item_value_string(user_item[1], 'mail')
    first_name = _get_item_value_string(user_item[1], 'givenName')
    last_name = _get_item_value_string(user_item[1], 'sn')
    division = []
    # organizace
    organization_level_0 = {
        'code': 'MZP',
        'value': _get_item_value_string(user_item[1], 'company')
    }
    division.append(organization_level_0)
    # sekce
    organization_level_1 = {
        'code': _get_item_value_string(user_item[1], 'extensionAttribute5'),
        'value': _get_item_value_string(user_item[1], 'extensionAttribute7')
    }
    if organization_level_1['code'] != '':
        division.append(organization_level_1)
    # odbor
    organization_level_2 = {
        'code': _get_item_value_string(user_item[1], 'extensionAttribute4'),
        'value': _get_item_value_string(user_item[1], 'extensionAttribute6')
    }
    if organization_level_2['code'] != '':
        division.append(organization_level_2)
    # oddělení
    organization_level_3 = {
        'code': _get_item_value_string(user_item[1], 'departmentNumber'),
        'value': _get_item_value_string(user_item[1], 'department')
    }
    if organization_level_3['code'] != '':
        division.append(organization_level_3)
    degree = _get_item_value_string(user_item[1], 'extensionAttribute8')
    out = {
        'dn': dn, 'member': member, 'title': title, 'name': name, 'username': mail, 'email': mail,
        'first_name': first_name, 'last_name': last_name, 'degree': degree, 'division': division
    }
    return out


def _extract_org_structure(user_list):
    """Extrahuje ornanizační strukturu ze seznamu uživatelů

    :param user_list: Seznam uživatelů
    :return:
    """
    org_structure = None
    for user in user_list:
        org_structure = _merge_user_to_os(user=user, org_structure=org_structure)
    return org_structure


def _merge_user_to_os(user=None, org_structure=None):
    print(user['dn'])
    tree = _get_directory_tree(user=user)
    if (org_structure is None) or ('code' not in org_structure):
        org_structure = deepcopy(tree)
        return org_structure
    l0 = deepcopy(tree)
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    if (l0 is not None) and l0['children']:
        l1 = deepcopy(l0['children'][0])
    if (l1 is not None) and l1['children']:
        l2 = deepcopy(l1['children'][0])
    if (l2 is not None) and l2['children']:
        l3 = deepcopy(l2['children'][0])
    if (l3 is not None) and l3['children']:
        l4 = deepcopy(l3['children'][0])
    os_l0 = org_structure
    os_l1 = None
    os_l2 = None
    os_l3 = None
    os_l4 = None
    if l0['code'] != os_l0['code']:
        raise DirectoryException('Organization code \"{}\"is invalid.'.format(l0['code']))
    if (os_l0 is not None) and os_l0['children'] and (l1 is not None):
        match1 = list(filter(lambda ou: ou['code'] == l1['code'], os_l0['children']))
        if bool(match1):
            os_l1 = match1[0]
    if (os_l1 is not None) and os_l1['children'] and (l2 is not None):
        match2 = list(filter(lambda ou: ou['code'] == l2['code'], os_l1['children']))
        if bool(match2):
            os_l2 = match2[0]
    if (os_l2 is not None) and os_l2['children'] and (l3 is not None):
        match3 = list(filter(lambda ou: ou['code'] == l3['code'], os_l2['children']))
        if bool(match3):
            os_l3 = match3[0]
    if (os_l3 is not None) and os_l3['children'] and (l4 is not None):
        match4 = list(filter(lambda ou: ou['code'] == l4['code'], os_l3['children']))
        if bool(match4):
            os_l4 = match4[0]
    if (os_l1 is None) and (l1 is not None):
        os_l0['children'].append(l1)
        return org_structure
    if (os_l2 is None) and (l2 is not None):
        os_l1['children'].append(l2)
        return org_structure
    if (os_l3 is None) and (l3 is not None):
        os_l2['children'].append(l3)
        return org_structure
    if (os_l4 is None) and (l4 is not None):
        os_l3['children'].append(l4)
    return org_structure


def _get_directory_tree(user):
    i = 0
    out = {}
    work = None
    parent = None
    for div in user['division']:
        if i == 0:
            out = deepcopy(div)
            parent = deepcopy(div)
            out['children'] = []
            work = out['children']
        else:
            ou = deepcopy(div)
            parent_next = deepcopy(div)
            ou['children'] = []
            ou['parent'] = deepcopy(parent)
            work.append(ou)
            work = ou['children']
            parent = parent_next
        i += 1
    return out


def _get_item_value_string(data_dict, item_name):
    if data_dict is None:
        return None
    out = ''
    if item_name in data_dict:
        out = str(data_dict[item_name][0], 'utf-8')
    return out


DIRECTORY_FACTORY = DirectoryFactory()
