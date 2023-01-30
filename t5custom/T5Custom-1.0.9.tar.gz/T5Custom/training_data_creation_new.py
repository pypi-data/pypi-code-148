import pandas as pd
import random
import string

df = pd.DataFrame(data={"Sentences": [None], "UseCase": [None], "classifications": [None]})


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_training_data():
    global df
    usecases = ["range", "null_check", "date", "number", "length", "comparison"]

    for usecase in usecases:
        if usecase == "range":
            for i in range(0, 200):
                num1 = random.randint(0, 9999)
                num2 = random.randint(0, 99999)
                name = get_random_string(6)
                Sentences = ["%s should not be greater than %d ,but less than %d" % (name, num2, num1),
                             "%s must be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s could be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s is more than %d ,but less than %d" % (name, num1, num2),
                             "%s is greater than %d,but less than %d" % (name, num1, num2),
                             "%s must be greater than %d,but less than  %d" % (name, num1, num2),
                             "%s exceeds %d,but does not exceeds %d" % (name, num1, num2),
                             "%s could be less than %d and more than %d" % (name, num1, num2),
                             "%s might be in between %d to %d" % (name, num1, num2),
                             "%s can be in range %d to %d" % (name, num1, num2),
                             "%s is with in %d to %d" % (name, num1, num2),
                             "%s must be in between %d to %d" % (name, num1, num2),
                             "%s is more than %d and also %s should not exceed %d" % (name, num1, name, num2),
                             "%s is comprised between %d, excluded, and %d" % (name, num1, num2),
                             "%s is strictly greater than %d and strictly lower than %d" % (name, num1, num2),
                             "%s equals a number under %d and over %d" % (name, num1, num2),
                             "%s shall be found somewhere between %d and %d" % (name, num1, num2)
                             ]
                if num1 > num2:
                    temp = num2
                    num2 = num1
                    num1 = temp
                for Sentence in Sentences:
                    expected_use_case = "Value is_within(%d,%d)" % (num1, num2)
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "null_check":
            null_not_null = ["not_null", "is_null"]
            for null_case in null_not_null:
                if null_case == "not_null":
                    for i in range(0, 200):
                        name = get_random_string(6)
                        Sentences = ["%s cannot be null" % name,
                                     "%s is not null" % name,
                                     "%s can not be equal to null" % name,
                                     "%s can not be left empty" % name,
                                     "%s cannot be empty" % name,
                                     "%s is not empty" % name,
                                     "%s can not be equal to empty" % name,
                                     "%s can not be left blank" % name,
                                     "%s cannot be blank" % name,
                                     "%s is not blank" % name,
                                     "%s can not be equal to blank" % name,
                                     "%s could not be equal to blank" % name,
                                     "%s must not be blank" % name,
                                     "%s must not be empty" % name,
                                     "%s must not be null" % name,
                                     "%s should not be empty" % name,
                                     "%s should not be null" % name,
                                     "%s should not be blank" % name,
                                     "%s could not be empty" % name,
                                     "%s could not be null" % name,
                                     "%s could not be blank" % name,
                                     "%s would not be empty" % name,
                                     "%s would not be null" % name,
                                     "%s would not be blank" % name,
                                     "%s isn't empty" % name,
                                     "%s number should not be null" % name,
                                     "%s depth must not be null" % name,
                                     "%s is not null" % name,
                                     "%s could not be null" % name,
                                     "%s is not a null" % name,
                                     "%s mustn't be null" % name,
                                     "%s mustn't be empty" % name,
                                     "%s mustn't be an empty string" % name,
                                     "%s cannot be null" % name,
                                     "%s can't be a null" % name,
                                     "%s cannot be empty" % name,
                                     "%s can't be a empty" % name,
                                     "%s is expected to be not null" % name,
                                     "%s is required to be not null" % name,
                                     "%s is expected to be not empty" % name,
                                     "%s is required to be not empty" % name,
                                     "%s should have a expired indicator" % name,
                                     "A business associate credit check has the source of the check",
                                     "%s should have a lithology description" % name,
                                     "%s must have a non-null loan number" % name,
                                     "%s has some values" % name,
                                     "%s cannot have any characters" % name,
                                     "%s is always NOT NULL" % name,
                                     "Lets say %s cannot have null values" % name,
                                     "%s field cannot be blank or empty" % name,
                                     "%s should contain something" % name,
                                     "%s must be populated" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input Data != 'NULL' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif null_case == "is_null":
                    for i in range(0, 200):
                        name = get_random_string(6)
                        Sentences = ["%s can be null" % name,
                                     "%s is null" % name,
                                     "%s can be equal to null" % name,
                                     "%s can be left empty" % name,
                                     "%s can be empty" % name,
                                     "%s is empty" % name,
                                     "%s can be equal to empty" % name,
                                     "%s can be left blank" % name,
                                     "%s can be blank" % name,
                                     "%s is blank" % name,
                                     "%s can be equal to blank" % name,
                                     "%s could be equal to blank" % name,
                                     "%s must be blank" % name,
                                     "%s must be empty" % name,
                                     "%s must be null" % name,
                                     "%s should be empty" % name,
                                     "%s should be null" % name,
                                     "%s should be blank" % name,
                                     "%s could be empty" % name,
                                     "%s could be null" % name,
                                     "%s could be blank" % name,
                                     "%s would be empty" % name,
                                     "%s would be null" % name,
                                     "%s would be blank" % name,
                                     "%s is empty" % name,
                                     "%s number should be null" % name,
                                     "%s depth must be null" % name,
                                     "%s is null" % name,
                                     "%s could be null" % name,
                                     "%s is a null" % name,
                                     "%s must be null" % name,
                                     "%s must be empty" % name,
                                     "%s must be an empty string" % name,
                                     "%s can be null" % name,
                                     "%s can be a null" % name,
                                     "%s can be empty" % name,
                                     "%s can be a empty" % name,
                                     "%s is expected to be null" % name,
                                     "%s is required to be null" % name,
                                     "%s is expected to be empty" % name,
                                     "%s is required to be empty" % name,
                                     "%s should not have a expired indicator" % name,
                                     "%s should not have a lithology description" % name,
                                     "%s must have a null loan number" % name,
                                     "%s has not some values" % name,
                                     "%s can not have any characters" % name,
                                     "%s is always NULL" % name,
                                     "Lets say %s have null values" % name,
                                     "%s field can not be blank or empty" % name,
                                     "%s should not contain something" % name,
                                     "%s must not be populated" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input Data = 'NULL' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "date":
            date = ["is_date", "is_not_date"]
            for date_case in date:
                if date_case == "is_date":
                    for i in range(0, 200):
                        name = get_random_string(6)
                        Sentences = ["%s can have values of type DATE only" % name,
                                     "%s can only be of type date" % name,
                                     "%s consists of a DATE" % name,
                                     "%s describes date" % name,
                                     "%s is comprised of a DATE" % name,
                                     "%s is equivalent to date" % name,
                                     "%s represents a date" % name,
                                     "%s represents a specific day, month and year" % name,
                                     "%s shall be 'DATE'" % name,
                                     "%s should contain the value of date" % name,
                                     "%s is equal to the value of date" % name,
                                     "%s may contain the value of date" % name,
                                     "%s is of value date" % name,
                                     "%s can only hold date data type" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) = 'DATE' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif date_case == "is_not_date":
                    for i in range(0, 200):
                        name = get_random_string(6)
                        Sentences = ["%s isn't a date" % name,
                                     "%s is not a date" % name,
                                     "%s must not be a date" % name,
                                     "%s mustn't be date" % name,
                                     "%s should not be date" % name,
                                     "%s should not be of type date" % name,
                                     "%s shouldn't be a date" % name,
                                     "%s isn't of type date" % name,
                                     "%s may not contain the value of date" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) != 'DATE' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "number":
            numbers = ["is_number", "is_not_number"]
            for number_case in numbers:
                if number_case == "is_number":
                    for i in range(0, 200):
                        name = get_random_string(6)
                        Sentences = ["%s must be of type integer" % name,
                                     "%s should be of type integer" % name,
                                     "%s must be a smallint" % name,
                                     "%s is number" % name,
                                     "%s must be of integer type" % name,
                                     "%s must be a smallint" % name,
                                     "%s Advances must be a whole number" % name,
                                     "%s Before Modification must be an integer" % name,
                                     "%s is number" % name,
                                     "%s is a number" % name,
                                     "%s should be a number" % name,
                                     "%s is of type number" % name,
                                     "%s must be of type number" % name,
                                     "%s must be of a type number" % name,
                                     "%s should be of type number" % name,
                                     "%s should be of a type number" % name,
                                     "%s needs to be of type number" % name,
                                     "%s must be a smallint" % name,
                                     "%s is a NUMBER" % name,
                                     "%s is a type number" % name,
                                     "The value of %s can only be number" % name,
                                     "%s is a value which is numerical" % name,
                                     "%s is always a number" % name,
                                     "%s is comprised by a number" % name,
                                     "%s must be numeric" % name,
                                     "%s belongs to numeric" % name,
                                     "%s is equal to numeric" % name,
                                     "%s can be numeric values" % name,
                                     "%s can have numerals" % name,
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) = 'NUMBER' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif number_case == "is_not_number":
                    for i in range(0, 200):
                        name = get_random_string(5)
                        Sentences = ["%s isn't a number" % name,
                                     "%s is not a number" % name,
                                     "%s mustn't be a number" % name,
                                     "%s should not be a number" % name,
                                     "%s isn't of type number" % name,
                                     "%s isn't of a type number" % name,
                                     "%s is not of a type number" % name,
                                     "%s must not be of type number" % name,
                                     "%s should not be of a type number" % name,
                                     "%s shouldn't be of type number" % name,
                                     "%s is not of type integer" % name,
                                     "%s shouldn't be of type number" % name,
                                     "%s should not be of type number" % name,
                                     "%s cannot contain numerals" % name,
                                     "%s may not contain numeral" % name
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Type(Input) != 'NUMBER' THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "length":
            length = ["=", "!=", "<", "<=", ">", ">="]
            for use_case_length in length:
                if use_case_length == "=":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = ["length of %s can be equal to %d" % (name, num),
                                     "length of %s is equal to %d" % (name, num),
                                     "length of %s is %d" % (name, num),
                                     "length of %s must be %d" % (name, num),
                                     "length of %s should be equal to %d" % (name, num),
                                     "length of %s must be equal to %d" % (name, num),
                                     "length of %s should be %d" % (name, num),
                                     "length of %s could be equal to %d" % (name, num),
                                     "%s is %d characters long" % (name, num),
                                     "%s is %d digits" % (name, num),
                                     "%s is %d characters long" % (name, num),
                                     "%s %d characters long" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) = '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "!=":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = [
                            "length of %s can not be equal to %d" % (name, num),
                            "length of %s is not equal to %d" % (name, num),
                            "length of %s is not %d" % (name, num),
                            "length of %s must not be %d" % (name, num),
                            "length of %s should not be equal to %d" % (name, num),
                            "length of %s must not be equal to %d" % (name, num),
                            "length of %s should not be %d" % (name, num),
                            "length of %s could not be equal to %d" % (name, num),
                            "%s isn't %d characters long" % (name, num),
                            "%s isn't %d digits" % (name, num),
                            "%s is not %d characters long" % (name, num),
                            "%s is not %d digits" % (name, num),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) != '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "<":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = [
                            "%s must be shorter than %d characters" % (name, num),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) < '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == "<=":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = [
                            "Length of % s is less than or equal to % d characters" % (name, num),
                            "%s should be less than or equal to %d characters" % (name, num),
                            "%s must be less than or equal to %d characters" % (name, num),
                            "Length of %s is less than or equal to %d characters" % (name, num),
                            "%s must be less than or equal to %d characters" % (name, num),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) <= '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == ">":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = [
                            "%s needs to be longer than %d characters" % (name, num),
                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) > '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                if use_case_length == ">=":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        name2 = get_random_string(6)
                        Sentences = [

                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Length(Input) >= '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        elif usecase == "comparison":
            comparison = ['comparison_equal_to', 'comparison_not_equal_to', 'comparison_less_than',
                          'comparison_less_than_equal_to', 'comparison_greater_than',
                          'comparison_greater_than_equal_to', 'neg_comparison', 'pos_comparison']
            for comparison_use_case in comparison:
                if comparison_use_case == "comparison_equal_to":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(6)
                        Sentences = ["Water depth is %d" % num,
                                     "%s is %d" % (name, num),
                                     "%s should be %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s is be %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s is equal %d" % (name, num),
                                     "%s should be - %d" % (name, num),
                                     "%s cannot be greater than or less than %d" % (name, num),
                                     "The value of %s is %d" % (name, num),
                                     "The value of %s must be %d" % (name, num),
                                     "The value of %s is %d" % (name, num),
                                     "%s is %d" % (name, num),
                                     "%s is equal %d" % (name, num),
                                     "%s is equal to %d" % (name, num),
                                     "%s must be %d" % (name, num),
                                     "%s MUST BE A %d" % (name, num),
                                     "%s must be equals to %d" % (name, num),
                                     "%s must be exactly %d" % (name, num),
                                     "%s must be just %d" % (name, num),
                                     "%s should be %d" % (name, num),
                                     "%s should be equal to %d" % (name, num),
                                     "%s should be equals to %d" % (name, num),
                                     "%s value is %d" % (name, num),
                                     "The value of %s equals %d" % (name, num),
                                     "The value of %s is the same as %d" % (name, num),
                                     "Value of %s should be equals to %d" % (name, num)
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input = %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_not_equal_to":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        Sentences = ["%s longitude should not be %d" % (name, num),
                                     "%s does not equal %d" % (name, num),
                                     "%s not equals to %d" % (name, num),
                                     "%s can be anything but %d" % (name, num),
                                     "%s can be anything other than %d" % (name, num),
                                     "%s should n't hold equal to %d" % (name, num),
                                     "%s can't have a value of %d" % (name, num),
                                     "%s does not consist of %d" % (name, num),
                                     "%s is not %d" % (name, num),
                                     "%s must not be equal to %d" % (name, num),
                                     "%s must not be %d" % (name, num),
                                     "%s can not be %d" % (name, num),
                                     "%s can't be %d" % (name, num),
                                     "%s can not be equal to %d" % (name, num),
                                     "%s is not able to equal %d" % (name, num),
                                     "%s is not equal to %d" % (name, num),
                                     "%s may not be %d" % (name, num),
                                     "%s must not be equal %d" % (name, num),
                                     "%s must not be equals to %d" % (name, num),
                                     "%s shall not be %d" % (name, num),
                                     "%s should not be %d" % (name, num),
                                     "%s should not be equal to %d" % (name, num),
                                     "%s should not be equals to %d" % (name, num),
                                     "%s must not be  %d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input != %d THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                        df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_less_than":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        name2 = get_random_string(5)
                        Sentences = [

                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input < '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_less_than_equal_to":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        name2 = get_random_string(5)
                        Sentences = [

                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input <= '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_greater_than":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        name2 = get_random_string(5)
                        Sentences = [

                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input > '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "comparison_greater_than_equal_to":
                    for i in range(0, 200):
                        num = random.randint(0, 9999)
                        name = get_random_string(5)
                        name2 = get_random_string(5)
                        Sentences = [

                        ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input >= '%d' THEN TRUE" % num
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "neg_comparison":
                    for i in range(0, 200):
                        name = get_random_string(5)
                        num = random.randint(0, 9999)
                        Sentences = ["%s can be negative" % name,
                                     "%s is a negative number" % name,
                                     "%s is negative" % name,
                                     "%s is -%d or not a positive number" % (name, num),
                                     "%s is not positive or not 0" % name,
                                     "%s is not positive or not zero" % name,
                                     "%s can not be positive" % name,
                                     "%s is not a positive number" % name,
                                     "%s is not positive " % name,
                                     "%s is negative or -%d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input < 0 THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
                elif comparison_use_case == "pos_comparison":
                    for i in range(0, 200):
                        name = get_random_string(5)
                        num = random.randint(0, 9999)
                        Sentences = ["%s can not be negative" % name,
                                     "%s is not a negative number" % name,
                                     "%s is not negative" % name,
                                     "%s is %d or a positive number" % (name, num),
                                     "%s is positive or 0" % name,
                                     "%s is positive or zero" % name,
                                     "%s can be positive" % name,
                                     "%s is a positive number" % name,
                                     "%s is positive " % name,
                                     "%s is not negative or not -%d" % (name, num),
                                     ]
                        for Sentence in Sentences:
                            expected_use_case = "IF Input >= 0 THEN TRUE"
                            df1 = pd.DataFrame(
                                {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                            if len(df.dropna()) == 0:
                                df = df1
                            df = pd.concat([df, df1])
        print("Data creating started for :%s ,data size %d" % (usecase, len(df.dropna())))
    b_size_df = len(df)
    df.sort_values("Sentences", inplace=True)
    df.drop_duplicates(subset="Sentences", keep=False, inplace=True)
    df.to_csv("datasets/generated_training.csv", mode='w', index=False)
    a_size_df = len(df)
    print("before removing duplicate from df: %d and after removed duplicates size is : %d" % (b_size_df, a_size_df))
