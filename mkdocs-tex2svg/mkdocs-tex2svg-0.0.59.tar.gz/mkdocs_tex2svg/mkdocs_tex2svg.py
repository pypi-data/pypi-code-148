#  License: GNU GPLv3+, Rodrigo Schwencke (Copyleft) 

"""
(Comprehensive) LaTeX Extension for Mkdocs, with custom LaTeX packages, and Dynamic Mkdocs Light and Dark Themes.
Renders the output as Base64 SVGs.

Requires a comprehensive LaTeX distribution, like texlive-most in Manjaro/Archlinux

This extension is the exclusive work of Rodrigo Schwencke, Copyleft.
"""

import os
import re
import markdown
import subprocess
import base64
import shlex
from random import randint
from .htmlColors import HTML_COLORS

# Global vars
BLOCK_RE_TEX2SVG = re.compile(
    r'^[ 	]*```tex2svg[ ]* (?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL
    )

BLOCK_RE_VARTABLE = re.compile(
        r'^[ 	]*```vartable\n(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL)

TEX2SVG_COMMAND = 0
tex2svgVersion = "0.0.4"

# Command whitelist
SUPPORTED_COMMANDS = ['tex2svg', 'vartable']
AUTHORIZED_CONFIGS = ["vartable", "priority"]

# DEFAULT COLOR OF TEXTS, BACKGROUNDS for LABELS and for FV - Forbidden Values (Valeurs Interdites - VI)
DEFAULT_COLOR = '789ABC'
DEFAULT_LIGHT_COLOR = '000000'
DEFAULT_LIGHT_BGLABEL = 'FFFFFF'
DEFAULT_LIGHT_BGVI = 'FFFFFF'

DEFAULT_DARK_COLOR = 'FFFFFF'
DEFAULT_DARK_BGLABEL = '2E303E'
DEFAULT_DARK_BGVI = '2E303E'

DEFAULT_VARTABLE_DICT = {
    'light': {
        'color': f'{DEFAULT_LIGHT_COLOR}',
        'bglabel': f'{DEFAULT_LIGHT_BGLABEL}', 
        'bgvi': f'{DEFAULT_LIGHT_BGVI}'}, 
    'dark': {
        'color': f'{DEFAULT_DARK_COLOR}', 
        'bglabel': f'{DEFAULT_DARK_BGLABEL}', 
        'bgvi': f'{DEFAULT_DARK_BGVI}'
        }
    }

DEFAULT_COLOR = DEFAULT_COLOR.lower()
DEFAULT_LIGHT_COLOR = DEFAULT_LIGHT_COLOR.lower()
# DEFAULT_DARKTHEME_COLOR = DEFAULT_DARKTHEME_COLOR.lower()
DEFAULT_PRIORITY = '75'

inlineMode = True
DEFAULT_PACKAGES = ['amsmath', 'tkz-tab', 'amssymb']

DEBUG = False

ESC_CHAR = {
    '$': r"\$",
    '*': r"\*",
    '^': r"\^",
}

class MkdocsTex2SvgExtension(markdown.Extension):

    def __init__(self, **kwargs):
        self.config = {
            'vartable' :        [DEFAULT_VARTABLE_DICT, 'Default Vartable Dict'],
            'priority' :        [DEFAULT_PRIORITY, 'Default Priority for this Extension']
        }
        super(MkdocsTex2SvgExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add MkdocsTex2SvgPreprocessor to the Markdown instance. """
        md.registerExtension(self)
        md.preprocessors.register(MkdocsTex2SvgPreprocessor(md, self.config), 'tex2svg_block', int(self.config['priority'][0]))

class MkdocsTex2SvgPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md, config):
        super(MkdocsTex2SvgPreprocessor, self).__init__(md)
        self.config = config
        self.formatConfigOptions()

    def formatConfigOptions(self):
        for entry in self.config.keys():
            if entry == "vartable": # format vartable options
                colorLight = self.config[entry][0]["light"]["color"] = self.config[entry][0]["light"]["color"].lower()
                bgLabelLight = self.config[entry][0]["light"]["bglabel"] = self.config[entry][0]["light"]["bglabel"].lower()
                bgVILight = self.config[entry][0]["light"]["bgvi"] = self.config[entry][0]["light"]["bgvi"].lower()

                colorDark = self.config[entry][0]["dark"]["color"] = self.config[entry][0]["dark"]["color"].lower()
                bgLabelDark = self.config[entry][0]["dark"]["bglabel"] = self.config[entry][0]["dark"]["bglabel"].lower()
                bgVIDark = self.config[entry][0]["dark"]["bgvi"] = self.config[entry][0]["dark"]["bgvi"].lower()

                # Set Colors of Texts & Borders
                if colorLight in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    colorLight = self.config[entry][0]["light"]["color"]
                elif len(self.config[entry][0]["light"]["color"]) in [3, 6, 8]:
                    colorLight = self.config[entry][0]["light"]["color"] = "#"+str(self.config[entry][0]["light"]["color"])

                if colorDark in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    colorDark = self.config[entry][0]["dark"]["color"]
                elif len(self.config[entry][0]["dark"]["color"]) in [3, 6, 8]:
                    colorDark = self.config[entry][0]["dark"]["color"] = "#"+str(self.config[entry][0]["dark"]["color"])

                # Set Background Colors for Labels
                if bgLabelLight in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    bgLabelLight = self.config[entry][0]["light"]["bglabel"]
                elif len(self.config[entry][0]["light"]["bglabel"]) in [3, 6, 8]:
                    bgLabelLight = self.config[entry][0]["light"]["bglabel"] = "#"+str(self.config[entry][0]["light"]["bglabel"])

                if bgLabelDark in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    bgLabelDark = self.config[entry][0]["dark"]["bglabel"]
                elif len(self.config[entry][0]["dark"]["bglabel"]) in [3, 6, 8]:
                    bgLabelDark = self.config[entry][0]["dark"]["bglabel"] = "#"+str(self.config[entry][0]["dark"]["bglabel"])

                # Set Background Colors for Forbidden Values (FV / Valeurs Interdites / VI)
                if bgVILight in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    bgVILight = self.config[entry][0]["light"]["bgvi"]
                elif len(self.config[entry][0]["light"]["bgvi"]) in [3, 6, 8]:
                    bgVILight = self.config[entry][0]["light"]["bgvi"] = "#"+str(self.config[entry][0]["light"]["bgvi"])

                if bgVIDark in HTML_COLORS.keys(): # HTML HEXA COLOR, just for information
                    bgVIDark = self.config[entry][0]["dark"]["bgvi"]
                elif len(self.config[entry][0]["dark"]["bgvi"]) in [3, 6, 8]:
                    bgVIDark = self.config[entry][0]["dark"]["bgvi"] = "#"+str(self.config[entry][0]["dark"]["bgvi"])

    def read_block(self, text:str)->(str, int) or (None, -1):
        """Returns a tuple:
        - the graphviz or dot block, if exists, and
        - a code integer to caracterize the command : 
            0 for a'grapvhiz' command, 
            1 if 'dot' command)
        or (None, None), if not a graphviz or dot command block"""
        blocks = [BLOCK_RE_TEX2SVG.search(text),
                  BLOCK_RE_VARTABLE.search(text)]
        for i in range(len(blocks)):
            if blocks[i] is not None:
                return blocks[i], i
        return None, -1

    def get_decalage(self, command:str, text:str)->int:
        """Renvoie le décalage (nombre d'espaces) où commencent les ``` dans la ligne ```command ...
        Cela suppose que le 'text' réellement la commande, ce qui est censé être le cas lros de l'utilisation de cette fonction
        """
        # command = 'tex2svg' or 'vartable' etc..
        i_command = text.find("```"+command)
        i_previous_linefeed = text[:i_command].rfind("\n")
        decalage = i_command - i_previous_linefeed-1
        return decalage

    def read_svg_from(self, filename:str):
        with open(filename, "r", encoding="utf-8") as f:
            svgList = f.readlines()
        return svg

    def to_file(self, content:str,filename:str):
        content = f"{content}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def escape_chars(self, output):
        for c in ESC_CHAR:
            output = output.replace(c, ESC_CHAR[c])
        return output

    def get_preamble_postamble(self, inlineMode=True, packages=DEFAULT_PACKAGES)->tuple:
        if inlineMode:
            preamble = r"\documentclass{article}"+"\n"
            for package in packages:
                preamble += rf"\usepackage{{{package}}}"+"\n"
            preamble += r"""\begin{document}
\pagestyle{empty}
\begin{equation*}
"""
            postamble = r"""\end{equation*}
\end{document}
"""
        else: # block mode
            preamble = r"\documentclass{article}"+"\n"
            for package in packages:
                preamble += rf"\usepackage{{{package}}}"+"\n"
            preamble += r"""\begin{document}
\pagestyle{empty}
$$"""
            postamble = r"""$$
\end{document}
"""
        return (preamble, postamble)

    def formatSvg(self, svg, color, bgLabel, bgVI):
        svgList = svg.split("\n")
        if """<?xml version="1.0" encoding="UTF-8"?>""" == svgList[0]:
            # "<?xml ...>" element breaks Math Tables inside Admonitions, when at index 0 of list : let's remove it
            svgList = svgList[1:]
        svg = "\n".join(svgList)
        svg = svg.replace("fill=\"rgb(100%, 100%, 100%)\"", f"fill=\"{bgLabel}\"")
        svg = svg.replace("stroke=\"rgb(100%, 100%, 100%)\"", f"stroke=\"{bgVI}\"")
        svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"{color}\"")
        return svg

    def run(self, lines): # Preprocessors must extend markdown.Preprocessor
        """
        Each subclass of Preprocessor should override the `run` method, which
        takes the document as a list of strings split by newlines and returns
        the (possibly modified) list of lines.
        
        Match and generate dot code blocks.
        """
        dirName = "docs/tex2svg"
        dirName = dirName.lstrip("/")
        dirName = dirName.rstrip("/")
        # dirPath = f"./{dirName}"
        dirPath = f"{dirName}"
        os.makedirs(f"{dirPath}", exist_ok=True)
        text = "\n".join(lines)
        while 1:
            m, block_type = self.read_block(text)
            if not m:
                break
            else:
                salt = randint(1,100000)
                if block_type == TEX2SVG_COMMAND: # General Graphviz command
                    command = m.group('command')
                     # Whitelist command, prevent command injection.
                    if command not in SUPPORTED_COMMANDS:
                        raise Exception('Command not supported: %s' % command)
                    # text = self.escape_chars(text)
                    filename = m.group('filename')
                    decalage = self.get_decalage("graphviz "+command, text)
                    htmlHeader = " "*decalage+f"""<span class="tex2svg"></span>"""
                else: # VARTABLE command
                    filename = "noname.svg"
                    command = "vartable"
                    decalage = self.get_decalage(command, text)
                    htmlHeader = " "*decalage+f"""<span class="tex2svg vartable"></span>"""

                filetype = filename[filename.rfind('.')+1:]

                # RAW TEX2SVG BLOCK CONTENT
                content = m.group('content')
                tex = content

                try:
                    # bgcolor = self.config['bgcolor'][0]
                    bgcolor = "#"+DEFAULT_COLOR
                    preamble, postamble = self.get_preamble_postamble(True, DEFAULT_PACKAGES)
                    tex = preamble+tex+postamble

                    # Create Random Name
                    randomFilename = f"{dirPath}/tmp{salt}"
                    self.to_file(tex, f"{randomFilename}.tex")

                    # Export Tkz-tab to Svg
                    os.system(f"pdflatex -output-directory {dirPath} {randomFilename}.tex &> /dev/null")
                    os.system(f"pdfcrop {randomFilename}.pdf {randomFilename}_crop.pdf &> /dev/null")
                    os.system(f"pdf2svg {randomFilename}_crop.pdf {randomFilename}.svg &> /dev/null")

                    # Read Exported Svg File
                    encoding = "utf-8"
                    with open(f"{randomFilename}.svg", "rb") as f:
                        s = base64.b64encode(f.read())
                    svg = base64.b64decode(s).decode(f"{encoding}")

                    bgLight = self.config["vartable"][0]["light"]["color"]
                    bgLabelLight = self.config["vartable"][0]["light"]["bglabel"]
                    bgVILight = self.config["vartable"][0]["light"]["bgvi"]

                    bgDark = self.config["vartable"][0]["dark"]["color"]
                    bgLabelDark = self.config["vartable"][0]["dark"]["bglabel"]
                    bgVIDark = self.config["vartable"][0]["dark"]["bgvi"]

                    svgLight = self.formatSvg(svg, bgLight, bgLabelLight, bgVILight)
                    svgDark = self.formatSvg(svg, bgDark, bgLabelDark, bgVIDark)

                    # Create and Save three files : one for Light Mode, one for separation of the contiguous svgs, and one for Dark Mode
                    self.to_file(svgLight, f"{randomFilename}light.svg")
                    htmlSeparator = """<span id="separator"></span>\n"""
                    self.to_file(htmlSeparator, f"{dirPath}/separator.html")
                    self.to_file(svgDark, f"{randomFilename}dark.svg")

                    # Start of Popen
                    cmd_parts = [f"""cat {randomFilename}light.svg {dirPath}/separator.html {randomFilename}dark.svg"""]

                    i = 0
                    p = {}
                    for cmd_part in cmd_parts:
                        try:
                            cmd_part = cmd_part.strip()
                            if i == 0:
                                p[0]=subprocess.Popen(shlex.split(cmd_part),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            else:
                                p[i]=subprocess.Popen(shlex.split(cmd_part),stdin=p[i-1].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            i += 1
                        except Exception as e:
                            err = str(e) + ' : ' + str(cmd_part)
                            return (
                                '<pre>Error : ' + err + '</pre>'
                                '<pre>' + content + '</pre>').split('\n')
                    (output, err) = p[i-1].communicate()
                    exit_code = p[0].wait()

                    svgGlobal = output.decode("utf-8")
                    svgList = svgGlobal.split(htmlSeparator)

                    svgLight = svgList[0]
                    svgDark = svgList[1]

                    # create IMG1 for Light Mode
                    base64Encoding = 'base64'
                    svgLight = svgLight.encode('utf-8')
                    svgLight = base64.b64encode(svgLight).decode('utf-8')
                    data_url_filetype = 'svg+xml'
                    data_path1 = "data:image/%s;%s,%s" % (
                        data_url_filetype,
                        base64Encoding,
                        svgLight)
                    img1 = " "*decalage+"![" + randomFilename + "Light" + "](" + data_path1 + "){.text2svg .light}"

                    # create IMG2 for Dark Mode
                    svgDark = svgDark.encode('utf-8')
                    svgDark = base64.b64encode(svgDark).decode('utf-8')
                    data_url_filetype = 'svg+xml'
                    data_path2 = "data:image/%s;%s,%s" % (
                        data_url_filetype,
                        base64Encoding,
                        svgDark)
                    img2 = " "*decalage+"![" + randomFilename + "Dark" + "](" + data_path2 + "){.tex2svg .dark}"

                    # Clean The Tmp Folder after
                    if not DEBUG:
                        for filename in os.listdir(dirPath):
                            try:
                                if os.path.exists(f"{dirPath}/{filename}"):
                                    os.remove(f"{dirPath}/{filename}")
                            except:
                                print("oups..")
                        # os.remove(f"""{randomFilename}.tex""")
                        # os.remove(f"""{randomFilename}.aux""")
                        # os.remove(f"""{randomFilename}.log""")
                        # os.remove(f"""{randomFilename}.pdf""")
                        # os.remove(f"""{randomFilename}_crop.pdf""")
                        # os.remove(f"""{randomFilename}.svg""")
                        # os.remove(f"{dirPath}/separator.html")
                        # if os.path.exists(f"""{randomFilename}dark.svg"""):
                        #     os.remove(f"""{randomFilename}dark.svg""")
                        # if os.path.exists(f"""{randomFilename}light.svg"""):
                        #     os.remove(f"""{randomFilename}light.svg""")

                    # text = '%s\n%s\n%s\n%s' % (
                    #     text[:m.start()], img1, img2, text[m.end():])
                    text = f"""{text[:m.start()]!s}\n{htmlHeader!s}\n{img1!s}\n{img2!s}\n{text[m.end():]!s}"""
                except Exception as e:
                        return (
                            '<pre>Error : ' + str(e) + '</pre>'
                            '<pre>' + content + '</pre>').split('\n')
        return text.split("\n")

def makeExtension(*args, **kwargs):
    return MkdocsTex2SvgExtension(*args, **kwargs)
