#-------  spj_grader 0.3.2 ----------
# somchai.p@chula.ac.th

import psutil
import ast, dis, types
import inspect
import io, tokenize, re
import time
import json
import copy
import os
import math
import subprocess
import builtins
import traceback
from diff_match_patch import diff_match_patch # much faster than difflib.ndiff
from black import format_str, FileMode
from numpy import ndarray, array, allclose
from numbers import Number

TOP_LEVEL_STATEMENT = 'Top-Level Statements'
TEST_STUDENT_FILE = '$$_test_file_$$.py'
RESULT_STUDENT_FILE = '$$_err_stdout_kept_$$.pickle'
BUILTINS_FUNCS = {e for e in dir(__builtins__) if e.islower()}

class spjStringIO(io.StringIO):
    def __init__(self, buffer=None, maxsize=None):
        super().__init__(buffer)
        self.maxsize = maxsize
        
    def write(self, content):
        if self.maxsize <= 0: return # ignore all write
        if self.maxsize != None and self.tell()+len(content) > self.maxsize:
            r = super().write(content[:self.maxsize-self.tell()] + '...(more)')
            raise IOError(f"stdout's size exceeds {self.maxsize}")
        return super().write(content)
    
class spjCode:
    """Code object containing source code to be executed or analyzed.

    Attributes:
        src_code: (str) source code.
        extracted: (bool) status whether the code is extracted to parts
        import_stmt: (str) all import statements
        top_level_stmt: (str) all top-level statements (outside functions)
        func_source: (dict) {function_name: function source code}
        
    Typical usage example:
        c = spjCode(souce_code)
        c.exec(use_thread=True)
        f = c.get_functions()
    """    
    def __init__(self, c):
        """Initialize code object to the given src."""        
        self.src_code = str(c.rstrip())
        self.extracted = False
        self.import_stmt = None
        self.top_level_stmt = None
        self.func_source = None
        self.class_source = None
    
    def __str__(self):
        """Return the source code."""        
        return self.src_code

    def __eq__(self, rhs):
        """Test if self and rhs have the same source code."""
        return str(self) == str(rhs)

    def __add__(self, rhs):
        """Return a new code object created from self followed by rhs."""
        return spjCode(str(self) + '\n' + str(rhs))
    
    def _exec_subprocess(self, timeout=None):
        """Execute the code using subprocess.

        Args:
            timeout: in second (None -> no timeout)
        Returns:
            error message
        """
        spjUtil.write_text_file(TEST_STUDENT_FILE, '# coding=utf-8\n' + str(self))
        cmd = [sys.executable, TEST_STUDENT_FILE]
        x = subprocess.run(cmd, timeout=timeout, stderr=subprocess.PIPE)
        err = x.stderr.decode('utf-8')
        return err
        #subprocess.run(['python', TEST_STUDENT_FILE], timeout=timeout)
        #x = subprocess.run(['python', '-c', str(self)],
        #x = subprocess.run(['python', TEST_STUDENT_FILE],
        #                   timeout=timeout, capture_output=True)

    def _exec_thread(self, timeout=None):
        """Execute the code using thread.

        Args:
            timeout: in second (None -> no timeout)
        Returns:
            error message
        """        
        # stdout, stdin and open are changed
        # if thread timeout in join, the three are not restored
        saved = (builtins.open, sys.stdout, sys.stdin)
        t = spjThread(str(self))
#        t = spjProcess(str(self))
        t.start()
        t.join(timeout)
        if t.is_alive():
            t.terminate()
            t.join() # need this, wait for thread to be killed
            #time.sleep(1)
            err = f'Time-out: {timeout}s'
        else:
            err = t.get_error() # '' if no error
        builtins.open, sys.stdout, sys.stdin = saved
        if t.is_alive(): print("  can't kill thread")
        return err
        
    def exec(self, timeout=None, use_thread=True):
        """Execute the code, no changes in globals or locals.

        Args:
            timeout: in second (None -> no timeout).
            use_thread: True (use thread), False (use subprocess),
                use thread is faster than subprocess
                but may cause problem to the grader
                if the executed code consumes too much memory.
        Raises:
            any exception from executing the code or syntax error.
        """        
        if use_thread:
            err = self._exec_thread(timeout)
        else:
            err = self._exec_subprocess(timeout)
        if err:
            raise Exception(err.splitlines()[-1])
    
    def find_loop(self, comprehension=True):
        """Find locations in the code having loops.

        Args:
            comprehension: (bool) whether to include comprehension.
        Returns:
            a list of tuples (loop instruction, line number).
        """
        loops = (ast.For, ast.While, ast.AsyncFor)
        if comprehension: loops += (ast.ListComp, ast.comprehension)
        found = []
        try:
            nodes = ast.walk(ast.parse(self.src_code))
            for node in nodes:
                if isinstance(node, loops):
                    found.append((type(node).__name__, node.lineno))
        except:
            pass
        return found
    
    def find_import(self, allowable='all', prohibited=None):
        """Find locations in the code having unallowed import.

        Args:
            allowable: a list of all allowable import module names
                or 'all' to allow all modules.
            prohibited: a list of all prohibited import module names
                or None to allow all modules.
        Returns:
            a list of tuples (unallowed module name, line number).
        Typical usage example:
            results = code.find_import(allowable=['math', 'numpy'])
            results = code.find_import(prohibited=['os', 'sys'])
        """        
        prohibited = prohibited or []
        # import ??
        # from ?? import ...
        found = []
        try:
            nodes = ast.walk(ast.parse(self.src_code))
            for node in nodes:
                if isinstance(node, ast.Import):
                    for m in node.names:
                        if m.name in prohibited or \
                           allowable != 'all' and m.name not in allowable:
                            found.append((m.name, node.lineno))
                elif isinstance(node, ast.ImportFrom):
                    if node.module in prohibited or \
                       allowable != 'all' and node.module not in allowable:
                        found.append((node.module, node.lineno))
        except:
            pass
        return found

    def find_LTSD(self, LTSD='LSD'):
        """Find locations in the code using specified List/Tuple/Set/Dict.

        Args:
            LTSD: str contains letters L, T, S, and/or 'D'
                specified containers of interest.
        Returns:
            a list of tuples (instruction, line number).
        Typical usage example:
            results = code.find_LSTD(LSTD='SD') # find set and dict.
        """
        container_asttypes = []
        container_types = []
        if 'T' in LTSD:
            container_asttypes.append(ast.Tuple)
            container_types.append('tuple')
        if 'L' in LTSD:
            container_asttypes.extend([ast.List, ast.ListComp])
            container_types.append('list')
        if 'S' in LTSD:
            container_asttypes.extend([ast.Set, ast.SetComp])
            container_types.append('set')
        if 'D' in LTSD:
            container_asttypes.extend([ast.Dict, ast.DictComp])
            container_types.append('dict')
        container_asttypes = tuple(container_asttypes)
        found = []
        try:
            nodes = ast.walk(ast.parse(self.src_code))
            for node in nodes:
                if isinstance(node, container_asttypes):
                    found.append((type(node).__name__, node.lineno))
                elif isinstance(node, ast.Call) and hasattr(node.func, 'id') and \
                     node.func.id in container_types:
                    found.append((node.func.id, node.lineno))     
        except:
            pass
        return found

    def find_mcall(self, allowable='all', prohibited=None):
        """Find locations in the code using specified method calls.

        Args:
            allowable: a list of all allowable method names
                or 'all' to allow all calls.
            prohibited: a list of all prohibited method names
                or None to allow all calls.
        Returns:
            a list of tuples (instruction, line number).
        Typical usage example:
            results = code.find_mcall(allowable=['append', 'insert'])
            results = code.find_mcall(prohibited=['pop', 'remove', 'sort'])
        """        
        prohibited = prohibited or []
        found = []
        try:
            nodes = ast.walk(ast.parse(self.src_code))
            for node in nodes:
                if isinstance(node, ast.Call):
                    nf = node.func
                    if hasattr(nf, 'attr'):  # method call
                        if nf.attr in prohibited or \
                           allowable != 'all' and nf.attr not in allowable:
                            found.append((nf.attr, nf.lineno))
        except:
            pass
        return found
    
    def find_fcall(self, allowable='all', prohibited=None):
        """Find locations in the code using specified function calls.

        Args:
            allowable: a list of all allowable function names
                or 'all' to allow all calls.
            prohibited: a list of all prohibited function names
                or None to allow all calls.
        Returns:
            a list of tuples (instruction, line number).
        Typical usage example:
            results = code.find_fcall(allowable=['input', 'print', 'len'])
            results = code.find_fcall(prohibited=['map', 'sorted', 'min', 'max'])
        """        
        found = []
        prohibited = prohibited or []
        try:
            nodes = ast.walk(ast.parse(self.src_code))
            for node in nodes:
                if isinstance(node, ast.Call):
                    nf = node.func
                    if hasattr(nf, 'id'):     # function call
                        if nf.id in prohibited or \
                           allowable != 'all' and nf.id not in allowable and \
                           nf.id not in BUILTINS_FUNCS:
                            found.append((nf.id, nf.lineno))
        except:
            pass
        return found

    def bytecount(self):
        """Return bytecount of the codes and constants used.

        Returns:
            a dict {'code': bytecount of codes,
                    'const': bytecount of constants,
                    'code+const': total bytecount of codes and constants}.
            an empty dict if invalid code (compilation error).
        """           
        def nbc(c):
            nbcode = len(c.co_code)
            nconst = 0
            for e in c.co_consts:
                if isinstance(e, type(nbc.__code__)):
                    n1,n2 = nbc(e)
                    nbcode += n1
                    nconst += n2
                elif isinstance(e, str) and '.<locals>.' in e:
                    continue
                else:
                    #print('>>', e,sys.getsizeof(e))
                    nconst += sys.getsizeof(e)
            #print(c.co_name, (nbcode, nconst))
            return nbcode, nconst
        
        s = self.src_code.replace('\n','\n ')
        if s.rstrip() == '': s = ' pass'
        src = 'def _foo_():\n' + ' ' + s
        try:
            exec(src)
            n1,n2 = nbc(locals()['_foo_'].__code__)
            return {'code': n1, 'const': n2, 'code+const': n1+n2}
        except:
            return {}

