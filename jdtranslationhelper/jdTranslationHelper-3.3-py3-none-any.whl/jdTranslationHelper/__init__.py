from typing import Optional, Dict
import locale
import json
import sys
import os


class jdTranslationHelper():
    def __init__(self, lang: Optional[str] = None, default_language: str = "en_GB") -> None:
        if not lang:
            self._selected_language = locale.getlocale()[0]
        else:
            self._selected_language = lang
        self._default_language = default_language
        self.strings: Dict[str, str] = {}

    def readLanguageFile(self, language_filename: str) -> None:
        """Reads a .lang file"""
        with open(language_filename, encoding="utf-8") as lines:
            for line in lines:
                line = line.replace("\n", "")
                if line == "" or line.strip().startswith("#"):
                    continue
                key, op, value = line.rstrip().partition('=')
                if not op:
                    print('Error loading line "{}" in file {}'.format(line, language_filename), file=sys.stderr)
                else:
                    self.strings[key] = value

    def readJsonFile(self, path: str) -> None:
        """Reads a .json file"""
        with open(path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        for key, value in json_data.items():
            self.strings[key] = value

    def readFile(self, path: str) -> None:
        """Reads a .lang or .json file"""
        if path.endswith(".lang"):
            self.readLanguageFile(path)
        elif path.endswith(".json"):
            pass
        else:
            raise ValueError(f"{path} is not a valid file")

    def loadDirectory(self, path: str) -> None:
        """Reads all langauge files in a Directory"""
        language_filename = os.path.join(path, self._default_language)
        if os.path.isfile(language_filename + ".lang"):
            self.readLanguageFile(language_filename + ".lang")
        elif os.path.isfile(language_filename + ".json"):
            self.readJsonFile(language_filename + ".json")
        else:
            print(f"{language_filename}.lang or {language_filename}.json was not found", file=sys.stderr)
            return

        language_filename = os.path.join(path, self._selected_language)
        if os.path.isfile(language_filename + ".lang"):
            self.readLanguageFile(language_filename + ".lang")
        elif os.path.isfile(language_filename + ".json"):
            self.readJsonFile(language_filename + ".json")

    def translate(self, key: str, default: Optional[str] = None) -> str:
        """Returns the translation of the Key"""
        if default is None:
            default = key
        return self.strings.get(key, default)

    def getStrings(self) -> Dict[str, str]:
        """Returns a Dict with all Keys with their translation"""
        return self.strings

    def getLanguage(self) -> str:
        """Returns the Language"""
        return self._selected_language

    def getDefaultLanguage(self) -> str:
        """Returns the default Language"""
        return self._default_language
