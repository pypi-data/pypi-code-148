from pykotor.common.script import ScriptFunction

from pykotor.common.stream import BinaryReader

nwscript_file = "C:/New folder/nwscript.nss"
file = BinaryReader.load_file(nwscript_file).decode(errors='ignore')
file = file.split("\n")[1666:]

functions = []
function = ScriptFunction("void", "", [], "", "")
for line in file:
    if line.startswith("//"):
        function = ScriptFunction("void", "", [], "", "")
        #routine_id = line[3:line.index(".")]
        print(line)