#     def has_method_call(self, methods):
#         try:
#             bytecodes = list(dis.Bytecode(self.src_code))
#             bc = []
#             for inst in bytecodes:
#                 if isinstance(inst.argval, types.CodeType):
#                     bc.extend(list(dis.Bytecode(inst.argval)))
#             bytecodes.extend(bc)
#             for inst in bytecodes:
#                 if inst.opname=='LOAD_METHOD' and \
#                    inst.argval in methods:
#                     return True
#             return False
#         except:
#             return None
            
    def _extract_parts(self):
        # https://stackoverflow.com/questions/1769332
        # SPJ: extract import, functions and top-level statements
        #  stored in self.import_stmt, self.func_source, self.top_level_stmt
        
        if self.extracted: return self.func_source is not None
        self.extracted = True
        
        t = (self.src_code + '\npass').replace('\\\n', ' ')
        io_obj = io.StringIO(t)
        last_line = -1
        last_col = 0
        out = ''
        curfunc = ''
        curclass = ''
        func_source = {}
        class_source = {}
        tls = ''
        parens = []
        try:
            toks = list(tokenize.generate_tokens(io_obj.readline))
        except:
            return False
        for i,tok in enumerate(toks):
            toktype = tok[0]
            tokstr = tok[1]
            sline, scol = tok[2]
            eline, ecol = tok[3]
            ltext = tok[4]
            if sline > last_line:
                last_col = 0
            if scol > last_col:
                out += (" " * (scol - last_col))
            if tokstr and tokstr in '{[(':
                parens.append(tokstr)
            elif tokstr and tokstr in '}])':
                parens.pop()
            elif scol == 0 and len(parens)==0 and \
               toktype in (tokenize.NAME, tokenize.STRING): # found a top-level statement
                if curfunc != '':  # end of previous function
                    func_source[curfunc] = out.rstrip()
                    curfunc = ''
                elif curclass != '':
                    class_source[curclass] = out.rstrip()
                    curclass = ''
                else:
                    tls += out.rstrip() + '\n'
                if tokstr == 'def': # found a new function def
                    curfunc = toks[i+1][1]
                elif tokstr == 'class':
                    curclass = toks[i+1][1]
                out = ''
            out += tokstr
            last_col = ecol
            last_line = eline
            
        for f,code in func_source.items():
            func_source[f] = '\n'.join(l for l in code.splitlines() if l.strip())
        for c,code in class_source.items():
            class_source[c] = '\n'.join(l for l in code.splitlines() if l.strip())

        lines = tls.splitlines()
        top_level_stmt = import_stmt = ''
        for line in lines:
            if line.strip() == '': continue
            if line.split()[0] in ['from', 'import']:
                import_stmt += line + '\n'
            else:
                top_level_stmt += line + '\n'
                
        self.import_stmt = import_stmt
        self.top_level_stmt = top_level_stmt
        self.func_source = func_source
        self.class_source = class_source
        return True

#     def remove_comment(self): # not remove doc strings
#         # https://stackoverflow.com/questions/1769332
#         io_obj = io.StringIO(self.src_code)
#         out = ""
#         last_line = -1
#         last_col = 0
#         try:
#             toks = list(tokenize.generate_tokens(io_obj.readline))
#         except:
#             return self
#         for tok in toks:
#             toktype = tok[0]
#             tokstr = tok[1]
#             sline, scol = tok[2]
#             eline, ecol = tok[3]
#             ltext = tok[4]
#             if sline > last_line:
#                 last_col = 0
#             if scol > last_col:
#                 out += (" " * (scol - last_col))
#             if toktype != tokenize.COMMENT:
#                 out += tokstr
#             last_col = ecol
#             last_line = eline
#         out = '\n'.join(l for l in out.splitlines() if l.strip())
#         return spjCode(out)

    def remove_comment_doc_str(self, remove_comment=True, remove_doc_str=True):
        """Return a new code with no comment or no docstring.

        Args:
            remove_comment: True/False specifies if not to include comment.
            remove_doc_str: True/False specifies if not to include docstring.
        Returns:
            A new code with no comment or no docstring.
        """        
        # https://stackoverflow.com/questions/1769332        
        io_obj = io.StringIO(self.src_code)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        try:
            toks = list(tokenize.generate_tokens(io_obj.readline))
        except:
            return self
        for tok in toks:
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            if remove_comment and token_type == tokenize.COMMENT:
                pass
            elif remove_doc_str and token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
                    if prev_toktype != tokenize.NEWLINE:
                        #if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        out = '\n'.join(l for l in out.splitlines() if l.strip())
        return spjCode(out)

    def remove_top_level_statements(self):
        """Return a new code with no top-level statements."""
        if not self._extract_parts(): return self
        c = self.import_stmt
        c += '\n' + self.get_all_class_source() + '\n'
        for f,src in self.func_source.items():
            c += src + '\n'
        return spjCode(c)
    
    def is_empty_func(self, func_name): #, remove_doc_str=False):
        """Test if the func_name of this code is an empty function."""
        c = self.get_func_code(func_name)
#        s = str(c.remove_comment_doc_str(remove_doc_str=remove_doc_str)).strip()
        s = str(c.remove_comment_doc_str(remove_doc_str=False)).strip()

        # 'def f\n(x\n) :' -> def f(x) :\n'
        s = s.replace("\n", ' ').replace(':', ':\n').strip()
        # def whitespace+ word whitespace* ( anychar ) whitespace* :
        x = re.findall(r'def\s+\w*\s*\(.*\)\s*:', s)
        return len(x) == 1 and x[0] == s
        
    def add_pass_to_empty_funcs(self):
        """Return a new code where pass statements are inserted to all empty functions."""
        if not self._extract_parts(): return self
        c = self.import_stmt
        if len(self.class_source)>0:
            c += self.get_all_class_source() + '\n'
        for f in self.get_func_names():
            src = self.get_func_source(f)
            if self.is_empty_func(f):       #, remove_doc_str=False):
                src += '\n    pass'
            c += src + '\n'
        c += self.top_level_stmt
        return spjCode(c)

    def get_import(self):
        """Return a string of all import statements in this code."""
        if not self._extract_parts(): return ''
        return self.import_stmt

    def get_TLS(self):
        """Return a string of all top-level statements in this code."""
        if not self._extract_parts(): return ''
        return self.top_level_stmt

    def get_all_class_source(self):
        """Return source code (str) of all classes in this code."""
        if not self._extract_parts(): return ''
        src = ''
        for c, csrc in self.class_source.items():
            src += csrc + '\n'
        return src
    
    def get_func_names(self):
        """Return a list of all function names in this code."""
        if not self._extract_parts(): return []  # set() ???
        return list(self.func_source.keys())

    def get_func_source(self, func_name):
        """Return source code (str) of func_name in this code."""
        if not self._extract_parts(): return ''
        return self.func_source.get(func_name, '')
    
    def get_func_code(self, func_name):
        """Return code of func_name in this code."""
        return spjCode(self.get_func_source(func_name))

    def get_all_funcs_source(self):
        """Return source code (str) of all functions in this code."""
        if not self._extract_parts(): return ''
        src = ''
        for f, fsrc in self.func_source.items():
            src += fsrc + '\n'
        return src

    def get_func_calls(self, code):
        """Return a list of function names being called in this code."""
        io_obj = io.StringIO('\n' + str(code) + '\n')
        try:
            toks = list(tokenize.generate_tokens(io_obj.readline))
        except:
            return []
        func_calls = []
        for i in range(1,len(toks)-1):
            prev_toktype = toks[i-1][0]
            prev_tokstr = toks[i-1][1]
            toktype = toks[i][0]
            tokstr = toks[i][1]
            next_tokstr = toks[i+1][1]
            if toktype == tokenize.NAME and next_tokstr == '(' and \
               prev_tokstr not in ('def', '.'):
