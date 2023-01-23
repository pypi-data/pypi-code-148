import requests
import os
import random


class KelimeScraper:
    def __init__(self, base_url="https://sozluk.gov.tr/gts"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://sozluk.gov.tr",
            "Connection": "keep-alive",
            "Referer": "https://sozluk.gov.tr/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        self.alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
        self.words_folder = os.path.join(os.path.dirname(__file__), "kelimelerr")
        if not os.path.exists(self.words_folder):
            os.mkdir(self.words_folder)
            self._download_words_folder()
        self.wordlists = [file for file in os.listdir(self.words_folder) if file.endswith(".list")]

    def _download_words_folder(self):
        """Download the words folder from the github repository"""
        url = "https://raw.githubusercontent.com/CanNuhlar/Turkce-Kelime-Listesi/master/"

        # download the files
        for letter in self.alphabet:
            response = requests.get(url + letter + ".list", headers=self.headers)
            with open(os.path.join(self.words_folder, letter + ".list"), "w", encoding="utf-8") as f:
                f.write(response.text)

        

    def get_meaning(self, word):
        """Get the meaning of a word from the given url"""
        # Get the response from the url
        response = requests.get(self.base_url + "?ara=" + word, headers=self.headers)

        # Get the meaning from the response
        meaning = response.json()[0]["anlamlarListe"][0]["anlam"]

        # Return the meaning
        return meaning


    def get_random_word(self, first_letter=None, length=None):
        """Get a random word from the kelimeler folder"""
        if first_letter is None:
            first_letter = random.choice(self.alphabet)
        wordlist = first_letter + ".list"
        if wordlist not in self.wordlists:
            raise ValueError("Kelime listesi bulunamadı.")
        with open(os.path.join(self.words_folder, wordlist), "r", encoding="utf-8") as f:
            words = f.readlines()
        if length is None:
            return random.choice(words).strip()
        else:
            return random.choice([word for word in words if len(word.strip()) == length]).strip()



class Kelime(KelimeScraper):
    def __init__(self, base_url="https://sozluk.gov.tr/gts", word=None, first_letter=None, length=None):
        super().__init__(base_url)
        if word is None:
            word = self.get_random_word(first_letter, length)
        self.word = word


    @property
    def meaning(self):
        return self.get_meaning(self.word)



if __name__ == "__main__":
    # Kelime class'ından kelime nesnesi oluştur
    k = Kelime(first_letter="a", length=5)

    # kelimenin anlamını yazdır
    print(k.word)

    # kelimenin anlamını yazdır
    print(k.meaning)