"""
    Title: HeadKuarter
    Module Name: passwordGenrator
    Language: Python
    Date Created: 23-05-2022
    Date Modified: 23-05-2022
    Description:
        ###############################################################
        ##  genrate password ussing formosa                          ## 
        ###############################################################
 """

from . import generator
from . import mnemonic
from pathlib import Path
import copy
import random
#import swapper
import json
import gc
import traceback


def get_directory() -> Path:
        """
            This method finds out in which directory the code is running

        Returns
        -------
        path
            Returns the absolute path found of the file
        """
        return Path(__file__).parent.absolute()

# varible 
selected_theme = "finances"
directory_path = (get_directory() / "themes")
files_path = Path(directory_path)
# Finding paths and filtering .json files
themes = tuple([each_directory.stem for each_directory in files_path.glob(r"*.json")])
base_dict = mnemonic.Mnemonic(selected_theme).words_dictionary
edited_dict = copy.deepcopy(base_dict)

global last_text 
global last_n_phrases  
global password_lines
last_text = ""
password_lines = []
last_n_phrases = 0


var_check_number=False
var_check_case = False
var_check_char = False


number_phrases = 1 # initial value

def generate_text(selected_theme,number_phrases,rbn,rbc,sc):
        """
            This method calls object Generator which build a mnemonic phrase in formosa standard
            then updates displayed text
        """
        g = generator.Generator(number_phrases * 32, selected_theme, None)
       
        phrases = g.show_phrases()


        global last_text
        global last_n_phrases 
        global password_lines
        

        text = ""
        phrase_len = len(base_dict["NATURAL_ORDER"])
        for word_index in range(len(phrases)):
            text = text + phrases[word_index][0:2]
        password_genrated = text
        text = text + "\n"
        for phrase_index in range(len(phrases) // phrase_len):
            text = text + " ".join(phrases[phrase_len * phrase_index:phrase_len * (phrase_index + 1)]) + "\n"

        #print(f'bool {rbn}, {rbc}, {sc}')

        insert_number(rbn)
        insert_spc_char(rbc)
        insert_swap_case(sc)

        return(password_genrated)


def insert_number(flag):
        """
            This method changes an ordinary character to a number
        """
        to_replace = ["a", "e", "i", "o", "b", "g", "t"]
        replace_by = ["4", "3", "1", "0", "8", "6", "7"]
        insert_character(to_replace, replace_by, flag)

def insert_spc_char(flag):
        """
            This method changes an ordinary character to a special character
        """
        to_replace = ["c", "h", "l", "s", "j"]
        replace_by = ["¢", "#", "£", "$", "!"]
        insert_character(to_replace, replace_by, flag)

def insert_swap_case(flag):
        """
            This method swaps the case of a character
        """
        to_replace = list(map(chr, range(97, 123)))
        replace_by = [each_char.swapcase() for each_char in to_replace]
        insert_character(to_replace, replace_by, flag)

def insert_character(to_replace: list, replace_by: list, check_box_var: bool):
        """
            This method finds out if the text in the texbox is written as natural or edited
            and calls method replace_characters() with correct order of variables

        Parameters
        ----------
        to_replace : list
            The list of characters to be removed
        replace_by : list
            The list of characters to be inserted
        check_box_var : bool
            This variable tells if the word is written as natural, or it is already edited
        """
        array_criteria = [each_char in last_text for each_char in to_replace]
        if check_box_var and any(array_criteria):
            replace_characters(replace_by, to_replace, False)
        elif not check_box_var:
            replace_characters(to_replace, replace_by, True)
        

def replace_characters(insert: list, remove: list, check_var: bool = False):
        """
            This method replaces a character given by another character given

        Parameters
        ----------
        insert : list
            The list of characters to be removed
        remove : list
            The list of characters to be inserted
        check_var : bool
            Controls which criteria are used, if it is any or none element in the list
        """
        global last_text
        global password_lines
        lines = last_text.splitlines(False)
        for line_index in password_lines:
            # If there is any character to be removed in the line and
            # There is any or none character inserted in the line depending on the control variable "check_var"
            if any([each_char in lines[line_index] for each_char in remove]) and \
                    check_var == any([each_char in lines[line_index] for each_char in insert]):
                index_list = []
                [index_list.append(lines[line_index].find(each_char)) for each_char in remove]
                lesser_char = min([each_index for each_index in index_list if each_index >= 0])
                lesser_char_index = remove.index(lines[line_index][lesser_char])
                new_line = lines[line_index].replace(remove[lesser_char_index], insert[lesser_char_index], 1)
                last_text = last_text.replace(lines[line_index], new_line)
        #print (last_text)        

def gen_save_file():
    """
        This method saves the generated phrases to a txt file
    """
    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(last_text)
    


