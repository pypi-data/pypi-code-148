import os, random
from wayOfChange import Project
import Utility
input = Utility.input
class Syllabic:
    # Espanol not finished needs to be sorted alphabetically
    validLanguages = ["Syllabic", "Shakespeare", "Espanol"]
    language = "Shakespeare"

    wordTypes = {
        "N": "Noun",
        "p": "Plural",
        "h": "Noun phrase",
        "V": "Verb (usually participle)",
        "t": "Transitive verb",
        "i": "Intransitive verb",
        "A": "Adjective",
        "v": "Adverb ",
        "C": "Conjunction",
        "P": "Preposition ",
        "!": "Interjection",
        "r": "Pronoun ",
        "D": "Definite article",
        "I": "Indefinite article",
        "o": "Nominative",
    }
    print("started going through moby words...")
    if True:  # or language == "Syllabic":
        with open(
                os.path.join(Project.directory, "mobypos.txt"), encoding="utf-8"
        ) as f:
            # with open("espanol.txt") as f:
            # with open('espanol.txt', encoding="ISO-8859-1") as f:
            # with open("espanol.txt") as f:
            mobyWords = {}
            mobyWordsByFirstLetter = {}
            for line in f:
                _word = line[: line.index("\\")]
                _wordType = line[line.index("\\"): line.index("\\") + 2]
                _wordType = _wordType.replace("\\", "")
                # mobyWords.append(line.strip())
                mobyWords[_word] = {"partOfSpeech": _wordType}
                _firstLetter = _word[0].lower()

                if not _firstLetter in mobyWordsByFirstLetter:
                    mobyWordsByFirstLetter[_firstLetter] = {}
                mobyWordsByFirstLetter[_firstLetter][_word] = {
                    "partOfSpeech": _wordType
                }
                # print(mobyWordsByFirstLetter)
    if True:
        # elif language == 'Shakespeare':
        with open(os.path.join(Project.directory, "shakespeare.txt")) as f:
            shakespeareWords = set
            shakespeareWordsByLetter = {}
            censorChars = [
                '"',
                ".",
                ";",
                ":",
                ",",
                "!",
                "'",
                "-",
                "?",
                ".",
                "*",
                "(",
                ")",
                ">",
                "<",
                "[",
                "]",
            ]
            omitWordWithCharsInMiddle = ["|", ".", "@", "_"]
            _wordsClean = []

            for l, line in enumerate(f):
                line = line.strip()
                _words = line.split(" ")
                for w, word in enumerate(_words):
                    if len(word) > 0:
                        _word = word[:]
                        while len(_word) > 0 and _word[-1] in censorChars:
                            _word = _word[:-1]
                        while len(_word) > 0 and _word[0] in censorChars:
                            _word = _word[1:]
                    if len(_word) > 1:
                        if _word.isupper():
                            _word = _word.lower()
                        # Filter numbers and weird computer strings
                        if len(_word) > 2 and any(
                                [char in ["|", ".", "@"] for char in _word[1:-1]]
                        ):
                            pass
                        elif any([c.isdigit() for c in _word]):
                            pass
                        elif any([c in ["|", ".", "@", "_"] for c in _word]):
                            _wordsClean.append(_word)
                            _wordsClean[-1] = (
                                _wordsClean[-1]
                                .replace("|", " ")
                                .replace("@", " ")
                                .replace(".", " ")
                                .replace("_", " ")
                            )
                        if _word[0].lower() in shakespeareWordsByLetter:
                            shakespeareWordsByLetter[_word[0].lower()].append(
                                _word
                            )
                        else:
                            shakespeareWordsByLetter[_word[0].lower()] = []
                # input('line {} {}'.format(l,' '.join(_wordsClean)))
            _wordsClean = set(_wordsClean)
            for letter in shakespeareWordsByLetter:
                shakespeareWordsByLetter[letter] = list(
                    set(shakespeareWordsByLetter[letter])
                )

    if language == "Espanol":

        # TODO# basic drunk version not tewsted
        espanolWords = []
        with open("espanol.txt", encoding="ISO-8859-1") as f:
            for l, line in enumerate(f):
                espanolWords.append(line.strip())
        raise ValueError(
            "Not done this yet.. maybe needs alphabetisation not sure"
        )

    # input('mobyWords created {} mobyWords created'.format('\n'.join(mobyWords)))
    # print(mobyWords.keys(),random.randint(1,1000))
    @classmethod
    def getRandomEnglishWord(cls, firstLetter=None, useShakespeare=None) -> str:
        if useShakespeare is None:
            useShakespeare = Syllabic.language == "Shakespeare"
        if firstLetter is None:
            _word = list(Syllabic.mobyWords.keys())[
                random.randint(0, len(Syllabic.mobyWords) - 1)
            ]
        else:
            firstLetter = firstLetter.lower()
            if not useShakespeare:
                _wordList = Syllabic.mobyWordsByFirstLetter
                _word = list(_wordList[firstLetter].keys())[
                    random.randint(0, len(_wordList[firstLetter]) - 1)
                ]
            else:
                _wordList = Syllabic.shakespeareWordsByLetter
                _word = list(_wordList[firstLetter])[
                    random.randint(0, len(_wordList[firstLetter]) - 1)
                ]

        return _word