#               prev_toktype != tokenize.NAME and prev_tokstr != '.':
                if tokstr not in func_calls:
                    func_calls.append(tokstr)
        return func_calls

    def get_deep_func_calls(self, code, called_fn=None):
        """Return a list of function names being called including all deep calls
        in this code. (called_fn is used internally during recursion).
        """
        called_fn = called_fn or []
        src_code = str(code)
        all_funcs = self.get_func_names()
        for fn in self.get_func_calls(src_code):
            if fn in all_funcs and fn not in called_fn:
                called_fn.append(fn)
                self.get_deep_func_calls(self.get_func_source(fn), called_fn)
        return called_fn
        
    def get_code_deep_called_from(self, funcs, excluded_fcalls=None):
        """Return code of all functions and those being called.

        Args:
            funcs: a list of function names or 'all' (all functions).
            excluded_fcalls: a list of ignored function names.
        Returns:
            A code having all functions in funcs including all deep-called funcions
            excluding all function names in excluded_fcalls.
            If function name is TLS or 'Top-Level Statements',
            functions called from top-level statements are included.
        """
        excluded_fcalls = excluded_fcalls or []
        if funcs == 'all':
            allf = sorted(self.func_source.keys()) # all func names
        else:
            allf = []
            for f in funcs:
                if f == TOP_LEVEL_STATEMENT:
                    allf = self.get_deep_func_calls(self.get_TLS(), allf)
                elif f not in allf:
                    x = [g for g in self.get_deep_func_calls(self.get_func_source(f))
                           if g not in excluded_fcalls and g not in allf]
                    allf.extend([f] + x)                    
        src = ''
        for f in allf:
            src += self.get_func_source(f) + '\n'
        return spjCode(src)        

    def _reorder_class(self):
        def dedent(src):
            n = 0
            lines = src.splitlines()
            for line in lines:
                line0 = line.lstrip()
                if line0.startswith('def '):
                    n = len(line)-len(line0)
                    break
            for i in range(len(lines)):
                line0 = lines[i].lstrip()
                k = len(lines[i]) - len(line0)
                lines[i] = lines[i][min(k,n):]
            return n, '\n'.join(lines)
        def indent(n, src):
            lines = src.splitlines()
            for i in range(len(lines)):
                if len(lines[i].strip()) > 0:
                    lines[i] = ' '*n + lines[i]
            return '\n'.join(lines)

        src = ''
        for c in sorted(self.class_source.keys()):
            csrc = self.class_source[c] + '\n'
            k = csrc.find('\n')
            classdef = csrc[:k]
            n,csrc = dedent(csrc[k+1:-1])
            # bug on comment location -> remove it (TODO)
            cc = spjCode(csrc).remove_comment_doc_str(remove_comment=True)
            rsrc = str(cc.reorder(funcs='all'))
            isrc = indent(n, rsrc)
            src += classdef + '\n' + isrc + '\n'
        return src
    
    def reorder(self, funcs, excluded_fcalls=None):
        """Return a new code by reordering this code: import, class defs, func defs and TLS"""
        # functions are placed in called orders (first called, first placed)
        excluded_fcalls = excluded_fcalls or []
        if not self._extract_parts(): return self
        c = self._reorder_class()
        c += str(self.get_code_deep_called_from(funcs, excluded_fcalls))
        if funcs == 'all' or TOP_LEVEL_STATEMENT in funcs:
            if self.import_stmt:
                c = self.import_stmt + '\n' + c
            if self.top_level_stmt:
                c += '\n' + self.top_level_stmt + '\n'
        return spjCode(c)

#-------------------------------------------------------------------
import json
import pickle
import html

class spjUtil:
    @staticmethod
    def read_text_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_text_file(filename, t):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(t)
            
    @staticmethod
    def load_json(json_file):
        with open(json_file, encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_pickle(pickle_file):
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)
        
    @staticmethod
    def dump_json(data, json_file):
        with open(json_file, 'w', encoding='utf-8') as fo:
            json.dump(data, fo, indent=2, ensure_ascii=False)

    @staticmethod
    def dump_pickle(data, pickle_file):
        with open(pickle_file, 'wb') as fo:
            pickle.dump(data, fo, protocol=pickle.HIGHEST_PROTOCOL)
            
    @staticmethod
    def html_esc(t):
        #return html.escape(str(t))
        return str(t).replace('&', '&amp;')\
                     .replace('<', '&lt;')\
                     .replace('>', '&gt;')
                     
    @staticmethod
    def red(t):
        return f'<font color=red>{spjUtil.html_esc(t)}</font>'
    
    @staticmethod
    def green(t):
        return f'<font color=#00FF00>{spjUtil.html_esc(t)}</font>'

    @staticmethod
    def yellow(t):
        return f'<font color=yellow>{spjUtil.html_esc(t)}</font>'

    @staticmethod
    def file_remove(filename):
        if os.path.exists(filename):
          os.remove(filename)

    @staticmethod
    def edit_sequence(from_, to_): # from Y to X
        # [(0,original), (1,insert), (-1,delete)]
        return diff_match_patch().diff_main(from_, to_)
    
#         m = len(X); n = len(Y)
#         L = [[0]*(n+1) for i in range(m+1)]
#         for i in range(m):
#             for j in range(n):
#                 if X[i] == Y[j]:
#                     L[i][j] = L[i-1][j-1] + 1
#                 else:
#                     L[i][j] = max(L[i-1][j], L[i][j-1])
#                     
#         lcs = ''
#         i = len(X)-1; j = len(Y)-1
#         ops = []
#         while i>=0 and j>=0:
#             if X[i]==Y[j]:
#                 ops.append(('=',X[i]))
#                 i -= 1; j -= 1
#             else:
#                 if L[i][j-1] > L[i-1][j]:
#                     ops.append(('-',Y[j]))
#                     j -= 1
#                 else:
#                     ops.append(('+',X[i]))
#                     i -= 1
#         while i>=0:
#             ops.append(('+',X[i]))
#             i -= 1
#         while j>=0:                    
#             ops.append(('-',Y[j]))
#             j -= 1
#         return ops[::-1]
    
#------------------------------------------------------
import csv
import pprint
import random

