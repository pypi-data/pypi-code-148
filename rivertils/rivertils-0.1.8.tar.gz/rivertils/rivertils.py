import argparse
from rivertils.lists import *

from google.cloud import translate_v2
import os
import six

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue

def get_language(message):
    """
    A crude quick test likely returns None
    """
    language = None
    if len(message) < 3:
        language = "en"
    else:
        # phrases like 'haha' are triggering bizarre language ids
        for x in indicates_english_message:
            if x.lower() in message.lower():
                language = "en"
    # print(f"from get_language(): {language}")
    return language


def translate_text(text):
    """
    
    Translates text into the target language with Google Cloud Translate API.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    """
    
    translate_client = translate_v2.Client( )

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=None)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result


def get_test_message_and_language(message: str):
    """
    Removes any @mention at the start of the message string.
    If the message is not english, it translates it to english.
    Also, returns a language code to let you know which language the user is communicating in.
    """
    # print("get_message_and_language()")

    # response = None
    language = None

    # message = remove_at(message)
    # print(f"{message=}")

    

    # blob = TextBlob(message)
    # print(f"blob= {blob}")
    # exit()

    language_code = get_language(message)
    # print(f"{language_code=}")

    if not language:

        try:    
            translation = translate_text(message)
            # print(f"{translation=}")

            language_code = translation["detectedSourceLanguage"]

            if translation["detectedSourceLanguage"] != "en":
                
                message = translation["translatedText"]
                # print(f"{language=}")
                # print(f"{message=}")
        except Exception as e:
            print(
                "Rivertils: couldn't do translator.translate in get_message_and_language.py: ",
                e,
                message,
                language,
            )
            language_code = "en"


    # print(f"returning {message}, {language_code}")
    return message, language_code
    # return response

# def remove_at(message):
#     """
#     If there's a comma in the first 20 characters
#     Remove everything before and including the first comma.
#     """

#     # If there's a comma in the first 20 characters
#     if "," in message[:20]:

#         # Remove everything before and including the first comma.
#         message = message.split(",", 1)[1].strip()

#     return message