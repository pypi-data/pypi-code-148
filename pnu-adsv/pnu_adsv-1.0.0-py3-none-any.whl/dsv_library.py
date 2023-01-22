#!/usr/bin/env python3
""" adsv - Analyze delimiter-separated values files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import csv
from enum import Enum
import logging
import os
import re

from .file_utilities import get_file_encoding, get_file_line_terminator
from .string_utilities import get_string_type_and_value

LINES_TO_SCAN = 30
CHUNK_SIZE = 16384


####################################################################################################
def get_dsv_delimiter(filename, encoding="utf-8"):
    """ Assuming the filename is a CSV file, try to guess its delimiter and end-of-line type """
    if not os.path.isfile(filename):
        return ""

    class State(Enum):
        """ Possible states of our custom CSV file parser """
        NOT_QUOTED = 1
        IN_SQUOTES = 2
        OUT_SQUOTES = 3
        IN_DQUOTES = 4
        OUT_DQUOTES = 5

    # Count the special characters that could be delimiters
    # in the LINES_TO_SCAN sample
    characters = {}
    with open(filename, "r", encoding=encoding, errors="ignore") as file:
        line = file.readline()
        line_number = 1
        characters[0] = {}
        state = State.NOT_QUOTED
        while line and line_number <= LINES_TO_SCAN:
            for character in line:
                if state == State.NOT_QUOTED:
                    if character == "'":
                        state = State.IN_SQUOTES
                    elif character == '"':
                        state = State.IN_DQUOTES
                    elif not character.isalnum() and character != '\n':
                        if character in characters[line_number - 1].keys():
                            characters[line_number - 1][character] += 1
                        else:
                            characters[line_number - 1][character] = 1
                elif state == State.IN_SQUOTES:
                    if character == "'":
                        state = State.OUT_SQUOTES
                elif state == State.OUT_SQUOTES:
                    if character == "'":
                        state = State.IN_SQUOTES
                    else:
                        state = State.NOT_QUOTED
                        if character not in ("'", '"', '\n'):
                            if character in characters[line_number - 1].keys():
                                characters[line_number - 1][character] += 1
                            else:
                                characters[line_number - 1][character] = 1
                elif state == State.IN_DQUOTES:
                    if character == '"':
                        state = State.OUT_DQUOTES
                elif state == State.OUT_DQUOTES:
                    if character == '"':
                        state = State.IN_DQUOTES
                    else:
                        state = State.NOT_QUOTED
                        if character not in ("'", '"', '\n'):
                            if character in characters[line_number - 1].keys():
                                characters[line_number - 1][character] += 1
                            else:
                                characters[line_number - 1][character] = 1

            if state not in (State.IN_SQUOTES, State.IN_DQUOTES):
                state = State.NOT_QUOTED
                characters[line_number] = {}
                line_number += 1

            line = file.readline()

    # Identify the special characters that appear in the same quantity
    # than in the first (headers?) line
    candidates = {}
    for i in range(1, LINES_TO_SCAN):
        for character in characters[i]:
            if character in characters[0] \
            and characters[i][character] == characters[0][character]:
                if character in candidates:
                    candidates[character] += 1
                else:
                    candidates[character] = 1

    # Select the one with the highest count of occurrences
    highest_count = 0
    best_candidate = ""
    for character, count in candidates.items():
        logging.debug("Delimiter candidate: character='%s', count='%d'", character, count)
        if character not in ('\r', '\n') \
        and count > highest_count:
            highest_count = count
            best_candidate = character

    return best_candidate


####################################################################################################
def analyze_dsv_file(
    filename,
    delimiter="",
    encoding="",
    ):
    """ Analyze the data in a CSV file """
    analysis = {}

    if not os.path.isfile(filename):
        logging.error("'%s' is not accessible", filename)
        return analysis

    # Try to identify the encoding of the file
    if not encoding:
        analysis["encoding"] = get_file_encoding(filename)
        if not analysis["encoding"]:
            analysis["encoding"] = "utf-8"
    else:
        analysis["encoding"] = encoding

    # Try to identify the CSV dialect and the presence of a headers line
    with open(filename, newline='', encoding=analysis["encoding"], errors="ignore") as csv_file:
        try:
            dialect = csv.Sniffer().sniff(csv_file.read(CHUNK_SIZE))
            analysis['delimiter'] = dialect.delimiter
            analysis['doublequote'] = dialect.doublequote
            analysis['quotechar'] = dialect.quotechar
            analysis['escapechar'] = dialect.escapechar
            analysis['lineterminator'] = dialect.lineterminator
        except:
            analysis['delimiter'] = ''
            analysis['doublequote'] = ''
            analysis['quotechar'] = ''
            analysis['escapechar'] = ''
            analysis['lineterminator'] = ''

        csv_file.seek(0)

        try:
            analysis["has headers"] = csv.Sniffer().has_header(csv_file.read(CHUNK_SIZE))
        except:
            analysis["has headers"] = False

    # Override delimiter if requested
    if delimiter:
        analysis['delimiter'] = delimiter

    # Try on our own if still unknown
    if not analysis['delimiter']:
        analysis['delimiter'] = get_dsv_delimiter(filename, encoding=analysis["encoding"])
    if not analysis['lineterminator']:
        analysis['lineterminator'] = get_file_line_terminator(filename)

    # Now we read the file, taking note of the number of lines, the number of fields,
    # the headers (if present) and the count of distinct values for each field
    analysis["lines"] = 0
    analysis["fields"] = 0
    analysis["headers"] = []
    analysis["distinct values"] = {}
    with open(filename, newline='', encoding=analysis["encoding"], errors="ignore") as csv_file:
        lines = csv.reader(csv_file, delimiter=analysis['delimiter'])
        for line in lines:
            analysis["lines"] += 1
            if not analysis["fields"]:
                analysis["fields"] = len(line)
            elif len(line) != analysis["fields"]:
                logging.error(
                    "Line #%d has %d fields instead of %d!",
                    analysis['lines'],
                    len(line),
                    analysis['fields']
                    )

            if analysis["lines"] == 1 and analysis["has headers"]:
                analysis["headers"] = line
            else:
                for i in range(len(line)):
                    if i in analysis["distinct values"]:
                        if line[i] in analysis["distinct values"][i]:
                            analysis["distinct values"][i][line[i]] += 1
                        else:
                            analysis["distinct values"][i][line[i]] = 1
                    else:
                        analysis["distinct values"][i] = {}
                        analysis["distinct values"][i][line[i]] = 1

    return analysis


####################################################################################################
def print_dsv_file_analysis(
    filename,
    delimiter="",
    encoding="",
    hide_threshold="0.2",
    max_lines=-1,
    min_count=-1,
    top_lines=5,
    ):
    """ Print the data analysis of a CSV file """
    if not os.path.isfile(filename):
        logging.error("'%s' is not accessible", filename)
        return 1

    analysis = analyze_dsv_file(filename, delimiter=delimiter, encoding=encoding)

    print(f"Filename='{filename}':")
    print(f"  Encoding='{analysis['encoding']}'")
    print( "  CSV dialect:")
    print(f"    Delimiter={repr(analysis['delimiter'])}")
    print(f"    Doublequote={analysis['doublequote']}")
    print(f"    Quote character={analysis['quotechar']}")
    print(f"    Escape character={analysis['escapechar']}")
    print(f"    Line terminator={repr(analysis['lineterminator'])}")
    print(f"  Has headers={analysis['has headers']}")
    print(f"  Lines={analysis['lines']:,}")
    print(f"  Fields={analysis['fields']:,}")

    # Maximum width of counts including Thousand separators
    padding = len(str(analysis['lines'])) + (len(str(analysis['lines'])) // 3)

    for i in range(analysis['fields']):
        print()
        if analysis['has headers']:
            print(f"  Field #{i + 1} '{analysis['headers'][i]}':")
        else:
            print(f"  Field #{i + 1}:")
        print(f"    Distinct values={len(analysis['distinct values'][i]):,}")

        # Values type (we'll use it for sorting records if they are not strings)
        value_type = ""
        altvalues = {}
        for value in analysis['distinct values'][i]:
            new_value_type = ""

            new_value_type, new_value = get_string_type_and_value(value)

            if not value_type:
                if value:
                    value_type = new_value_type
            elif value_type != new_value_type:
                if value:
                    value_type = "str"
                    break

            if value:
                altvalues[new_value] = value

        if not value_type:
            value_type = "str"

        if value_type == "int":
            print("    Values type=integer")
        elif value_type == "float":
            print("    Values type=float")
        elif value_type == "datetime":
            print("    Values type=date and time")
        else:
            print("    Values type=string")

        print("    Values count:")
        if len(analysis["distinct values"][i]) >= int(analysis["lines"] * hide_threshold):
            print("      ... Number of distinct values exceeds display threshold ...")
        else:
            line_no = 0
            for value, count in dict(sorted(
                analysis["distinct values"][i].items(),
                key=lambda item: item[1],
                reverse=True
                )).items():
                if max_lines != -1 and line_no >= max_lines:
                    print("      ... Too many values to display ...")
                    break

                if count >= min_count:
                    print(f"      {count:>{padding},} '{value}'")

                line_no += 1

        print("    Values range:")
        if len(analysis["distinct values"][i]) > 2 * top_lines:
            if value_type == "str":
                for value in sorted(analysis["distinct values"][i].keys())[:top_lines]:
                    if '\r' in value or '\n' in value:
                        value = re.sub(r"(\r|\n).*", "", value)
                        print(
                            f"      '{value}'"
                            + " ... Only showing first line of multi-lines values ..."
                            )
                    else:
                        print(f"      '{value}'")
                print("      ...")
                for value in sorted(analysis["distinct values"][i].keys())[-1 * top_lines:]:
                    if '\r' in value or '\n' in value:
                        value = re.sub(r"(\r|\n).*", "", value)
                        print(
                            f"      '{value}'"
                            + " ... Only showing first line of multi-lines values ..."
                            )
                    else:
                        print(f"      '{value}'")
            else:
                for new_value in sorted(altvalues.keys())[:top_lines]:
                    print(f"      '{altvalues[new_value]}'")
                print("      ...")
                for new_value in sorted(altvalues.keys())[-1 * top_lines:]:
                    print(f"      '{altvalues[new_value]}'")
        else:
            if value_type == "str":
                for value in sorted(analysis["distinct values"][i].keys())[:2 * top_lines]:
                    if '\r' in value or '\n' in value:
                        value = re.sub(r"(\r|\n).*", "", value)
                        print(
                            f"      '{value}'"
                            + " ... Only showing first line of multi-lines values ..."
                            )
                    else:
                        print(f"      '{value}'")
            else:
                for new_value in sorted(altvalues.keys())[:2 * top_lines]:
                    print(f"      '{altvalues[new_value]}'")

    return 0


####################################################################################################
def print_dsv_fields(
    filename,
    fields,
    delimiter="",
    encoding="",
    flatten=False,
    ):
    """ Print the requested fields delimiter-separated """
    if not os.path.isfile(filename):
        logging.error("'%s' is not accessible", filename)
        return 1

    analysis = analyze_dsv_file(filename, delimiter=delimiter, encoding=encoding)

    with open(filename, newline='', encoding=analysis["encoding"], errors="ignore") as csv_file:
        lines = csv.reader(csv_file, delimiter=analysis['delimiter'])
        for line in lines:
            insert_delimiter = False
            for field in fields:
                if field - 1 <= len(line):
                    field_value = line[field - 1]
                    if insert_delimiter:
                        print(analysis['delimiter'], end="")

                    if analysis["delimiter"] in field_value \
                    or analysis["quotechar"] in field_value \
                    or '\r' in field_value \
                    or '\n' in field_value \
                    or (analysis["escapechar"] is not None \
                    and analysis["escapechar"] in field_value):
                        print(analysis["quotechar"], end="")

                        if analysis["quotechar"] in field_value:
                            if analysis["doublequote"]:
                                field_value = field_value.replace(
                                    analysis["quotechar"],
                                    analysis["quotechar"] * 2
                                    )
                            elif analysis["escapechar"] is not None:
                                field_value = field_value.replace(
                                    analysis["quotechar"],
                                    analysis["escapechar"] + analysis["quotechar"]
                                    )
                            else:
                                field_value = field_value.replace(
                                    analysis["quotechar"],
                                    analysis["quotechar"] * 2
                                    )
                                logging.warning("EscapeChar is undefined while DoubleQuote is False")
                                logging.info("Changing DoubleQuote to True")
                                analysis["doublequote"] = True

                        if flatten:
                            if '\r' in field_value:
                                field_value = field_value.replace('\r', '\\r')
                            if '\n' in field_value:
                                field_value = field_value.replace('\n', '\\n')

                        if (analysis["escapechar"] is not None \
                        and analysis["escapechar"] in field_value):
                            field_value = field_value.replace(
                                analysis["escapechar"],
                                analysis["escapechar"] * 2
                                )

                        print(field_value, end="")
                        print(analysis["quotechar"], end="")
                    else:
                        print(field_value, end="")

                    insert_delimiter = True

            print(analysis['lineterminator'], end="")

    return 0
