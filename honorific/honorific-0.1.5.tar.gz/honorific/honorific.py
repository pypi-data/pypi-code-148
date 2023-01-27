import logging
import re
import subprocess

import pymorphy2
import spacy
from spacy.tokens import Token

try:
    nlp = spacy.load("ru_core_news_lg")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "ru_core_news_lg"])
    nlp = spacy.load("ru_core_news_lg")

logging.getLogger("spacy_lefff").setLevel(logging.WARNING)

morph = pymorphy2.MorphAnalyzer()

your_sing = {
    "твой": "ваш",
    "твои": "ваши",
    "твоего": "вашего",
    "твоих": "ваших",
    "твоему": "вашему",
    "твоим": "вашим",
    "твоими": "вашими",
    "твоём": "вашем",
    "твоем": "вашем",
    "твоя": "ваша",
    "твоей": "вашей",
    "твою": "вашу",
    "твоё": "ваше",
    "твое": "ваше",
    "по-твоему": "по-вашему",
}

your_plur = {
    "ваш": "твой",
    "вашего": "твоего",
    "вашем": "твоём",
    "ваша": "твоя",
    "вашей": "твоей",
    "вашу": "твою",
    "ваше": "твоё",
    "вашему": "твоему",
    "ваши": "твои",
    "ваших": "твоих",
    "вашим": "твоим",
    "вашими": "твоими",
    "по-вашему": "по-твоему",
}

honoratives = [
    "миссис",
    "мисс",
    "мистер",
    "миледи",
    "милорд",
    "сеньор",
    "сеньорита",
    "мадам",
    "мадемуазель",
    "мадмуазель",
    "мосье",
    "месье",
    "мсье",
    "мусьё",
    "мосье",
    "монсьер",
    "сэр",
    "сер",
    "госпожа",
    "господин",
]


def word_parser(word: str, lemma: str):
    """
    Правильный парсинг слова
    :param word:
    :param lemma:
    :return:
    """
    parse: pymorphy2.analyzer.Parse = morph.parse(word)
    list_parse = [p for p in parse if p.normal_form == lemma]  # подходящие разборы
    return list_parse[0] if len(list_parse) > 0 else parse[0]


def punctuation_separator(text: str) -> str:
    """
    Обработка пунктуации:
        день был замечательный!светит солнце. -> день был замечательный! светит солнце.

    :param text:
    :return:
    """
    new_text = re.sub(r"(\.|\,|\?|\!)([\w])", r"\1 \2", text)
    new_text = re.sub(r"\s+", " ", new_text)
    if new_text[-1] not in [".", ",", "?", "!"]:
        new_text += "."
    return new_text


def list2string(tokens: list, honorative, pronoun_from: str) -> str:
    """
    Преобразование списка токенов в строку
    Удаление слов гоноративов из строки

    :param tokens: Список токенов :type: list[Token, ...]
    :param honorative: слова гоноративы
    :param pronoun_from:
    :return:
    """
    punctuation = ",.?:;!'\"<>()-=@№#$%^&*|\/}{[]"

    string = ""
    for ind, token in enumerate(tokens):
        # условие нужно для того, чтобы убрать все слова гоноративы при обработке фразы ВЫ->ТЫ
        if token.lower() in honorative and pronoun_from == "вы":
            continue

        if ind == 0:
            string += token

        elif token in punctuation:
            string += token

        else:
            string += " " + token
    return string.strip()


def search_nsubj(head, pronoun_from) -> str:
    """
    Проход по всем зависимым словам вершины
    :param head:
    :param pronoun_from:
    :return: субъект (подлежащие). Если такого нет возвращает None
    """
    for child in head.children:
        if child.dep_ == "nsubj" or child.dep_ == "nsubj:pass":
            return child.text.lower()