class spjSubmissions:
    """Code submissions.

    Attributes:
        db: {
              'submissions': {pid: {sid: code} },
              'solutions':   {pid: {'output': [[stdout, [kept, ...],
                                               {filename:fcontent}], ...],
                                    'src': solution_src_code},
                                    'bytecount': {'code':int, 'const':int, 'code+const':int} }},
              'testsuite':   {pid: {'testfunc_names': [func_name, ...],
                                    'srccode': testsuite_src_code }},
              'results':     {pid: {sid: {
                                       'output': [[sc, err, stdout, [kept, ...],
                                                   {filename:fcontent}], ...],
                                       'bytecount': {'code':int, 'const':int, 'code+const':int},
                                       'find_loop': [...],
                                       'find_import': [...],
                                       'find_LTSD': [...],
                                       'find_mcall': [...],
                                       'find_fcall': [...],
                                         }},
              'grade_params': {param_name: param_value},
              'check_conds': {cond_name: {'args': {name:value}},
                                          'funcs': [func_name] or 'all',
                                          'deep': bool,
                                          'excluded_fcalls': [func_name]}},
              'total_score': {pid: {sid: float}},
            }        
        pid: {sid: pid}
        
    Typical usage example:
        pid = 'HW10'
        sms = spjSubmissions.from_json(pid + '_submissions.json')
        sms.remove_top_level_statements()
        sms.remove_comment_docstr(remove_comment=False, remove_docstr=True)
        sms.add_pass_to_empty_funcs()
        
        with open(pid+'_solution.py') as f:
            sol_code = f.read()
        only_ids = 'all'  # ['6430000021', '6430001221']
        sms.grade(pid, sol_code, only_ids=only_ids, verbose=True,
                  create_py=False, prohibited_imports=['os', 'sys'],
                  use_thread=True)
                  
        sms.check_import(allowable=['math', 'numpy'])
        sms.check_LTSD(LTSD='TSD', funcs=['f1', 'f2'], deep=True, excluded_fcalls=['f3'])
        sms.check_loop(comprehension=True, funcs=['f1', 'f2'], deep=True)
        sms.check_fcall(prohibited=['map', 'sorted'], funcs='all', deep=True)
        sms.check_mcall(prohibited=['sort'], funcs='all', deep=True)
        
        sms.create_testscript_file(pid)
        sms.to_pickle(pid + '.pickle', to_json=False)
        sms.to_csv(pid + '.csv')
        sms.to_html(pid + '.html',
                    only_ids='all', use_pprint=True, output_limit=1000,
                    remove_docstr=True, remove_comment=True,
                    hide_ids=False, sorted_by='id', # 'id', 'random', 'bytecount', 'bytecode'
                    show_result=True, show_solution=True, show_diff=True,
                    correct_testcases=None,  # None, [], 'all', [testfunc_names]
                   )  # show only sids whose all testcases in correct_testcases are correct. 
    """
    def __init__(self, filepath):
        """Initialize submissions to the given file.

        Args:
            filepath: json file containing {pid: {sid: src_code}}
        """  
        if filepath.endswith('.pickle'):
            db = spjUtil.load_pickle(filepath)
        elif filepath.endswith('.json'):
            db = spjUtil.load_json(filepath)
            if 'submissions' not in db:
                db = {'submissions': db}
        else:
            raise ValueError(f'unsupported file type: {submissions}')
        
        for pid, codes in db['submissions'].items():
            for sid, srccode in codes.items():
                codes[sid] = spjCode(srccode)
                    
        for k in ['results', 'solutions', 'testsuite',
                  'grade_params', 'check_conds', 'total_score']:
            if k not in db:
                db[k] = {}
        # self.db {
        #   'submissions': {pid: {sid: code} },
        #   'results':     {pid: {sid: {'output': [[sc, err, out, kept, fcontent],...],
        #                               'has_loop': [...],
        #                               '???': ???, ... }},
        #   'solutions':   {pid: {'output': [[out, kept, fcontent],...], 'src': str}},
        #   'testsuite':   {pid: ['xxx', ...],...}
        #   'total_score': {pid: {sid: float}}
        # }
        # self.pid contains pid of each sid
        self.db = db
        self.pid = {sid: pid for pid in self.db['submissions']
                                 for sid in self.db['submissions'][pid]}

    def add_total_score(self, total_score_func):
        """Compute and store total scores from grade results using total_score_func."""
        dbt = self.db['total_score'] = {}
        for pid in self.get_pids():
            dbt[pid] = {}
        for sid in self.get_sids():
            pid = self.get_pid(sid)
            dbt[pid][sid] = total_score_func(self.get_result(sid))
            # get_result returns
            # {'sid':sid, 'pid':pid,
            #  'output': [ [sc,err,stdout,kept,fcontent],...] ], 'check???': ... }            
        
    def get_total_score(self, sid):
        """Return total_score of the sid."""
        pid = self.get_pid(sid)
        return self.db['total_score'][pid][sid]
        
    #--------------------------------------------------------
    @staticmethod
    def from_json(json_file):
        """Return spjSubmissions object created from json_file
        json_file containing {pid: {sid: src_code}}."""
        return spjSubmissions(json_file)

    #--------------------------------------------------------
    def get_sol_output(self, pid):
        """Return grading output for problem pid."""        
        # [ [stdout,kept], [stdout,kept], ... ]
        return self.db['solutions'][pid]['output']
    
    def get_pids(self):
        """Return all problem ids of this submissions."""
        return self.db['submissions'].keys()

    def get_sids(self, pid=None):
        """Return all student ids having submitted code for pid, or
        return all sids if pid is None"""
        if pid != None: # return all sids of pid
            if pid not in self.db['submissions']:
                return []
            return self.db['submissions'][pid].keys()
        else:
            sids = []   # return all sids of all pids
            for pid in self.db['submissions']:
                sids.extend(self.db['submissions'][pid].keys())
            return sids

    def get_pid(self, sid):
        """Return pid of the student id or None if no sid in the submissions."""
        return self.pid[sid] if sid in self.pid else None
        
    def get_code(self, sid):
        """Return submitted src code of the student id."""
        pid = self.get_pid(sid)
        return self.db['submissions'][pid][sid]

    def get_result(self, sid):
        """Return grading result
        {'sid': sid, 'pid': pid,
         'output': [ [score, errmsg, stdout, [kepts], {filename:filecontent}], ]
         'bytecount': {'code':int, 'const':int, 'code+const':int},
         'find_loop': [...], 'find_import': [...], 'find_LTSD': [...],
         'find_mcall': [...], 'find_fcall': [...] }
        """
        pid = self.get_pid(sid)
        if pid is None: return {}
        db = self.db['results'][pid]
        if sid not in db: return {}
        result = {'sid': sid, 'pid': pid}
        result.update(db[sid])
        return result
        # {'sid':sid, 'pid':pid,
        #  'output': [ [sc,err,p1,p2,fcontent],...] ], '???': ... }

    #-------------------------------------------------------
    def remove_top_level_statements(self):
        """Remove top-level statements from all submitted codes."""
        for pid, v in self.db['submissions'].items():
            for sid, code in v.items():
                v[sid] = code.remove_top_level_statements()

    def remove_comment_doc_str(self, remove_comment=True, remove_doc_str=True):
        """Remove comment and/or docstring from all submitted codes."""
        for pid, v in self.db['submissions'].items():
            for sid, code in v.items():
                v[sid] = code.remove_comment_doc_str(remove_comment, remove_doc_str)

    def add_pass_to_empty_funcs(self):
        """Add a pass statement in every empty function."""
        for pid, v in self.db['submissions'].items():
            for sid, code in v.items():
                v[sid] = code.add_pass_to_empty_funcs()
    #---------------------------------------------------------
    # {
    #   'submissions': {pid: {sid: code} },
    #   'results':     {pid: {sid: {'output': [...],
    #                               'has_loop': [...],
    #                               '???': ???, ... }},
    def _check_cond(self, find_cond_fname, funcs, deep, excluded_fcalls, args):
        excluded_fcalls = excluded_fcalls or []
        sids_found = []
        for sid in self.get_sids():
            pid = self.get_pid(sid)
            # not all sids have results if only some ids are graded
            if pid not in self.db['results']: continue
            if sid not in self.db['results'][pid]: continue
            c = self.get_code(sid)
            if funcs == 'all':
                found = [getattr(c, find_cond_fname)(**args)]
            else:
                all_funcs = c.get_func_names()
                found = []
                for f in funcs:
                    b = []
                    if f in all_funcs:
                        if deep:
                            c1 = c.get_code_deep_called_from([f], excluded_fcalls)
                        else:
                            c1 = c.get_func_code(f)
                        b = getattr(c1, find_cond_fname)(**args)
                    found.append(b)
            self.db['results'][pid][sid][find_cond_fname] = found
            if any(len(e)>0 for e in found):
                sids_found.append(sid)
        mod_args = dict(args)
        for k,v in args.items():  # {'allowable':['not_numpy_101', 'rot90', ...]} 
            if isinstance(v, list) and len(v)>10: 
                mod_args[k] = [v[0] + '...']
        self.db['check_conds'][find_cond_fname] = {
                    'args': mod_args,
                    'funcs': funcs,
                    'deep': deep,
                    'excluded_fcalls': excluded_fcalls,
                }
        return {find_cond_fname.replace('find', 'check'): sids_found}
    
    def check_import(self, allowable='all', prohibited=None,
                     funcs='all', deep=True, excluded_fcalls=None):
        """Check and store if submitted codes import prohibited package.

        Args:
            allowable: 'all' or a list of allowable package names.
            prohibited: None or a list of prohibited package names.
            funcs: 'all' or a list of function names to be checked.
            deep: whether to deeply check called functions.
            excluded_fcalls: None of a list function names not being checked.
            
        Returns:
            a dict {check_name (str): a list of student IDs whose codes have illegal imports}.
            
        Results:
            check results are kept in self.     
        """
        return self._check_cond('find_import', funcs, deep, excluded_fcalls,
                                {'allowable':allowable, 'prohibited':prohibited})
        
    def check_loop(self, comprehension=True,
                   funcs='all', deep=True, excluded_fcalls=None):
        """Check and store if submitted codes have loop.

        Args:
            comprehension: True/False whether to include list/set/dict comprehension checks.
            funcs: 'all' or a list of function names to be checked.
            deep: whether to deeply check called functions.
            excluded_fcalls: None of a list function names not being checked.
            
        Returns:
            a dict {check_name (str): a list of student IDs whose codes have loops}.
            
        Results:
            check results are kept in self.     
        """
        return self._check_cond('find_loop', funcs, deep, excluded_fcalls,
                                {'comprehension':comprehension})

    def check_LTSD(self, LTSD='LSD',
                   funcs='all', deep=True, excluded_fcalls=None):
        """Check and store if submitted codes use list/tuple/set/dict.

        Args:
            LTSD: str contains letter L, T, S, and/or D specifying which containers to be checked.
                  e.g. 'SD' -> check if the code uses set or dict.
            funcs: 'all' or a list of function names to be checked.
            deep: whether to deeply check called functions.
            excluded_fcalls: None of a list function names not being checked.
            
        Returns:
            a dict {check_name (str): a list of student IDs whose codes use specified containers}.
            
        Results:
            check results are kept in self.     
        """
        return self._check_cond('find_LTSD', funcs, deep, excluded_fcalls,
                                {'LTSD':LTSD})

    def check_mcall(self, allowable='all', prohibited=None,
                    funcs='all', deep=True, excluded_fcalls=None):
        """Check and store if submitted codes call prohibited methods.

        Args:
            allowable: 'all' or a list of allowable method calls.
            prohibited: None or a list of prohibited method calls.
            funcs: 'all' or a list of function names to be checked.
            deep: whether to deeply check called functions.
            excluded_fcalls: None of a list function names not being checked.
            
        Returns:
            a dict {check_name (str): a list of student IDs whose codes call illegal methods}.
            
        Results:
            check results are kept in self.     

        Examples:
            sms.check_mcall(allowable=['append', 'insert']) # can call only these two.
            sms.check_mcall(prohibited=['sort']) # can call any methods except sort.    
        """
        return self._check_cond('find_mcall', funcs, deep, excluded_fcalls,
                                {'allowable':allowable, 'prohibited':prohibited})
        
    def check_fcall(self, allowable='all', prohibited=None,
                    funcs='all', deep=True, excluded_fcalls=None):
        """Check and store if submitted codes call prohibited functions.

        Args:
            allowable: 'all' or a list of allowable functions.
            prohibited: None or a list of prohibited functions.
            funcs: 'all' or a list of function names to be checked.
            deep: whether to deeply check called functions.
            excluded_fcalls: None of a list function names not being checked.
            
        Returns:
            a dict {check_name (str): a list of student IDs whose codes call illegal functions}.
            
        Results:
            check results are kept in self.     

        Examples:
            sms.check_fcall(allowable=['max', 'max']) # can call only these two.
            sms.check_fcall(prohibited=['sorted']) # can call any functions except sorted.
        """
        return self._check_cond('find_fcall', funcs, deep, excluded_fcalls,
                                {'allowable':allowable, 'prohibited':prohibited})
       
    #--------------------------------------------------------
    def grade(self, pid_prefix, solution_code, verbose=True,
              only_ids='all', create_py=False,
              ignored_ids=None, prohibited_imports=None,
              temp_dir='', use_thread=False, no_score_if_error=False):
        """Grade all submitted codes.

        Args:
            pid_prefix: problem name
            solution_code: {pid: spjCode of solution}
            verbose: True/False: show student IDs during grading
            only_ids: 'all' or a list of student IDs (str) to be graded
                      or int (randomly chosen a number of student ids to be graded)
            create_py: True/False: create .py for each grdaed submitted code (for debugging)
            ignored_ids: None or a list of student IDs not to be graded
            prohibited_imports: None or a list of illegal package names (skip grading if found)
            temp_dir: (not yet implemented) folder to be used to store temporary files during grading
            use_thread: True (use thread for faster grading),
                        False (use subprocess to avoid out of mem error)
            no_score_if_error: True/False: skip scoring if error is found
                        
        Results:
            grading results are kept in self.     
        """        
        
        def get_testsuite(pid_prefix, pid):
            if not os.path.exists(f'{pid}_testsuite.py'):
                pid = pid_prefix
            testsuite = __import__(f'{pid}_testsuite').Testsuite()
            testsuite.srccode = spjUtil.read_text_file(f'{pid}_testsuite.py')
            testsuite.solcode = solution_code[pid]
            testsuite.use_thread = use_thread
            return testsuite
            
        ignored_ids = ignored_ids or []
        prohibited_imports = prohibited_imports or []
        if temp_dir != '':
            if not temp_dir.endswith('/'):
                temp_dir += '/'
