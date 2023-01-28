import os
from time import sleep

from ply.lex import LexError

from pykotor.common.script import DataType
from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.ncs import NCS, write_ncs, read_ncs
from pykotor.resource.formats.ncs.compiler.interpreter import Interpreter, Stack
from pykotor.resource.formats.ncs.compiler.lexer import NssLexer
from pykotor.resource.formats.ncs.compiler.parser import NssParser
from pykotor.resource.formats.ncs.optimizers import RemoveNopOptimizer


def main1():
    nssLexer = NssLexer()
    nssPareser = NssParser()

    lex = nssLexer.lexer
    parser = nssPareser.parser

    aaa = """
    int num = 123;
    string tag = "abc";
    object a = GetObjectByTag(tag, num);
    """

    bbb = """
    int num = GetPartyMemberCount();
    object a = GetObjectByTag(GetStringByStrRef(0), num);
    """

    ccc = """
    void main() {
        int abc = 0;
        if (abc)
        {
            abc = 1;
        }
        abc = 2;
    }
    """

    # EngineCalls can be called without declaration/assignment
    # but still adds to stack unrecorderd
    # need to fix.

    t = parser.parse(ccc, tracking=True)

    #GetObjectByTag(tag, num);

    ncs = NCS()
    t.compile(ncs)
    for inst in ncs.instructions:
        print(inst)


def compile(script):
    nssLexer = NssLexer()
    nssPareser = NssParser()

    lex = nssLexer.lexer
    parser = nssPareser.parser

    ncs = NCS()
    t = parser.parse(script)
    t.compile(ncs)
    return ncs


def main2():
    dir1 = "C:/Users/hugin/Desktop/Scripts/K1/"
    dir2 = "C:/Users/hugin/Desktop/Scripts/K2/"

    success = []
    failed = []

    for file in os.listdir(dir1):
        try:
            script = BinaryReader.load_file(dir1 + file).decode()
            compile(script)
            success.append(file)
        except (Exception, LexError) as e:
            failed.append(file)
    for file in os.listdir(dir2):
        try:
            script = BinaryReader.load_file(dir2 + file).decode()
            compile(script)
            success.append(file)
        except (Exception, LexError) as e:
            failed.append(file)

    total_scripts = len(success) + len(failed)
    percentage = int(len(success)/total_scripts*100)
    print("{}/{} ({}%)".format(len(success), total_scripts, percentage))
    print(success)


def main4():
    dir1 = "C:/Users/hugin/Desktop/Scripts/K1/"
    dir2 = "C:/Users/hugin/Desktop/Scripts/K2/"

    for file in os.listdir(dir1):
        script = BinaryReader.load_file(dir1 + file).decode(errors="ignore")
        if "for(" in script or "for (" in script:
            print(file)


def main3():
    script = """
    
    void main()
    {
        int a = 5;
        int b = 0;
        b += 2 * 2;
    }
    """
    ncs = compile(script)
    #ncs.print()

    interpreter = Interpreter(ncs)
    interpreter.run()
    interpreter.print()


def main5():
    script = """
            #include "k_inc_cheat"

            void main()
            {
                case 1:
                
            }
        """
    ncs = compile(script)
    ncs.optimize([RemoveNopOptimizer()])
    ncs.print()
    write_ncs(ncs, "C:/Users/hugin/Desktop/ext/epic.ncs")

    interpreter = Interpreter(ncs)
    interpreter.run()


def main6():
    ncs = read_ncs("C:/Users/hugin/Desktop/ext/epic.ncs")
    #ncs.print()

    interpreter = Interpreter(ncs)
    interpreter.run()

    interpreter.print()
    print(interpreter.action_snapshots)



def main7():
    stack = Stack()
    stack.add(DataType.FLOAT, 1)  # -24
    stack.add(DataType.FLOAT, 2)  # -20
    stack.add(DataType.FLOAT, 3)  # -17
    stack.add(DataType.FLOAT, 4)  # -12
    stack.add(DataType.FLOAT, 5)  # -8
    stack.add(DataType.FLOAT, 6)  # -4
    stack.copy_to_top(-12, 4)


main6()
