"""
    Title: HeadKuarter
    Module Name: creatContainer
    Language: Python
    Date Created: 
    Date Modified: 7-05-2022
    Description:
        ###############################################################
        ##                    Password Genrator                      ## 
        ###############################################################
 """

import random
import sys
from . import mnemonic


class Generator:
    def __init__(self, entropy_size: int, chosen_theme: str, entropy):
        # Pick "finances" as default, if no theme is given
        chosen_theme = (chosen_theme if chosen_theme is not None else "finances")
        self.m = mnemonic.Mnemonic(chosen_theme)
        self.phrase_len = len(self.m.words_dictionary["FILLING_ORDER"])
        # Pick random if the entropy input is none
        entropy_bits = (entropy if entropy is not None else bytearray(
            [random.getrandbits(8) for _ in range(entropy_size//8)]))
        self.phrase = self.m.to_mnemonic(entropy_bits).split()

    def show_phrases(self) -> list[str]:
        """
            This method prints the generated phrases and returns the phrases
        Returns
        -------
        str
            This is the returned phrases generated as a string variable
        """
        '''  for i in range(len(self.phrase)):
            print(self.phrase[i][0:2], end="")
        
        for i in range(len(self.phrase)//self.phrase_len):
            print(" ".join(self.phrase[self.phrase_len*i:self.phrase_len*(i+1)]))'''
        return self.phrase