#            global TEST_STUDENT_FILE, RESULT_STUDENT_FILE
#            if TEST_STUDENT_FILE.startswith('$$'):
#                TEST_STUDENT_FILE = temp_dir + TEST_STUDENT_FILE
#            if RESULT_STUDENT_FILE.startswith('$$'):
#                RESULT_STUDENT_FILE = temp_dir + RESULT_STUDENT_FILE
        
        # {pid: {sid: {'output': [(point, err, part1, part2, fcontent), ...]
        #              'has_loop': ???, ???: ???
        #             }}
        DB_res = {}
        DB_sol = {}
        DB_testsuite = {}
        for pid in self.get_pids():
            if not pid.upper().startswith(pid_prefix.upper()): continue
            if verbose: print(pid)
            if pid not in solution_code:
                if verbose: print('>> no solution code')
                continue
            testsuite = get_testsuite(pid_prefix, pid)
            all_testscripts = testsuite.get_testscripts()
            DB_testsuite[pid] = {
                                 'testfunc_names': testsuite.get_testfunc_names(sorted_by_lineno=True),
                                 'srccode': testsuite.srccode
                                }
            DB_sol.update(self.gen_solution_DB(pid, solution_code, testsuite))
            DB_res[pid] = {}
            
            sids = []
            for sid in self.get_sids(pid):
                if sid in ignored_ids: print(sid, ' >> ignored'); continue
                if isinstance(only_ids, int) or \
                   only_ids == 'all' or sid in only_ids:
                    sids.append(sid)
            if isinstance(only_ids, int):
                random.shuffle(sids)
                sids = sids[:only_ids]
            
            for sid in sids:
                code = self.get_code(sid)
                if verbose:
                    ps = psutil.Process(os.getpid())
                    print(f'id={sid}, used-mem={ps.memory_info().rss}, #threads={ps.num_threads()}')
                
                DB_res[pid][sid] = {'output': []}
                DBR = DB_res[pid][sid]['output']
                DB_res[pid][sid]['bytecount'] = code.bytecount()
                
                illegals = code.find_import(prohibited=prohibited_imports)
                illegals = [e[0] for e in illegals]
                import_error = f'Illegal imports: {illegals}' if illegals else ''
                    
                testsuite.set_sid_pid(sid, pid)
#                for i, onecase in enumerate(testsuite.get_testscripts()):
                for i, onecase in enumerate(all_testscripts):
                    stu_err, stu_out, stu_kept, stu_fcontents = \
                        onecase.test(code) if not import_error else (import_error, '', [], {})
                    if no_score_if_error and stu_err != '':
                        sc = 0
                    else:
                        sol_out, sol_kept, sol_fcontents = DB_sol[pid]['output'][i]
                        sc = onecase.score(sol_out, sol_kept, sol_fcontents,
                                           stu_out, stu_kept, stu_fcontents)
