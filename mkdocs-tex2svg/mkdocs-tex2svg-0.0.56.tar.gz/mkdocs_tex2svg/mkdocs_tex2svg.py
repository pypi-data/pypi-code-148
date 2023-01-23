"""
Graphviz extension for Markdown (e.g. for mkdocs) :
Renders the output inline, eliminating the need to configure an output
directory.

Supports outputs types of SVG and PNG. The output will be taken from the
filename specified in the tag, if given, or. Example:

in SVG:

```dot
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

```graphviz dot attack_plan.svg
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

in PNG:

```graphviz dot attack_plan.png
digraph G {
    rankdir=LR
    Earth [peripheries=2]
    Mars
    Earth -> Mars
}
```

Requires the graphviz library (http://www.graphviz.org/) and python 3

Inspired by jawher/markdown-dot (https://github.com/jawher/markdown-dot)
Forked from  cesaremorel/markdown-inline-graphviz (https://github.com/cesaremorel/markdown-inline-graphviz)
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

BLOCK_RE_MATHTABLE = re.compile(
        r'^[ 	]*```mathtable\n(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL)

TEX2SVG_COMMAND = 0
tex2svgVersion = "0.0.4"

# Command whitelist
SUPPORTED_COMMANDS = ['mathtable']

# DEFAULT COLOR OF NODES, EDGES AND FONT TEXTS
DEFAULT_COLOR = '789ABC'
DEFAULT_LIGHTTHEME_COLOR = '000000'
DEFAULT_DARKTHEME_COLOR = 'FFFFFF'

DEFAULT_COLOR = DEFAULT_COLOR.lower()
DEFAULT_LIGHTTHEME_COLOR = DEFAULT_LIGHTTHEME_COLOR.lower()
DEFAULT_DARKTHEME_COLOR = DEFAULT_DARKTHEME_COLOR.lower()
DEFAULT_PRIORITY = '75'

inlineMode = True
DEFAULT_PACKAGES = ['amsmath', 'tkz-tab', 'amssymb']

ESC_CHAR = {
    '$': r"\$",
    '*': r"\*",
    '^': r"\^",
}

class MkdocsTex2SvgExtension(markdown.Extension):

    def __init__(self, **kwargs):
        self.config = {
            'color' :           [DEFAULT_COLOR, 'Default color for Nodes & Edges'],
            'light_theme' :     [DEFAULT_LIGHTTHEME_COLOR, 'Default Light Color for Nodes & Edges'],
            'dark_theme' :      [DEFAULT_DARKTHEME_COLOR, 'Default Dark color for Nodes & Edges'],
            'bgcolor' :         [DEFAULT_COLOR, 'Default bgcolor for Graph'],
            'graph_color' :     [DEFAULT_COLOR, 'Default color for Graphs & Subgraphs/Clusters Roundings'], 
            'graph_fontcolor' : [DEFAULT_COLOR, 'Default color for Graphs & Subgraphs/Clusters Titles'], 
            'node_color' :      [DEFAULT_COLOR, 'Default color for Node Roundings'], 
            'node_fontcolor' :  [DEFAULT_COLOR, 'Default color for Node Texts'],
            'edge_color' :      [DEFAULT_COLOR, 'Default color for Edge Roundings'],
            'edge_fontcolor' :  [DEFAULT_COLOR, 'Default color for Edge Texts'],
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
        self.convert2string(config)
        self.set_html_colors()

    def convert2string(self, config):
        for colorKey in config.keys():
            self.config[colorKey][0] = str(self.config[colorKey][0])

    def set_html_colors(self):
        colorDict = self.config.keys()
        for colorKey in self.config.keys(): # translate config options in lowercase
            self.config[colorKey][0] = self.config[colorKey][0].lower()
        if self.config['color'][0] in HTML_COLORS.keys():
            self.config['color'][0] = HTML_COLORS[self.config['color'][0]]
        else: # SET DEFAULT to #+'color'
            self.config['color'][0] = "#"+self.config['color'][0]
        for colorKey in colorDict:
            if colorKey in ['color', 'bgcolor', 'light_theme', 'dark_theme']: # Special Keys
                continue
            if self.config[colorKey][0] in HTML_COLORS.keys():
                self.config[colorKey][0] = HTML_COLORS[self.config[colorKey][0]]
            elif self.config[colorKey][0] != DEFAULT_COLOR: # If more specific, set specific
                    if colorKey not in ['priority']:
                        self.config[colorKey][0] = "#"+self.config[colorKey][0]
            else: # otherwise set default to 'color' default
                self.config[colorKey][0] = self.config['color'][0]
        # SPECIAL KEYS:
        if self.config['light_theme'][0] in HTML_COLORS.keys():
            self.config['light_theme'][0] = HTML_COLORS[self.config['light_theme'][0]]
        else: # SET DEFAULT to 'light_theme'
            self.config['light_theme'][0] = "#"+self.config['light_theme'][0]
        if self.config['dark_theme'][0] in HTML_COLORS.keys():
            self.config['dark_theme'][0] = HTML_COLORS[self.config['dark_theme'][0]]
        else:
            self.config['dark_theme'][0] = "#"+self.config['dark_theme'][0]        
        if self.config['bgcolor'][0] in HTML_COLORS.keys():
            self.config['bgcolor'][0] = HTML_COLORS[self.config['bgcolor'][0]]
        elif self.config['bgcolor'][0] != 'None' and self.config['bgcolor'][0] != 'none': 
            self.config['bgcolor'][0] = "#"+self.config['bgcolor'][0]

    def repair_svg_in(self, output):
        """Returns a repaired svg output. Indeed:
        The Original svg ouput is broken in several places:
        - in the DOCTYPE, after "\\EN". Does not break the code, but still
        - every "\n" line-end breaks admonitions: svg has to be inline in this function
        - "http://.." attribute in <!DOCTYPE svg PUBLIC ...> breaks mkdocs, which adds an '<a>' tag around it
        - in the comment tag, after '<!-- Generated by graphviz'. THIS BREAKS THE CODE AND HAS TO BE REPAIRED
        - in the svg tag, after the 'height' attribute; THIS BREAKS THE CODE AND HAS TO BE REPAIRED
        - first line "<!-- Title: ...  -->" breaks some graphs, it is totally removed"
        """
        encoding='utf-8'
        output = output.decode(encoding)
        output = self.escape_chars(output)
        lines = output.split("\n")
        newLines = []
        # searchText = "Generated by graphviz"
        for i in range(len(lines)):
            # if i+3 <= len(lines)-1 and ( (searchText in lines[i-1]) or (searchText in lines[i]) or (searchText in lines[i+1]) or (searchText in lines[i+2]) or (searchText in lines[i+3]) ) :
            #     continue
            # if i>=3 and ("<svg" in lines[i-1] and searchText in lines[i-4]):
            #     continue
            if i == 0 and """<?xml version="1.0" encoding="UTF-8"?>""" in lines[0]:
                continue
            if i>=0 and ("<svg" in lines[i]):
                s = lines[i]
                s = s[:-1]+""" class="tex2svg">"""
                newLines.append(s)
            else:
                newLines.append(lines[i])
        # newLines = newLines[1:]
        newOutput = "\n".join(newLines)
        xmlHeaders = f"""<span class="tex2svg-light-dark" data-library-default="#{DEFAULT_COLOR}" data-default="{self.config['color'][0]}" data-light="{self.config['light_theme'][0]}" data-dark="{self.config['dark_theme'][0]}"></span>"""
        newOutput = xmlHeaders + newOutput
        newOutput = newOutput.replace("\n", "")
        return newOutput

    def read_block(self, text:str)->(str, int) or (None, -1):
        """Returns a tuple:
        - the graphviz or dot block, if exists, and
        - a code integer to caracterize the command : 
            0 for a'grapvhiz' command, 
            1 if 'dot' command)
        or (None, None), if not a graphviz or dot command block"""
        blocks = [BLOCK_RE_TEX2SVG.search(text),
                  BLOCK_RE_MATHTABLE.search(text)]
        for i in range(len(blocks)):
            if blocks[i] is not None:
                return blocks[i], i
        return None, -1

    def get_decalage(self, command:str, text:str)->int:
        """Renvoie le décalage (nombre d'espaces) où commencent les ``` dans la ligne ```command ...
        Cela suppose que le 'text' réellement la commande, ce qui est censé être le cas lros de l'utilisation de cette fonction
        """
        # command = 'dot' or 'graphviz dot' or 'graphviz neato' or etc..
        i_command = text.find("```"+command)
        i_previous_linefeed = text[:i_command].rfind("\n")
        decalage = i_command - i_previous_linefeed-1
        return decalage

    def read_svg_from(self, filename:str):
        with open(filename, "r", encoding="utf-8") as f:
            svgList = f.readlines()
        # # print("svglist=",svglist)
        # if """<?xml version="1.0" encoding="UTF-8"?>""" == svgList[0]:
        #     # "<?xml ...>" element breaks Math Tables inside Admonitions, when at index 0 of list : let's remove it
        #     svgList = svgList[1:]
        # # svglist = [f"""<span class="tex2svg tex2svg-light-dark" data-library-default="#{DEFAULT_COLOR}" data-default="{self.config['color'][0]}" data-light="{self.config['light_theme'][0]}" data-dark="{self.config['dark_theme'][0]}"></span>"""] + [f"""<!-- Generated by mkdocs-tex2svg {tex2svgVersion} -->"""] + svglist
        # # svglist = [f"""<span class="tex2svg tex2svg-light-dark" data-library-default="#{DEFAULT_COLOR}" data-default="{self.config['color'][0]}" data-light="{self.config['light_theme'][0]}" data-dark="{self.config['dark_theme'][0]}"></span>"""] + svglist
        # svg = "".join(svgList)
        # # svg = self.escape_chars(svg)
        # # svg = svg.replace("\n","") # otherwise breaks Admonitions
        # # print("SVG=", svg)
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

    # def formatSvg(self, svg):
    #     svgList = svg.split("\n")
    #     if """<?xml version="1.0" encoding="UTF-8"?>""" == svgList[0]:
    #         # "<?xml ...>" element breaks Math Tables inside Admonitions, when at index 0 of list : let's remove it
    #         svgList = svgList[1:]
    #     svg = "\n".join(svgList)
    #     # svg = rf"{svg}"
    #     svg = svg.replace("fill=\"rgb(100%, 100%, 100%)\"", "fill=\"transparent\"")
    #     # print("BGCOLOR=", self.config['bgcolor'][0])
    #     # svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"{self.config['bgcolor'][0]}\"")
    #     # svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"var(--md-default-fg-color)\"")
    #     # svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"red\"")
    #     svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"#{DEFAULT_COLOR}\"")
    #     # svgList = [f"""<span class="tex2svg tex2svg-light-dark" data-library-default="#{DEFAULT_COLOR}" data-default="{self.config['color'][0]}" data-light="{self.config['light_theme'][0]}" data-dark="{self.config['dark_theme'][0]}"></span>"""].extend(svgList)
    #     return svg

    def formatSvg(self, svg, color):
        svgList = svg.split("\n")
        if """<?xml version="1.0" encoding="UTF-8"?>""" == svgList[0]:
            # "<?xml ...>" element breaks Math Tables inside Admonitions, when at index 0 of list : let's remove it
            svgList = svgList[1:]
        svg = "\n".join(svgList)
        # svg = rf"{svg}"
        svg = svg.replace("fill=\"rgb(100%, 100%, 100%)\"", "fill=\"transparent\"")
        # print("BGCOLOR=", self.config['bgcolor'][0])
        svg = svg.replace("\"rgb(0%, 0%, 0%)\"", f"\"{color}\"")
        # svgList = [f"""<span class="tex2svg tex2svg-light-dark" data-library-default="#{DEFAULT_COLOR}" data-default="{self.config['color'][0]}" data-light="{self.config['light_theme'][0]}" data-dark="{self.config['dark_theme'][0]}"></span>"""].extend(svgList)
        return svg


    def svg_encode(self, svg):
        # Ref: https://bl.ocks.org/jennyknuth/222825e315d45a738ed9d6e04c7a88d0
        # Encode an SVG string so it can be embedded into a data URL.
        enc_chars = """%#"{}<>""" # Encode these to %hex
        enc_chars_maybe = '&|[]^`;?:@=' # Add to enc_chars on exception
        svg_enc = ''
        # Translate character by character
        for c in str(svg):
            if c in enc_chars:
                if c == '"':
                    svg_enc += "'"
                else:
                    svg_enc += '%' + format(ord(c), "x")
            else:
                svg_enc += c
        return ' '.join(svg_enc.split()) # Compact whitespace

    # def createBase64DatapathForSvgOfColor(self, content, svg, randomFilename, color):
    #     # encoding = "utf-8"
    #     # with open(f"{randomFilename}.svg", "rb") as f:
    #     #     s = base64.b64encode(f.read())
    #     # # svg = base64.b64decode(s).decode("utf-8")
    #     # svg = base64.b64decode(s).decode(f"{encoding}")

    #     svg = self.formatSvg(svg, color)

    #     args = ["cat", f"""{randomFilename}.svg"""]
    #     proc = subprocess.Popen(
    #         args,
    #         stdin=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         stdout=subprocess.PIPE)
    #     # proc.stdin.write(content.encode('utf-8'))
    #     proc.stdin.write(content.encode('utf-8'))
    #     output, err = proc.communicate()

    #     svg = output
    #     svg = self.repair_svg_in(svg)

    #     # Export Svg Image as base64
    #     encoding = 'base64'
    #     svg = svg.encode('utf-8')
    #     svg = base64.b64encode(svg).decode('utf-8')
    #     data_url_filetype = 'svg+xml'
    #     data_path = "data:image/%s;%s,%s" % (
    #         data_url_filetype,
    #         encoding,
    #         svg)
    #     return data_path

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
                else: # MATHTABLE command
                    # text = self.escape_chars(text)
                    filename = "noname.svg"
                    command = "mathtable"
                    decalage = self.get_decalage(command, text)

                filetype = filename[filename.rfind('.')+1:]

                # RAW TEX2SVG BLOCK CONTENT
                content = m.group('content')
                tex = content

                try:
                    bgcolor = self.config['bgcolor'][0]
                    # graph_color = self.config['graph_color'][0]
                    # graph_fontcolor = self.config['graph_fontcolor'][0]
                    # node_color = self.config['node_color'][0]
                    # node_fontcolor = self.config['node_fontcolor'][0]
                    # edge_color = self.config['edge_color'][0]
                    # edge_fontcolor = self.config['edge_fontcolor'][0]
                    preamble, postamble = self.get_preamble_postamble(True, DEFAULT_PACKAGES)
                    tex = preamble+tex+postamble

                    # Create Random Name
                    randomFilename = f"{dirPath}/tmp{salt}"
                    print("randomFilename=",randomFilename)
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

                    # Create and Save three files : one for Light Mode, one for separation of the contiguous svgs, and one for Dark Mode
                    svgLight = self.formatSvg(svg, "red")
                    svgDark = self.formatSvg(svg, "blue")
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
                    os.remove(f"""{randomFilename}.tex""")
                    os.remove(f"""{randomFilename}.aux""")
                    os.remove(f"""{randomFilename}.log""")
                    os.remove(f"""{randomFilename}.pdf""")
                    os.remove(f"""{randomFilename}_crop.pdf""")
                    os.remove(f"""{randomFilename}.svg""")
                    if os.path.exists(f"""{randomFilename}dark.svg"""):
                        os.remove(f"""{randomFilename}dark.svg""")
                    if os.path.exists(f"""{randomFilename}light.svg"""):
                        os.remove(f"""{randomFilename}light.svg""")

                    # text = '%s\n%s\n%s\n%s' % (
                    #     text[:m.start()], img1, img2, text[m.end():])
                    text = f"""{text[:m.start()]!s}\n{img1!s}\n{img2!s}\n{text[m.end():]!s}"""
                except Exception as e:
                        return (
                            '<pre>Error : ' + str(e) + '</pre>'
                            '<pre>' + content + '</pre>').split('\n')
        return text.split("\n")

def makeExtension(*args, **kwargs):
    return MkdocsTex2SvgExtension(*args, **kwargs)