def possessive_pronouns(
    word: Token,
    head: Token.head,
    word_parse,
    parse_head,
    pronoun_from,
    pr_from_number,
    reflexive_pronouns,
    all_forms_pronoun_sing,
    all_forms_pronoun_plur,
) -> str:
    """
    Обработка притяжательных и возвратно-притяжательных местоимений

    :param word:
    :param head:
    :param word_parse:
    :param parse_head:
    :param pronoun_from:
    :param pr_from_number:
    :param reflexive_pronouns:
    :param all_forms_pronoun_sing:
    :param all_forms_pronoun_plur:
    :return:
    """
    if pr_from_number == "sing" and word.text.lower() in all_forms_pronoun_sing:
        new_word = all_forms_pronoun_sing[word.text.lower()]
    elif pr_from_number == "plur" and word.text.lower() in all_forms_pronoun_plur:
        new_word = all_forms_pronoun_plur[word.text.lower()]
    else:
        new_word = word.text.lower()
    return new_word


def verbs_inpast(
    word: Token, head: Token.head, word_parse, pronoun_from, pr_to_number
) -> str:
    """
    Обработка глаголов(сказуемых) в прошедшем времени
    (в т.ч. вспомогательные-глаголы, глаголы-связки, однородные сказуемые и т.д.)

    :param word: An individual token — i.e. a word, punctuation symbol, whitespace, etc. :type: spacy.tokens.Token
    :param head:
    :param word_parse: :type: pymorphy2.analyzer.Parse
    :param pronoun_from:
    :param pr_to_number:
    :return:
    """
    new_word = None
    #  обработка простых сказуемых
    if word.dep_ == "ROOT":
        nsubj = search_nsubj(
            word, pronoun_from
        )  # возрвращает nsubj или nsubj:pass(подлежащее) - строка ,например "он", "ты" и т.д., если подлежащего нет - вернет  None).
        if nsubj == pronoun_from:
            new_word = word_parse.inflect({pr_to_number}).word

    #  обработка однородных сказуемых, а также частей сложных сказуемых - вспомогательных глаголов и глаголов-связок.
    if word.dep_ == "conj" or word.dep_ == "cop" or word.dep_ == "aux:pass":
        head_nsubj = search_nsubj(head, pronoun_from)

        if head_nsubj == pronoun_from:
            new_word = word_parse.inflect({pr_to_number}).word

    if new_word is None:
        new_word = word.text.lower()
    return new_word


def adject_part_mod_verb(
    word, head, parse_head, word_parse, pr_from_number, pronoun_from, pr_to_number
) -> str:
    """
    Обработка кратких причастий и прилагательных, а так же модальных глаголов

    :param word:
    :param head:
    :param parse_head:
    :param word_parse:
    :param pr_from_number:
    :param pronoun_from:
    :param pr_to_number:
    :return:
    """
    new_word = None

    nsubj = search_nsubj(
        word, pronoun_from
    )  # возрвращает nsubj или nsubj:pass(подлежащее), если подлежащего нет - вернет  None).

    if nsubj == pronoun_from or (
        "VERB" in parse_head.tag
        and pr_from_number in parse_head.tag
        and ("2per" in parse_head.tag or "impr" in parse_head.tag)
    ):
        new_word = word_parse.inflect({pr_to_number}).word

    if word.dep_ == "conj" and nsubj is None:
        head_nsubj = search_nsubj(head, pronoun_from)

        if head_nsubj == pronoun_from:
            new_word = word_parse.inflect({pr_to_number}).word

    if new_word is None:
        new_word = word.text.lower()
    return new_word