#                    if output_limit != None:
#                        if len(stu_out) > output_limit:
#                            if verbose: print(sid, f'len(stdout) > {output_limit}');
#                            stu_out = stu_out[:output_limit] + ' ...(more)'
#                            stu_kept = [e if len(str(e)) <= output_limit else str(e)[:output_limit]+'...(more)'
#                                        for e in stu_kept]
                    DBR.append((sc, stu_err, stu_out, stu_kept, stu_fcontents))
                    
                if only_ids != 'all' and create_py: # for debugging
                    c = str(onecase.get_testcode()).rstrip()
                    spjUtil.write_text_file(pid+'_'+sid+'.py', c)
                            
        self.db['results'].update(DB_res)
        self.db['solutions'].update(DB_sol)
        self.db['testsuite'].update(DB_testsuite)
        
        argcount = self.grade.__code__.co_argcount
        varnames = self.grade.__code__.co_varnames
        params = {varnames[1]: eval(varnames[1])}    # save all param values
        for arg in varnames[3:argcount]:
            params[arg] = eval(arg)
        self.db['grade_params'] = params
        
        spjUtil.file_remove(TEST_STUDENT_FILE)
        spjUtil.file_remove(RESULT_STUDENT_FILE)
        return self.db

    def gen_solution_DB(self, pid, solution_code, testsuite):
        # solution_code -> {pid: Code object of solution}
        # pid_prefix -> numpy,  pid -> numpy00, numpy01, ...
        assert pid in solution_code
        DB_sol = {}
        DB_sol[pid] = {'output':[], 'src': str(solution_code[pid])}
        testsuite.set_sid_pid('00000', pid)
        for onecase in testsuite.get_testscripts():
            err,out,kept,fcontents = onecase.test(solution_code[pid])
            if err != '':
                print('gen_solution_DB -->', err)
                testcode = onecase.get_testcode()
                spjUtil.write_text_file('_solution_code.py', str(testcode))
                assert False, "See _solution_code.py"
            DB_sol[pid]['output'].append((out, kept, fcontents))
        DB_sol[pid]['bytecount'] = solution_code[pid].bytecount()                    
            
        return DB_sol

    #--------------------------------------------------------
    def to_pickle(self, filename, to_json=False):
        """Dump (serialize) the spjSubmissions object to filename in pickle format.

        Args:
            to_json: if True, dump in json format as well (with .json file type).
        """        
        db = copy.deepcopy(self.db)
        for pid,codes in db['submissions'].items():
            for sid in codes:
                codes[sid] = str(codes[sid]) # spjCode -> str
        spjUtil.dump_pickle(db, filename)
        if to_json:
            fn = filename[:filename.rfind('.')] + '.json'
            spjUtil.dump_json(db, fn)

    def to_csv(self, filename):
        """Write the grading results to filename in csv format."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            wrt = csv.writer(f, delimiter=',')
            DB_res = self.db['results']
            for i,pid in enumerate(DB_res):
                for j,sid in enumerate(DB_res[pid]):
                    dbr = DB_res[pid][sid]
                    if i == 0 and j == 0:
                        # add header row
                        x = []
                        for k,v in dbr.items():
                            if k == 'output': continue
                            if type(v) != list:
                                x.append(k)
                            else:
                                x.extend([k]*len(v))
                        header = ['pid','sid'] + self.db['testsuite'][pid]['testfunc_names'] + x
                        wrt.writerow(header)
                    others = []
                    for k,v in dbr.items():
                        if k == 'output': continue
                        if type(v) != list: v = [v]
                        others.extend(v)                
                    x = dbr['output']
                    flatten_results = [e for case in x for e in case]
                    one_row = [pid, int(sid)] + \
                              [e[0] for e in x] + \
                              others + \
                              flatten_results
                    wrt.writerow(one_row)
                    
    def to_html(self, filename, remove_comment=False, remove_doc_str=False,
                use_pprint=True, correct_testcases=None, output_limit=500,
                show_result=True, show_solution=True, show_diff=True,
                only_ids='all', hide_ids=False, sorted_by='id'):
        """Write the grading results to filename in html format.

        Args:
            remove_comment: if True, remove comment lines.
            remove_docstr: if True, remove docstring.
            use_pprint: if True, format the output using pprint.
            show_result: if True, show grading results.
            show_solution: if True, show solution and testsuite.
            show_diff: if True, show differences of outputs and solutions.
            correct_testcases: None or a list of testcase names to be shown.
            out_limit: the number of output chars to be shown.
            only_ids: 'all' or a list of student IDS to be shown.
            hide_ids: if True, change student IDs to sequence numbers 00001, 00002, ...
                      if False, show studend IDs as is.
                      a hiding format string, e.g. '000xxxxx00' will change
                      '6431234521' to '643xxxxx21'.
            sorted_by: 'id', 'random', 'bytebount', 'bytecode'.            
        """
        def get_solution(pid):
            dbs = self.db['solutions'][pid]
            output = [[1,'']+list(out) for out in dbs['output']] # out=(stdout,kept,fcontents)
            other = [(k,v) for k,v in dbs.items() if k not in ('output', 'src')]            
            return dbs['src'], output, other
                                
        def show_solution_testscript(pid):
            dbt = self.db['testsuite'][pid]
            sol_src, sol_output, sol_other = get_solution(pid)            
            t = add_one_sid(pid, 'Solution', spjCode(sol_src),
                             sol_output, sol_output, sol_other)
            t += f'<table border=1>{title_row("Testsuite")}'
            t += f'<tr><td><pre><code class="language-python">{spjUtil.html_esc(dbt["srccode"])}</code></pre></td>\n'
            t += '</tr></table><p>\n'
            return t
            
        def title_row(title):
            return f'<tr><td colspan="6"><font size=+2>{spjUtil.yellow(title)}</font>: {pid}</td></tr>\n'

        def get_check_detail(check):
            if check not in self.db['check_conds']: return ''
            params = self.db['check_conds'][check]
            args = {k:v for k,v in params["args"].items() if v!='all' and v!=None}
            detail = f'{check.replace("find","check")}({args})'
            if params["funcs"] != 'all':
                detail += f' in [{", ".join(params["funcs"])}]'
            if params["deep"]:
                detail += ' deep'
            if params["excluded_fcalls"] != []:
                detail += f'<br>&nbsp;&nbsp;&nbsp;exclude [{", ".join(params["excluded_fcalls"])}]'
            return detail
        
        def add_one_sid(pid, sid, code, results, sol_results, other_checks):
            dbt = self.db['testsuite'][pid]
            testfuncnames = dbt['testfunc_names']
            t = f'<table border=1>{title_row(sid)}'
            if show_result:
                xxx = 'sol' if sid.lower()[:3] == 'sol' else 'stu'
                t += '<tr style="background-color:#666666"><td>testfunc</td>'
                t += f'<td>sc</td><td>err</td><td>{xxx}_stdout</td><td>{xxx}_kept</td><td>{xxx}_fout</td></tr>\n'
                for i in range(len(testfuncnames)):
                    testfunc = testfuncnames[i]
                    r = results[i]
                    sol = sol_results[i]
                    # r = [sc, err, stu_stdout, stu_kept]
                    errtd = ' style="width:50px"' if r[1] else ''                
                    t += f'<tr><td style="width:1px">{testfunc}</td>'
                    t += f'<td style="width:1px">{round(r[0]+0.004,2)}</td>'
                    err = spjUtil.red(r[1]).replace("\n","<br>")
                    t += f'<td{errtd}>{err}</td>'
                    t += f'<td><pre>{colorize_result(sol[2], r[2])}</pre></td>'
                    kept = r[3]
                    if use_pprint:
                        kept_sol = pprint.pformat(sol[3], compact=True, width=100)
                        kept_stu = pprint.pformat(r[3], compact=True, width=100)
                    else:
                        kept_sol = str(sol[3])
                        kept_stu = str(r[3])
                    t += f'<td><pre>{colorize_result(kept_sol, kept_stu)}</pre></td>'
                    t += f'<td><pre>{file_contents(sol[4], r[4])}</pre></td></tr>\n'
                    
            for check, check_result in other_checks:
                if check.startswith('find'):
                    check = get_check_detail(check)
                    if all(len(e)==0 for e in check_result):
                        check_result = 'none'
                check_result = str(check_result)
                t += f'<tr><td colspan="6" style="background-color:#222266">{check}:'
                if len(check_result) > 100: t += '<br>&nbsp;&nbsp;'
                t += f'&nbsp;{spjUtil.green(check_result)}'
                t += '</td></tr>\n'
            if remove_comment or remove_doc_str:
                code = code.remove_comment_doc_str(remove_comment=remove_comment,
                                                   remove_doc_str=remove_doc_str)
            srccode = str(code).strip()
            t += f'<tr><td colspan="6"><pre><code class="language-python">{spjUtil.html_esc(srccode)}</code></pre></td></tr>\n'
            t += '</table><p></p>\n'
            return t

        def file_contents(fout1, fout2):
            # fout1, fout2 -> {filename: filecontent}
            fnames = set(fout1.keys()) & set(fout2.keys())
            t = []
            for fn in sorted(fnames):
                t.append('=filename: ' + fn)
                t.append(colorize_result(fout1[fn], fout2[fn]) + '\n')
            for fn in sorted(set(fout2) - fnames):
                t.append('-filename: ' + fn)
                t.append(colorize_result('', fout2[fn]) + '\n')
            for fn in sorted(set(fout1) - fnames):
                t.append('+filename: ' + fn)
                t.append(colorize_result(fout1[fn], '') + '\n')
            return '\n'.join(t)
                
        def get_sids(dbr_pid):
            # only_ids, testcases, sorted_by (from to_html's params)
            testcases = correct_testcases or []
            out = []
            for sid in dbr_pid:
                if type(only_ids) in (list, tuple) and sid in only_ids: continue
                results = dbr_pid[sid]['output']
                if testcases == 'all': testcases = list(range(len(results)))
                s = sum(results[i][0] for i in testcases)
                if s < len(testcases): continue
                out.append(sid)
            if sorted_by == 'id':
                out = sorted(out)
            elif sorted_by == 'random':
                random.shuffle(out)
            elif sorted_by == 'bytecount':
                out = sorted(out, key=lambda s:
                             dbr_pid[s]['bytecount']['code+const']
                             if dbr_pid[s]['bytecount'] != {} else math.inf)
            elif sorted_by == 'bytecode':
                out = sorted(out, key=lambda s:
                             dbr_pid[s]['bytecount']['code']
                             if dbr_pid[s]['bytecount'] != {} else math.inf)
            if isinstance(only_ids, int): out = out[:only_ids]
            return out

        def colorize_result(sol, stu):                        
            if show_diff:
                stu = add_diff_color(spjUtil.html_esc(sol), spjUtil.html_esc(stu))
            else:
                if len(stu) > output_limit:
                    stu = stu[:output_limit] + ' ... (more)'
                stu = spjUtil.green(stu)
            return stu
        
        def add_diff_color(x, y):
            r = '<font color="00FF00">'
            if x == y == '[]': return r + y + '</font>'
            prev = 0
            txtlen = 0
            for op in diff_match_patch().diff_main(y, x):
                if prev != op[0]:
                    if prev == -1:
                        r += '</s>'
                    if prev != 0:
                        r += '</font>'
                    if op[0] == 1:
                        r += '<font color=gray>'
                    elif op[0] == -1:
                        r += '<font color="FF8888"><s>'
                    prev = op[0]
                t = op[1]
                if txtlen + len(t) > output_limit:
                    r += t[:output_limit-txtlen] + '</font><font color=white> ... (more)'
                    break
                r += t
                txtlen += len(t)
            if prev==-1:
                r += '</s>'
            return r + '</font>'
        
        def hide_id(sid, n):
            if hide_ids == True: return f'{n:05}'
            if hide_ids == False: return sid
            h = hide_ids + 'x'*max(0,len(sid)-len(hide_ids))
            return ''.join('x' if e.lower()=='x' else d for e,d in zip(h,sid))
            
        # --------------------------------------------
        fout = open(filename, 'w', encoding='utf-8')
        DB_res = self.db['results']

        # use syntax highlight from https://highlightjs.org
        t = '''
<html>
<head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/languages/python.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/github-dark.min.css">
<script>hljs.highlightAll();</script>
</head>
<body bgcolor="black", text="white"><pre>
'''
        for pid in sorted(DB_res):
            if show_solution:
                t += show_solution_testscript(pid)
            _, sol_output, _ = get_solution(pid)
            fout.write(t);
            for n, sid in enumerate(get_sids(DB_res[pid]), 1):
                dbr = DB_res[pid][sid]
                code = self.get_code(sid)
                other_checks = [(k,v) for k,v in dbr.items() if k != 'output']
                t = add_one_sid(pid, hide_id(sid, n), code, dbr['output'], sol_output, other_checks)
                fout.write(t);
        fout.write('</pre></body></html>')
        fout.close()

    def create_testscript_file(self, pid, template_file='testscript_template.py', fout_name=None):
        fout_name = fout_name or f'{pid}_testscript.py'
        ts = __import__(f'{pid}_testsuite').Testsuite()
        testfuncs = ts.get_testfuncs(sorted_by_lineno=True)
        stdin_texts = {}
        testcase_funcs = ''
        for fname, func in testfuncs.items():
            t = inspect.getsource(func)
            k = t.find('def')
            k = t[:k].rfind('\n') + 1
            testcase_funcs += t[k:] + '\n'
            if func.stdin: stdin_texts[fname] = func.stdin
        solutions = dict(zip(testfuncs.keys(), self.get_sol_output(pid)))
        
        with open(template_file, encoding='utf-8') as f:
            src = f.read().format(testcase_funcs=testcase_funcs,
                                  solutions=solutions,
                                  stdin_texts=stdin_texts,
                                  pid=pid)
        
        with open(fout_name, 'w', encoding='utf-8') as f:
            f.write(format_str(src, mode=FileMode()))  # use black formatter

#-------------------------------------------------------------------
import sys
import editdistance

class spjTestsuite: # base class for Testsuite 
    timeout = 3
    kept_limit = 5000
    stdout_limit = 5000
    files = {}
    fwrite = False
    fsize_limit = 10000

    def __init__(self):
        self.kept = []

    def set_sid_pid(self, sid, pid):
        self.sid = sid
        self.pid = pid

    @staticmethod
    def set_testcase_default(timeout=None, stdout_limit=None, kept_limit=None,
                             ignore_input_prompt=False,
                             files=None, fwrite=None, fsize_limit=None):
        spjTestsuite.timeout = timeout or 3
        spjTestsuite.kept_limit = kept_limit or 5000
        spjTestsuite.stdout_limit = stdout_limit or 5000
        spjTestsuite.ignore_input_prompt = ignore_input_prompt
        spjTestsuite.files = files or {}
        spjTestsuite.fwrite = fwrite or False
        spjTestsuite.fsize_limit = fsize_limit or 10000
    
    @staticmethod
    def testcase(score_func, score_kwargs=None, stdin='', timeout=None,
                 stdout_limit=None, kept_limit=None, add_sol_funcs=None,
                 ignore_input_prompt=False,
                 files=None, fwrite=None, fsize_limit=None
                 ):
        def decorator(func):
            func.score_func = score_func              # scoring function
            func.score_kwargs = score_kwargs or {}    # {'arg1':val1, 'arg2':val2, ...}
            func.add_sol_funcs = add_sol_funcs or []  # sol_funcs replace submitted funcs
            func.ignore_input_prompt = ignore_input_prompt # no input prompt on stdout
            func.timeout = timeout or spjTestsuite.timeout                # execution time limit
            func.files = files or spjTestsuite.files                      # {filename: content}
            func.fwrite = fwrite or spjTestsuite.fwrite                   # True -> enable file write
            func.fsize_limit = fsize_limit or spjTestsuite.fsize_limit    # file size limit
            func.stdout_limit = stdout_limit or spjTestsuite.stdout_limit # -1 -> ignore all prints
            func.kept_limit = kept_limit or spjTestsuite.kept_limit       # measured w/ len(str(kept))
            if type(stdin) in (tuple, list):          # input text
                func.stdin = '\n'.join(str(e) for e in stdin)
            else:
                func.stdin = str(stdin)
            if func.stdin: func.stdin += '\n'

            return func
        return decorator
    
    def get_testfuncs(self, sorted_by_lineno=False):
        testfuncs = []
        for func in dir(self):
            f = getattr(self, func)
            if callable(f) and hasattr(f, 'score_func'):
                testfuncs.append(f)
        if sorted_by_lineno:
            testfuncs.sort(key=lambda f: inspect.getsourcelines(f)[1])
        return {f.__name__: f for f in testfuncs}

    def get_testfunc(self, func_name):
        return self.get_testfuncs()[func_name]
        
    def get_testfunc_names(self, sorted_by_lineno=False):
        return list(self.get_testfuncs(sorted_by_lineno).keys())
            
    def get_testscripts(self):
        # return a list of testscript objects
        testscripts = []
        for f in self.get_testfuncs(sorted_by_lineno=True).values():
            #setup_func = None # not yet implemented        
            #setup_src = '' if setup_func is None else f'self.{setup_func.__name__}()'
            testscripts.append(spjTestsuite.testscript(self, f))
        return testscripts

    @staticmethod
    def strip_str(s, strip='rstrip'):
        if strip == 'strip':
            s = s.strip()
        elif strip == 'rstrip':
            s = s.rstrip()
        elif strip == 'lstrip':
            s = s.lstrip()
        return s
        
    def keep(self, x, strip='rstrip'):
        if strip and type(x) is str:
            x = self.strip_str(x, strip)
        frames = inspect.getouterframes( inspect.currentframe() ) #[1][3]
        for frame in frames[1:]:  # trace parent back to the test_func
            if hasattr(self, frame.function):
                f = getattr(self, frame.function)
                if callable(f) and hasattr(f, 'score_func'):
                    testfunc = f
                    break
        else:
            assert False, 'keep is called outside testfunc'
        #testfunc = self.get_testfunc(parent_func_name)
        s = str(x)
        if testfunc.kept_limit != None and len(s) > testfunc.kept_limit:
            self.kept.append(s[:testfunc.kept_limit] + '...(more)')
            raise ValueError(f"Kept's size exceeds {testfunc.kept_limit}")
        self.kept.append(x)

    def score_approx_stdout(self, strip='rstrip'): # strip, rstrip, lstrip, none):
        stu = self.strip_str(self.stu_stdout, strip)
        sol = self.strip_str(self.sol_stdout, strip)        
        return self.approx_match(stu, sol)
    
    def score_exact_stdout(self, strip='rstrip'): # strip, rstrip, lstrip, none
        stu = self.strip_str(self.stu_stdout, strip)
        sol = self.strip_str(self.sol_stdout, strip)        
        return int(stu == sol)
                
    def score_kept(self, start=0, stop=None, isclose=True, approx=False, depth=0, order=True):
        if stop is None: stop = len(self.sol_kept)
        return self.score(self.sol_kept[start:stop], self.stu_kept[start:stop],
                          isclose=isclose, approx=approx, depth=depth, order=order)
    
    def score_exact_kept(self, start=0, stop=None, isclose=True, depth=0, order=True):
        return self.score_kept(start=start, stop=stop, isclose=isclose,
                               approx=False, depth=depth, order=order)

    def score_approx_kept(self, start=0, stop=None, depth=0, order=True):
        return self.score_kept(start=start, stop=stop, isclose=True,
                               approx=True, depth=depth, order=order)
#        if stop is None: stop = len(self.sol_kept)
#        s = sum(self.approx_match(a,b)
#                for a,b in zip(self.stu_kept[start:stop], self.sol_kept[start:stop]))
#        return s/len(self.sol_kept[start:stop])
    
    @staticmethod
    def approx_match(sol, stu):
        def f(x):
            if type(x) != list: return x
            return [str(e) if type(e) is list else e for e in x]
        
        if type(sol) != type(stu):
            return sol == stu
        if type(sol) == set:
            if len(sol) == len(stu) == 0: return 1
            return max(0,(len(sol&stu) - len(stu-sol))/ len(sol))
        if type(sol) == ndarray:
            sol = sol.tolist()
            stu = stu.tolist()
        if type(sol) != str:
            try:
                sol = list(sol)
                stu = list(stu)
            except:
                return sol == stu
        if len(sol) == len(stu) == 0: return 1
        # editdistance supports only strings and iterables of hashable objects
        sol = f(sol)
        stu = f(stu)
        return 1 - editdistance.distance(sol, stu)/max(len(sol),len(stu))
    
    @staticmethod
    def score(sol, stu, isclose=True, approx=False, depth=0, order=True):
        # approx = False
        # depth = 0:  [1,2,3,4], [1,2,3,4] --> 1
        #             [1,2,3,4], [1,2,3,0] --> 0
        #             [[1,2,3,0], [1,2,3,4]], [[1,2,3,4], [1,2,3,0]] --> 0
        # depth = 1:  [1,2,3,4], [1,2,0,4] --> 0.75
        #             [1,2,3,4], [2,3,4,0] --> 0
        #             [[1,2,3,4], [1,2,3,4]], [[1,2,3,4], [1,2,3,0]] --> 0.5
        # depth = 2:  [[1,2,3,4], [1,2,3,4]], [[1,2,3,4], [1,2,3,0]] --> (1+0.75)/2 = 0.875 
        #
        # approx = True
        # depth = 0:  [1,2,3,4], [1,0,3,4]  --> 0.75
        #             [1,2,3,4], [2,3,4,0]  --> 0.5
        #             [1,2,3,4], [0,0,2,3]  --> 0.25
        #             [1,2,3,4], [4,3,2,1]  --> 0
        #             [[1,2,3,4], [1,2,3,4]], [[0,0,0,0], [1,2,3,4]] --> 0.5
        # depth = 1:  [[1,2,3,4], [1,2,3,4]], [[2,3,4,0], [0,0,2,3]] --> (0.5+0.25)/2
        # depth = 2:  [[1,2,3,4], [1,2,3,4]], [[2,3,4,0], [0,0,2,3]] --> 0
        def eq(sol, stu):
            if isinstance(sol, Number) and isinstance(stu, Number):
                return int(isclose and math.isclose(sol,stu) or sol == stu)
            if type(sol) != type(stu):
                return 0
            if isinstance(sol, set):
                if approx:
                    return spjTestsuite.approx_match(sol, stu)
                else:
                    return sol == stu
            elif isinstance(sol, ndarray):
                if sol.shape != stu.shape: return 0
                return int(allclose(sol, stu))              
            elif type(sol) in (list, tuple):
                if approx:
                    if not order:
                        sol = set(sol)
                        stu = set(stu)
                    return spjTestsuite.approx_match(sol, stu)
                else:
                    if len(sol) != len(stu): return 0
                    if not order:
                        sol = sorted(sol)
                        stu = sorted(stu)
                    for a, b in zip(sol, stu):
                        if not eq(a, b): return 0
                    return 1
            else:
                return int(sol==stu)

        if (depth==0 or 
            (type(sol) not in (list,tuple,ndarray) and
             type(stu) not in (list,tuple,ndarray))):
            try:
                return eq(sol, stu)
            except Exception as e:
                raise Exception('ScoreError: ' + str(e))
        
        if type(sol) != type(stu): return 0
        if len(sol)==len(stu)==0: return 1
        if len(sol)==0 and len(stu)>0: return 0
        s = 0
        for a,b in zip(sol, stu):
            s += spjTestsuite.score(a, b, approx=approx, order=order, depth=depth-1)
        return s/len(sol)
        
    class testscript:
        def __init__(self, testsuite, testfunc):
            self.testsuite = testsuite
            self.testfunc = testfunc
            self.testcode = None
                     
        def test(self, code):
            #spjUtil.write_text_file('tt.txt', '****')
            try:
                compile(str(code), '', mode='exec')
            except Exception as err: 
                t = traceback.format_exc()
                return t[t.find('\n', t.rfind('File'))+1:], '', [], {}
            sol_func_src = ''
            for i,f in enumerate(self.testfunc.add_sol_funcs):
                sol_func_src += self.testsuite.solcode.get_func_source(f) + '\n'
            stu_class = code.get_all_class_source() + '\n'
            stu_funcs = code.get_all_funcs_source() + ' \n' + \
                         '# == added sol funcs ==\n' + \
                         sol_func_src
            stu_TLS = code.get_TLS()
            stu_source = '# == submitted funcs ==\n' + \
                         code.get_import() + '\n' + \
                         stu_class + '\n' + \
                         stu_funcs + '\n' + \
                         '# ===   main func    ==\n' + \
                         'def call_user_code():\n  pass\n' + \
                         '\n'.join(['  '+line.rstrip()
                                    for line in (stu_class+'\n'+stu_funcs+'\n'+stu_TLS).splitlines()]) + '\n'
            newline = '\n'
            test_src = f'''
{self.testsuite.srccode}
{newline.join(e.rstrip() for e in stu_source.splitlines())}

with spjInMemoryFile(files ={self.testfunc.files},
                     fwrite={self.testfunc.fwrite},
                     fsize_limit={self.testfunc.fsize_limit}) as mf:
    _stdin = sys.stdin
    _stdout = sys.stdout
    sys.stdin = io.StringIO({repr(self.testfunc.stdin)})
    sys.stdout = spjStringIO(maxsize={self.testfunc.stdout_limit})
    err = ''
    self = {self.testsuite.__class__.__name__}()
    self.sid = '{self.testsuite.sid}'
    self.pid = '{self.testsuite.pid}'
    builtins_print = builtins.print
    builtins_input = builtins.input
    if {self.testfunc.ignore_input_prompt}:
        def myinput(prompt=''):
            return builtins_input()
        builtins.input = myinput
        
    if {self.testfunc.stdout_limit} == -1:
        def myprint(*objects, sep='', end='', file=None, flush=False):
            return
        builtins.print = myprint        
    try:
        self.{self.testfunc.__name__}()
    except Exception as e:
        err = repr(e)
    finally:
        builtins.print = builtins_print
        builtins.input = builtins_input
        output = sys.stdout.getvalue().rstrip()
        sys.stdout.close()
        sys.stdin = _stdin
        sys.stdout = _stdout
        fout_contents = mf.get_fileout_contents()
spjUtil.dump_pickle( [err, output, self.kept, fout_contents],
                     {repr(RESULT_STUDENT_FILE)} )
'''
            #print('\n'.join(e for i,e in enumerate(test_src.splitlines(),1)))
            self.testcode = spjCode(test_src)
            try:
                self.testcode.exec(self.testfunc.timeout,
                                   self.testsuite.use_thread)
                return spjUtil.load_pickle(RESULT_STUDENT_FILE)
            except Exception as e:
                # time-out, syntax-error
                err = repr(e)
                if err.startswith('Exception('):
                    err = err[len('Exception(')+1:-2]
                elif err.startswith('TimeoutExpired'):
                    err = f'Time-out: {self.testfunc.timeout}s'
                return err,'',[],{}   # err,stdout,kept,fcontents
        
        def score(self, sol_out, sol_kept, sol_fcontents, stu_out, stu_kept, stu_fcontents):
            self.testsuite.sol_stdout = sol_out
            self.testsuite.sol_kept = sol_kept
            self.testsuite.sol_fcontents = sol_fcontents

            self.testsuite.stu_stdout = stu_out
            #try:   # previously use try-except, why ???
            self.testsuite.stu_kept = stu_kept
            #except:
            #    self.testsuite.stu_kept = []
            self.testsuite.stu_fcontents = stu_fcontents
            return self.testfunc.score_func(self.testsuite, **self.testfunc.score_kwargs)
        
        def get_testcode(self):
            return self.testcode
        
#-------------------------------------------------------
import io
import builtins

class spjInMemoryFile:
    def __init__(self, files=None, fwrite=False, fsize_limit=None):
        # files -> {filename: filecontent}
        files = files or {}
        self.files = files.copy()
        self.protected = set(files.keys())
        self.org_open = builtins.open
        self.fsize_limit = fsize_limit
        self.fwrite = fwrite
        self.fout_names = []
        
    def _not_writable(self, x):
        raise io.UnsupportedOperation(': not writable')
    
    def _my_open(self, filename,
                mode='r', buffering=-1, encoding=None,
                errors=None, newline=None, closefd=True, opener=None):
        if mode in ('r', 'rt'): #, 'rb'): 
            if filename in self.files:
                f = io.BytesIO(self.files[filename]) if 'b' in mode \
                    else io.StringIO(self.files[filename])
                f.write = f.writelines = self._not_writable
                return f
            raise FileNotFoundError(f"No such file or directory: '{filename}'")
        
        if (mode in ('w', 'wt') and  #, 'wb') and 
            (self.fwrite or filename == RESULT_STUDENT_FILE)):
            if filename in self.protected:
                raise FileExistsError(filename + ' is protected')
            
            def _close(fout):
                self.files[fout._filename] = fout.getvalue()
                fout._oclose()

            def _write(fout, t):
                if self.fsize_limit != None:
                    n = self.fsize_limit - fout.tell()
                    if n < len(t):
                        fout._owrite(t[:n] + '...(more)')
                        self.files[fout._filename] = fout.getvalue()
                        raise IOError(f'{fout._filename}: size > {self.fsize_limit}')
                fout._owrite(t)
                self.files[fout._filename] = fout.getvalue()
    
            # https://stackoverflow.com/questions/394770/override-a-method-at-instance-level
            fout = io.BytesIO() if 'b' in mode else io.StringIO()
            fout._oclose = fout.close
            fout.close = _close.__get__(fout, type(fout))
            fout._owrite = fout.write
            fout.write = _write.__get__(fout, type(fout))
            fout._filename = filename
            self.files[fout._filename] = ''
            self.fout_names.append(fout._filename)
            return fout
        raise ValueError(f"Can't open with mode: {mode}")

    def __enter__(self):
        builtins.open = self._my_open
        return self

    def __exit__(self, type, value, traceback):
        builtins.open = self.org_open

    def get_fileout_contents(self):
        return {fn: self.files[fn] for fn in self.fout_names }
    
#-------------------------------------------------------
# work only on Windows
import io
import threading
import ctypes

class spjThread(threading.Thread):  # thread is faster...
    def __init__(self, code):
        threading.Thread.__init__(self, )
        self.code = code
        self.err = ''
        
    def run(self):  # called after the thread is started
        try:
            exec(str(self.code), {})
            self.err = ''
        except Exception as e:
            self.err = repr(e)

    def get_error(self):      
        return self.err
    
    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def terminate(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            # exception fail
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)

#-------------------------------------------------------
# work on Windows & MasOS
import trace
import threading

class spjThread(threading.Thread):
    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def __init__(self, code):
        threading.Thread.__init__(self)
        self.killed = False
        self.code = code
        self.err = ''        

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run     
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace
    
    def terminate(self):
        self.killed = True

    def run(self):  # called after the thread is started
        try:
            exec(str(self.code), {})
            self.err = ''
        except Exception as e:
            self.err = repr(e)

    def get_error(self):      
        return self.err
     
#-------------------------------------------------------
# subprocess is better....
from multiprocessing import Process

class spjProcess(Process):
    def __init__(self, code):
        Process.__init__(self)
        self.code = code
        self.err = ''
        
    def run(self):  # called after the thread is started
        try:
            exec(str(self.code), {})
            self.err = ''
        except Exception as e:
            self.err = repr(e)

    def get_error(self):      
        return self.err
