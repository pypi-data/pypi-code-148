from enum import Enum
import re
import html

class general():
    def remove_newline(_str):
        oput = None
        if _str.strip()!= '':
            oput = _str.replace('\n','').strip()
        return oput


class telegram():
    def escape_strparse_markdownv1(_string):
        output=None
        if _string.strip()!='':
            output=_string\
                    .replace('{','\\{').replace('}','\\}')\
                    .replace('[','\\[').replace(']','\\]')\
                    .replace('(','\\(').replace(')','\\)')\
                    .replace('*','\\*')\
                    .replace('~','\\~')\
                    .replace('`','\\`')\
                    .replace('_','\\_')\
                    .replace('#','\\#')\
                    .replace('+','\\+')\
                    .replace('-','\\-')\
                    .replace('=','\\=')\
                    .replace('|','\\|')\
                    .replace('.','\\.')\
                    .replace('!','\\!')
        return output

class variable_type(Enum):
    str = 'str'
    int = 'int'
    bool = 'bool'
    float = 'float'
    list = 'list'
    function = 'function'
    method = 'method'
    enumMeta = 'enum.EnumMeta'
class kwargs():
    def getValueAllowed(self, kwargs, _nameOfKwargs, _typeOfKwargs, _defaultValue = None):
        value = _defaultValue; bAllowParams = False
        if str(_nameOfKwargs) in kwargs:
            if f"'{str(_typeOfKwargs)}'" in str(type(kwargs.get(str(_nameOfKwargs)))):
                value = kwargs.get(str(_nameOfKwargs)) 
                bAllowParams = True
        return value, bAllowParams    


class listofdictionary():
    def convert_type_value_listOfDictionary(self,_dict_source, _KeyParent, _KeyChild, _NewType):
        if len(_dict_source)!=0:
            # change type value
            for dict in _dict_source: 
                for dict_child in dict[str(_KeyParent)]:
                    for key, value in dict_child.items():
                        if key == str(_KeyChild):
                            dict_child[key]= _NewType(value)
        
        return _dict_source

    def sorted_listOfDictionary_inChildRange(self,_dict_source, _KeyParent, _KeyChild):
        dict_sorted = []

        if len(_dict_source)!=0:
            # change type value
            _dict_source = self.convert_type_value_listOfDictionary(_dict_source, _KeyParent, _KeyChild, int)

            # update decending of key value 
            for dict in _dict_source: 
                dict_temporary = []
                for dict_child in dict[str(_KeyParent)]:
                    dict_temporary.append(dict_child)
                update = sorted(dict_temporary, key=lambda data: -data[str(_KeyChild)])
                dict[str(_KeyParent)] = update

            # sorted
            dict_sorted = sorted(_dict_source, key=lambda data: -data[str(_KeyParent)][0][str(_KeyChild)])

            # change type value
            dict_sorted = self.convert_type_value_listOfDictionary(dict_sorted, _KeyParent, _KeyChild, str)

        return dict_sorted

    def getKeys_dictionary(self, _dicts, _numberOfKeyNeed):
        oput = ''
        if len(_dicts)!=0:
            key = list(_dicts[_numberOfKeyNeed].keys())
            oput = key[_numberOfKeyNeed]
        return oput


    def dictCollectReportProcess(self, _identifier, _position, _message, _lst_detail = []):
        identifier = ''
        position = ''
        message = ''
        detail = ''
        failed = {}
        ALLOWPARAM_1 = False

        if "'dict" in str(type(failed)):
            if str(_identifier).strip()!= '': 
                identifier = html.escape(_identifier)
                if str(_position).strip()!='': 
                    position = html.escape(_position)
                    if str(_message).strip()!='': 
                        message =  html.escape(_message)
                        ALLOWPARAM_1 = True

            if "'list'" in str(type(_lst_detail)): 
                if len(_lst_detail)!=0: detail = _lst_detail

            if ALLOWPARAM_1 == True:
                failed['identifier'] = identifier
                failed['position'] = position
                failed['message'] = str(message).replace("'", '"')
                failed['details'] = detail
            
            if len(failed) == 0 : failed.clear()

        return failed

class string():
    def getWord_searchString(self, _word, _strfind):
        word_oput=[]
        if str(_word).strip()!='' and str(_strfind).strip()!='':
            pattern = re.compile(r'{0}'.format(_strfind))
            lst_split = str(_word).strip().split(' ')
            if len(lst_split)!=0:
                for idx, wSplit in enumerate(lst_split):
                    if re.search(pattern, wSplit):
                        data = {}
                        data[idx] = wSplit
                        word_oput.append(data)
        return word_oput