def honor(text, pronoun_from: str = "ты", pronoun_to: str = "вы") -> str:
    """
    Изменение формы обращения с "ты" на "вы" или наоборот

    >>> honor("Как твои дела?")
    'Как ваши дела?'

    >>> honor("Может вы хотели бы прокатиться?", "вы", "ты")
    'Может ты хотел бы прокатиться?'

    :param text: Преобразуемая строка
    :param pronoun_from: изначальная форма
    :param pronoun_to: итоговая форма
    :return: Обработанная строка
    """

    all_forms_pronoun_sing = your_sing
    all_forms_pronoun_plur = your_plur
    honorative = honoratives  # список слов гоноративов
    reflexive_pronouns = morph.parse("свой")[1]
    pr_from_parse = morph.parse(pronoun_from)[0]
    pr_to_parse = morph.parse(pronoun_to)[0]

    # число исходного и целевого местоимения
    pr_from_number = pr_from_parse.tag.number
    if pr_from_number == "sing":
        pr_to_number = "plur"
    if pr_from_number == "plur":
        pr_to_number = "sing"

    list_all_sents = []  # список, где хранятся все предложения

    # обработка пунктуации + удаление лишних пробелов
    text = punctuation_separator(text)

    doc = nlp(text.strip())
    for sentence in doc.sents:
        list_tokens = []
        # список для слов с заглавной буквы
        list_uppercase = [0 for i in sentence]

        for ind, word in enumerate(sentence):
            # список токенов текущего предложения
            list_tokens.append(word.text.lower())
            if word.text[0].isupper():
                # если слово начиналось с заглавной буквы, ставим 1
                list_uppercase[ind] = 1

            # разбор текущего слова
            word_parse = word_parser(word.text.lower(), word.lemma_)
            parse_head = word_parser(
                word.head.text.lower(), word.head.lemma_
            )  # разбор определяющего слова(вершины) - head

            # местоимения
            # личные:вы/ты
            if (
                "NPRO" in word_parse.tag
                and word.text.lower()
                == pr_from_parse.inflect({word_parse.tag.case}).word
            ):
                list_tokens[ind] = pr_to_parse.inflect({word_parse.tag.case}).word
                # для обработки устойчивого выражения "ух ты"
                for child in word.children:
                    if child.text.lower() == "ух":
                        list_tokens[ind] = word.text.lower()
                # притяжательные: ваш/ваша/ваше/твоя/твой/твое и тд. + # наречия по-вашему/по-твоему
            if (
                word.text.lower() in all_forms_pronoun_sing
                or word.text.lower() in all_forms_pronoun_plur
            ):
                list_tokens[ind] = possessive_pronouns(
                    word,
                    word.head,
                    word_parse,
                    parse_head,
                    pronoun_from,
                    pr_from_number,
                    reflexive_pronouns,
                    all_forms_pronoun_sing,
                    all_forms_pronoun_plur,
                )
            # глаголы
            if "VERB" in word_parse.tag and pr_from_number in word_parse.tag:
                # изъявит. наклон.(наст. вр.+ буд.вр. + буд. аналитич. вр.) + повелит. наклонение
                if "2per" in word_parse.tag or "impr" in word_parse.tag:
                    print({pr_to_number})
                    list_tokens[ind] = word_parse.inflect({pr_to_number}).word
                    print(list_tokens[ind])
                # прошед. вр.
                if "past" in word_parse.tag:
                    list_tokens[ind] = verbs_inpast(
                        word, word.head, word_parse, pronoun_from, pr_to_number
                    )

            # модал. гл. + краткие причастия + краткие прилагательные
            if (
                "ADJS" in word_parse.tag or "PRTS" in word_parse.tag
            ) and pr_from_number in word_parse.tag:
                list_tokens[ind] = adject_part_mod_verb(
                    word,
                    word.head,
                    parse_head,
                    word_parse,
                    pr_from_number,
                    pronoun_from,
                    pr_to_number,
                )

        for ind, el in enumerate(list_uppercase):
            if el == 1:
                list_tokens[ind] = list_tokens[ind].title()
        list_all_sents.extend(list_tokens)

    # преобразуем список токенов в строку(удаляем гоноративы)
    new_string = list2string(list_all_sents, honorative, pronoun_from)
    return new_string
