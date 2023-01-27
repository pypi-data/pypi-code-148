from __future__ import annotations, print_function
import os, sys
sys.path.append('../')
class Utility:
    numToCipher = {
        "1": "ONE",
        "2": "TWO",
        "3": "THREE",
        "4": "FOUR",
        "5": "FIVE",
        "6": "SIX",
        "7": "SEVEN",
        "8": "EIGHT",
        "9": "NINE",
    }




    projectClasses = (
        'wayOfChange',
        'JazzNote',
        'Change'

    )

    @classmethod
    def grepClassFiles(cls):
        pass

    origInput = input

    @classmethod
    def print(cls, *args, sep=' ',end='\n'):
        from inspect import currentframe, getframeinfo
        frameinfo = getframeinfo(currentframe().f_back)
        linestr = 'File "{}", line {}'.format(frameinfo.filename, frameinfo.lineno)
        while len(linestr) < 60: linestr += ' '
        print(linestr, *args)


    @classmethod
    def input(cls,*args, sep=' '):
        # print('it is finally hpapening with input({})'.format(s))
        # frameinfo = getframeinfo(currentframe())
        fmt_str = ' File "{}", line {}, in {}'
        abs_filepath = os.path.abspath(__file__)
        import inspect
        #lineno = currentframe().f_back.f_lineno
        try:
            frame = inspect.currentframe().f_back.f_back
            prevFrame = inspect.currentframe().f_back

            lineno = frame.f_lineno
            prevLineno= prevFrame.f_lineno
        except AttributeError:
            try:
                frame = inspect.currentframe().f_back
                prevFrame = inspect.currentframe()
                lineno = frame.f_lineno
                prevLineno = prevFrame.f_lineno
            except AttributeError:
                frame = inspect.currentframe()
                lineno = frame.f_lineno
                prevLineno = None
                prevFrame = None

        stack = inspect.stack()


        # currentframe().f_back.f_locals


        #line_str = fmt_str.format(abs_filepath, lineno, frame)
        fmt_str = ' File "{}", line {},  \nin: {},  \nat: {} \nFile "{}", line {},  '
        line_str = '\n'.join([
                fmt_str.format(
                str(f.filename),
                prevLineno,
                '{}({})'.format(str(f.frame).split(' code ')[-1][:-1],[k +'='+str(v)+', ' for k,v in f.frame.f_locals.items()]),
                f.code_context[0].split(' code ')[-1].strip(),
                str(f.filename),
                f.lineno,
                #f.code_context[0]
        ) \
                for f in stack if f.code_context and f.code_context[0].strip().startswith('input(' )])
        return Utility.origInput(
            #'\n' + line_str + '\n' + sep.join([str(s) for s in args]) + ' :: input() called from line ' + str(lineno))
            '\n' + line_str + '\n' + sep.join([str(s) for s in args]))


    @classmethod
    def semitoneDistToFreqDiff(cls,f1, f2):
        return 12 * (math.log(f2 / f1) / math.log(2))

    @classmethod
    def secondSmallest(cls,iterable):
        return sorted(set(iterable))[1]

    @classmethod
    def secondBiggest(cls, iterable):
        return sorted(set(iterable))[-2]
    @classmethod
    def removeNestedParentheses(cls,s,brackets=('(',')')):
        ret = ''
        skip = 0
        for i in s:
            if i == brackets[0]:
                skip += 1
            elif i == brackets[1] and skip > 0:
                skip -= 1
            elif skip == 0:
                ret += i
        return ret
    
    @classmethod
    def allIndexes(cls,iterable,value)->[int]:
        if type(iterable) == str:
            if value in ('',' '): raise ValueError('did you really want the indexes of all spaces in a the string? "{}"'.format(iterable))
            indexes = [index for index in range(len(iterable)) if iterable.startswith(value, index)]
            '''if len(indexes) > 2:
                input('\nman oh man value: "{}"\n{}\n{}'.format(value,indexes,iterable))'''
            return indexes
        else:
            return [index for index, i in  enumerate(iterable) if i == value]

    @classmethod
    def compileApp():
        import PyInstaller.__main__

        PyInstaller.__main__.run([
            'my_script.py',
            '--onefile',
            '--windowed'
        ])

    @classmethod
    def threaded(cls,function,args:[]=False):
        # Call work function
        if args:
            t1 = threading.Thread(target=function, args=args)
        else:
            t1 = threading.Thread(target=function)
        t1.start()


    @classmethod
    def getClassVariables(cls, Class):
        return {key: value for key, value in Class.__dict__.items() if not key.startswith('__') and not callable(key)}

    @classmethod
    def rasterisePDF(cls,path,greyScale=False,invertColour=False):

        newPath = path.replace(
            '.pdf','Rasterised.pdf'
        )
        print('begin converting',path,'to a rasterised .pdf! This may take a long time.')
        _startTime = datetime.datetime.now()
        pages = pdf2image.convert_from_path(path,transparent=True,size=(8.5*300,None),dpi=300,fmt='png',)
        #imTarget = Image.open("/Users/apple/Desktop/bbd.jpg")

        im_list = pages
        pdf1_filename = newPath
        im1 = im_list[0]

        #im1.save(pdf1_filename, "PDF", resolution=8.5*1200, save_all=True, append_images=im_list[1:],
        #         subsampling=0,optimize=True)
        print('it took',datetime.datetime.now()-_startTime)
        pdf = FPDF()
        # imagelist is the list with all image filenames
        for i,image in enumerate(tqdm(pages)):
            pageDir = os.path.join(Graphics.getDirectoryOfColourScheme(greyScale,invertColour),'ChordsOfChangeBookPages')
            pagePath = os.path.join(pageDir,str(i)+'.png')
            Utility.makeDirectory(pageDir)
            image.save(pagePath)
            pdf.add_page()
            pdf.image(pagePath, 0, 0, 210, 297,)
        pdf.output(newPath, "F")
        print('finished rasterizing '+pdf1_filename)

    @classmethod
    def makeNumberCipheredIfPreceededBy(cls, text: str, number, cipherTriggers):
        if cipherTriggers == None:
            cipherTriggers = (
                "0",
                "=",
                ".",
                Book.unicodeChars["Flat"],
                Book.unicodeChars["Sharp"],
            )


        _done = False
        _cipheredText = ""
        for c, char in enumerate(text):
            if char == str(number):
                if c != 0 and (
                    text[c - 1] in cipherTriggers
                    or (text[c - 2] in cipherTriggers and text[c - 1] == " ")
                ):
                    _cipheredText += cls.numToCipher[char]
                else:
                    _cipheredText += char
            else:
                _cipheredText += char
        return _cipheredText

    @classmethod
    def makeNumberUnciphered(cls, text, number: int = None):
        if number == None:
            numbers = tuple(range(10))
        else:
            numbers = (number,)
        for num in cls.numToCipher.keys():
            text = text.replace(cls.numToCipher[num], num)
        return text

    @classmethod
    def replaceTextInFile(cls, filename, searchStr, replaceStr):
        # input(type(file))
        # Read in the file
        if type(filename) != str:
            raise TypeError("hey file{}".format(str(file)))
        with open(filename, "r") as file:
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace(searchStr, replaceStr)

        # Write the file out again
        with open(filename, "w", encoding="UTF8") as file:
            file.write(filedata)

    @classmethod
    def getParameters(cls, func):
        keys = func.__code__.co_varnames[: func.__code__.co_argcount][::-1]
        sorter = {j: i for i, j in enumerate(keys[::-1])}
        values = func.__defaults__[::-1]
        kwargs = {i: j for i, j in zip(keys, values)}
        sorted_args = tuple(
            sorted([i for i in keys if i not in kwargs], key=sorter.get)
        )
        sorted_kwargs = {i: kwargs[i] for i in sorted(kwargs.keys(), key=sorter.get)}
        return sorted_args, sorted_kwargs

    @classmethod
    def saveToFile(cls, text: str, filePath):
        with open(filePath, "w+", encoding="utf-8") as file:
            file.write(text)
            file.close()
            print("wrote to ////file:{}".format(filePath))

    @classmethod
    def splitList(cls, l: [], n: int) -> [[]]:
        return np.array_split(l,n)
        '''matrix = []
        for i in range(n):
            start = round(len(l) / n * i)
            end = round(len(l) / n * (i + 1))
            matrix.append(l[start:end])
        return matrix'''

    @classmethod
    def removeAccentsFromText(cls, s: str):
        # Needs unicodedata
        return "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )

    @classmethod
    def multiple_replace(cls, string, rep_dict):
        pattern = re.compile(
            "|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]),
            flags=re.DOTALL,
        )
        return pattern.sub(lambda x: rep_dict[x.group(0)], string)

    @classmethod
    def printPrettyVars(cls, *vars, sep=" ", indicator="="):
        """
        Gets the names and values of vars. Does it from the out most frame inner-wards.
        :param vars: variable to get name from.
        :param sep: what to put between vars.
        :param indicator: what to put between name and value.
        :return: string
        """
        for var in vars:
            for fi in reversed(inspect.stack()):
                names = [
                    var_name
                    for var_name, var_val in fi.frame.f_locals.items()
                    if var_val is var
                ]
                values = [
                    var_val
                    for var_name, var_val in fi.frame.f_locals.items()
                    if var_val is var
                ]
                if len(names) > 0 and names[0] != "var":
                    print(names[0], indicator, values[0].__repr__(), end=sep, sep="")

    @classmethod
    def openFile(cls, filename):
        try:
            if sys.platform == "win32":
                os.startfile(filename)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filename])
            print("opening _thisDoc:", filename)
        except:
            raise OSError("we were not able to open {}.".format(filename))

    @classmethod
    def makeCharEscaped(cls, char, string):
        return string.replace(char)

    @classmethod
    def writeToFile(cls, data: str, filename):
        file = open(filename, "w+")
        file.write(data)
        file.close()

    @classmethod
    def makeStrCamelCase(cls, string, firstWordIsLower=True):
        string = "".join(x for x in string.title() if not x.isspace())
        if firstWordIsLower:
            string = string[0].lower() + string[1:]
        return string

    @classmethod
    def replaceStrInFile(cls, filename, string, replacement):
        # Read in the file
        with open(filename, "r", encoding="utf-8") as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(string, replacement)

        # Write the file out again
        with open(filename, "w", encoding="utf-8") as file:
            file.write(filedata)

    @classmethod
    def floatToFraction(cls, num, latexFractions=True):
        import math
        integerPart = math.floor(num)
        # At this part we will add making the 2/7 fraction etc
        numOrig = num
        num = round(num - integerPart, 6)
        if num == 0:
            _fractionUnicode = ""
            _latexUnicode = ""
        elif num == 0.5:
            _fractionUnicode = "½"
            _latexUnicode = "$\\frac{1}{2}$"
        elif num == 0.333333:
            _fractionUnicode = "⅓"
            _latexUnicode = "$\\frac{1}{3}$"
        elif num == 0.666667:
            _fractionUnicode = "⅔"
            _latexUnicode = "$\\frac{2}{3}$"
        elif num == 0.25:
            _fractionUnicode = "¼"
            _latexUnicode = "$\\frac{1}{4}$"
        elif num == 0.75:
            _fractionUnicode = "¾"
            _latexUnicode = "$\\frac{3}{4}$"
        elif num == 0.2:
            _fractionUnicode = "⅕"
            _latexUnicode = "$\\frac{1}{5}$"
        elif num == 0.4:
            _fractionUnicode = "⅖"
            _latexUnicode = "$\\frac{2}{5}$"
        elif num == 0.6:
            _fractionUnicode = "⅗"
            _latexUnicode = "$\\frac{3}{5}$"
        elif num == 0.8:
            _fractionUnicode = "⅘"
            _latexUnicode = "$\\frac{4}{5}$"
        elif num == 0.142857:
            _fractionUnicode = "⅐"
            _latexUnicode = "$\\frac{1}{7}$"
        elif num == 0.285714:
            _fractionUnicode = "²⁄₇"
            _latexUnicode = "$\\frac{2}{7}$"
        elif num == 0.428571:
            _fractionUnicode = "³⁄₇"
            _latexUnicode = "$\\frac{3}{7}$"
        elif num == 0.571429:
            _fractionUnicode = "⁴⁄₇"
            _latexUnicode = "$\\frac{4}{7}$"
        elif num == 0.714286:
            _fractionUnicode = "⁵⁄₇"
            _latexUnicode = "$\\frac{5}{7}$"
        elif num == 0.857143:
            _fractionUnicode = "⁶⁄₇"
            _latexUnicode = "$\\frac{6}{7}$"
        elif num == 0.111111:
            _fractionUnicode = "⅑"
            _latexUnicode = "$\\frac{1}{9}$"
        elif num == 0.222222:
            _fractionUnicode = "²⁄₉"
            _latexUnicode = "$\\frac{2}{9}$"
        elif num == 0.444444:
            _fractionUnicode = "⁴⁄₉"
            _latexUnicode = "$\\frac{4}{9}$"
        elif num == 0.555556:
            _fractionUnicode = "⁵⁄₉"
            _latexUnicode = "$\\frac{5}{9}$"
        elif num == 0.777778:
            _fractionUnicode = "⁷⁄₉"
            _latexUnicode = "$\\frac{7}{9}$"
        elif num == 0.888889:
            _fractionUnicode = "⁸⁄₉"
            _latexUnicode = "$\\frac{8}{9}$"
        elif num == 0.909091:
            _fractionUnicode = "10⁄11"
            _latexUnicode = "$\\frac{10}{11}$"
        else:
            # raise ValueError(numOrig)
            _fractionUnicode = str(round(num, 2))
            _latexUnicode = _fractionUnicode
        _str = ""
        if integerPart:
            _str += str(integerPart)
        if latexFractions:
            _str += _latexUnicode
        else:
            _str += _fractionUnicode
        return _str

    @classmethod
    def rgbToHex(cls, rgbs):
        # hsls = [(0.61, 0.43981, 0.2806), (0.69, 0.528195, 0.2277)]
        return ["".join("%02X" % round(i * 100) for i in rgb) for rgb in rgbs]

    @classmethod
    def draw_ellipse(cls, image, bounds, width=1, outline="white", antialias=4):
        """Improved ellipse drawing function, based on PIL.ImageDraw."""
        # https://stackoverflow.com/questions/32504246/draw-ellipse-in-python-pil-with-line-thickness
        # Use a single channel image (mode='L') as mask.
        # The size of the mask can be increased relative to the imput image
        # to get smoother looking results.
        mask = Image.new(
            size=[int(dim * antialias) for dim in image.size], mode="L", color="black"
        )
        draw = ImageDraw.Draw(mask)

        # draw outer shape in white (color) and inner shape in black (transparent)
        for offset, fill in (width / -2.0, "white"), (width / 2.0, "black"):
            left, top = [(value + offset) * antialias for value in bounds[:2]]
            right, bottom = [(value - offset) * antialias for value in bounds[2:]]
            draw.ellipse([left, top, right, bottom], fill=fill)

        # downsample the mask using PIL.Image.LANCZOS
        # (a high-quality downsampling filter).
        mask = mask.resize(image.size, Image.LANCZOS)
        # paste outline color to input image through the mask
        image.paste(outline, mask=mask)

    @classmethod
    def replaceStrInFilenames(
        cls, dir="C:\\Users\\Edrihan\\PycharmProjects\\wayOfChange\\Graphics"
    ):
        for filepath in glob.iglob("./**/*.txt", recursive=True):
            with open(filepath, encoding="Latin-1") as file:
                s = file.read()
            s = s.replace("_", " ")
            with open(filepath, "w") as file:
                file.write(s)
                print("replacing char in {}".format(filepath))

    @classmethod
    def listIsSequential(cls, theList: [int], insertZero=True):
        first = theList[0]
        if insertZero and -1 in theList:
            # If the list contains [-1,1] in that order
            if theList.index(1) - theList.index(-1) == 1:
                theList = theList.insert(theList.index(1), 0)
        if all([c == (change - first) for c, change in enumerate(theList)]):
            return True
        else:
            return False

    @classmethod
    def turnLstToMatrix(cls, lst: list, cols: int = None, rows: int = None) -> [[]]:
        if rows == None and cols == None:
            raise ValueError("need to specify rows or columns")
        elif rows != None and cols != None:
            if rows * cols < len(lst):
                raise ValueError(
                    "not enough rows {} and cols {} to fit results.\n{}".format(
                        rows, cols, lst
                    )
                )
        elif rows != None:
            cols = math.floor(len(lst) / rows) + (len(lst) % rows != 0)
        elif cols != None:
            rows = math.floor(len(lst) / cols) + (len(lst) % cols != 0)
        _matrix = []
        _i = 0
        for row in range(rows):
            _matrix.append([])
            for col in range(cols):
                if _i < len(lst):
                    _matrix[-1].append(lst[_i])
                else:
                    _matrix[-1].append(None)

                _i += 1
        return _matrix



    @classmethod
    def flattenList(cls, lst: [list]) -> []:
        _flatten = lambda l: [item for sublist in l for item in sublist]
        if not isinstance(lst, (list,)):
            raise TypeError("{} is not a list.".format(lst))
        elif len(lst) >= 1 and not isinstance(lst[0], (list,)):
            return lst
        else:
            return _flatten(lst)

    @classmethod
    def flipAxesOfList(cls, lst: [list]):
        if not type(lst[0]) == list:
            raise TypeError("flipAxesOfList() accepts a list of lists.")
        _flippedLst = []
        for i in lst[0]:
            _flippedLst.append([1 for i in lst])
        for r, row in enumerate(lst):
            for d, data in enumerate(row):
                if (len(_flippedLst) + 1) < d:
                    _flippedList.append([])
                if (len(_flippedLst[d]) + 1) < r:
                    _flippedLst[d].append("")
                _flippedLst[d][r] = data
        # print(lst,_flippedLst,'blakfladkf')
        # input()
        return _flippedLst

    @classmethod
    def getFontStrings(cls):
        font_file = "/home/user/raleway.ttf"
        command = "otfinfo"
        params = ["--info"]
        result = subprocess.run(
            [command, *params, font_file], stdout=subprocess.PIPE
        ).stdout
        font_name_re = re.compile(r"Full name:\s*(.*)")
        font_name = font_name_re.findall(result.decode())
        print(font_name[0])

    @classmethod
    def makeDirectory(cls, path, printSuccess=True, printSkip=False):
        if os.path.isdir(path):
            if printSkip:
                print("skipped making {} because it already exists.".format(path))
            return True

        if 'F:' in path:
            raise TypeError('asdfasdf')
        os.makedirs(path, 0o777)
        if printSuccess:
            print("Successfully created the directory %s " % path)

    @classmethod
    def insertSubstringInStr(cls, pos: int, string: str, substring: str) -> str:
        return string[:pos] + substring + string[pos:]

    @classmethod
    def numPartOfStr(cls, string: str, includeDecimalPoint=True) -> float:
        _numPart = ""
        for char in string:
            if char.isdigit() or (includeDecimalPoint == True and char == "."):
                _numPart += char
        return float(_numPart)

    @classmethod
    def checkForDuplicates(cls, listToCheck: list):

        if len(set(listToCheck)) != len(listToCheck):
            input("woww, there are duplicates..")
        else:
            input("nice!- no duplicates!")
        print(
            "dupes",
            "\n  ".join([k for k, v in Counter(quals).items() if v > 1]),
            "length",
            len([k for k, v in Counter(quals).items() if v > 1]),
        )

        # indexes of dupes
        D = defaultdict(list)
        for i, item in enumerate(listToCheck):
            D[item].append(i)
        D = {k: v for k, v in D.items() if len(v) > 1}
        # Generic one
        print("D:", "\nd:".join([str(i[0]) + str(i[1]) for i in D.items()]))
        # specific one only for something I can't remember
        """print('D:', '\nd:'.join(
            [str(i[0]) + str([n + 1 for n in i[1]]) + str([str(theBook.sequence[a].straightenDegrees()) for a in i[1]])
             for i in D.items()]))"""

    @classmethod
    def allPinyin(cls):
        print("Hexagram pinyin\\\\")
        for i in Hexagram.pinyin:
            print(i)
        print("Trigram pinyin\\\\")
        print(Trigram.allPinyin())
        print("Tetragram pinyin\\\\")
        print(Tetragram.allPinyin())