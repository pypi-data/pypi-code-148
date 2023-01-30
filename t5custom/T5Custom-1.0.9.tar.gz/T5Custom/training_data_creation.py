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
    global df, df1
    usecases = ["range", "is_null", "not_null", "is_date", "is_not_date", "is_number", "is_not_number",
                "is_not_length", "is_length", "length", "is_not_comparison", "is_comparison", "comparison",
                "pos_neg_comparison"]

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
        elif usecase == "not_null":
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
                    expected_use_case = "VALUE is_not_equals to null"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_null":
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
                    expected_use_case = "VALUE is_equals to null"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_date":
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
                    expected_use_case = "VALUE is_equal to DATE"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_not_date":
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
                    expected_use_case = "VALUE is_not_equal to DATE"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_number":
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
                    expected_use_case = "VALUE is_equal to number"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_not_number":
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
                    expected_use_case = "VALUE is_not_equal to number"
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "length":
            for i in range(0, 200):
                num1 = random.randint(0, 9999)
                name = get_random_string(6)
                name2 = get_random_string(6)
                Sentences = ["Length of %s is less than or equal to %d characters" % (name, num1),
                             "%s should be less than or equal to %d characters" % (name, num1),
                             "%s must be less than or equal to %d characters" % (name, num1),
                             "Length of %s is less than or equal to %d characters" % (name, num1),
                             "%s must be less than or equal to %d characters" % (name, num1),

                             "%s must be shorter than %d characters" % (name, num1),
                             "%s needs to be longer than %d characters" % (name, num1),
                             "%s must be at least %d characters" % (name, num1),
                             "%s must be at most %d characters" % (name, num1),
                             "%s must be at most %d characters long" % (name, num1),
                             "%s must not be longer than %d characters" % (name, num1),
                             "%s may not be longer than %d characters" % (name, num1),
                             "%s must not be longer than %d characters" % (name, num1),
                             "%s must not be longer than %d symbols" % (name, num1),
                             "%s must not be longer than %d letters and digits" % (name, num1),
                             "%s must be less than or equal to %d characters" % (name, num1),
                             "%s must not be greater than %d characters" % (name, num1),
                             "%s must be shorter than %d characters" % (name, num1),
                             "%s should be less than or equal to %d characters" % (name, num1),
                             "%s should be %d characters" % (name, num1),
                             "%s must have a maximum of %d characters" % (name, num1),
                             "%s consists of either % d characters or less than % d characters" % (name, num1, num1),
                             "%s has either %d characters or less than %d characters" % (name, num1, num1),
                             "%s number of characters of %s should be more than % d" % (name, name2, num1),
                             "%s length is higher than %d" % (name, num1),
                             "%s length is necessarily greater than %d" % (name, num1),
                             "%s length of %s is always greater than %d" % (name, name2, num1),
                             "%s length of %s is bigger than %d" % (name, name2, num1),
                             "%s length of %s must be bigger than %d" % (name, name2, num1),
                             "%s length of %s should be bigger than %d" % (name, name2, num1),
                             "%s length of %s surpasses %d" % (name, name2, num1),
                             "%s consists of more than %d characters %d" % (name, num1, num1),
                             "%s contains more than %d characters" % (name, num1),
                             "%s has at least %d elements" % (name, num1),
                             "%s is as long as or longer than %d" % (name, num1),
                             "%s is comprised of more than %d characters or %d characters" % (name, num1, num1),
                             "%s length of %s is inferior to %d" % (name, name2, num1),
                             "%s length of %s is under %d" % (name, name2, num1),
                             "%s length of %s should measure below %d characters" % (name, name2, num1),
                             "%s number of characters of %s is lower than %d" % (name, name2, num1),
                             "%s length of %s is no more than %d" % (name, name2, num1),
                             "%s number of characters of %s should be more than %d" % (name, name2, num1),
                             "%s length cannot be greater than %d" % (name, num1),
                             "%s must not exceed % d characters" % (name, num1),
                             "%s needs to be longer than %d characters" % (name, num1),
                             "%s length cannot be equal to %d" % (name, num1),
                             "Character length of %s is not equal to %d" % (name, num1),
                             "%s can not be %d characters long" % (name, num1),
                             "Length of %s must be at least %d" % (name, num1),
                             "Length of %s must not exceed %d" % (name, num1),
                             "Length of %s must not exceed %d characters" % (name, num1),
                             "Length of %s is not %d" % (name, num1),
                             "Length of %s can not be equals to %d" % (name, num1),
                             "Length of %s must not be equals to %d" % (name, num1),
                             "Length of %s should definitely not equal to %d" % (name, num1),
                             "Character Length of %s is lower than %d" % (name, num1),
                             "Length of %s is smaller or equal to %d" % (name, num1),
                             "Character count of %s is %d or lower" % (name, num1),
                             "%s must not be greater than %d characters" % (name, num1),
                             "%s must not be longer than %d characters" % (name, num1),
                             "%s must not be longer than %d symbol" % (name, num1),
                             ]
                for Sentence in Sentences:
                    expected_use_case = "Value is_length(%d)" % num1
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_not_length":
            for i in range(0, 200):
                num = random.randint(0, 9999)
                name = get_random_string(5)
                Sentences = ["length of %s can not be equal to %d" % (name, num),
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
                    expected_use_case = "VALUE is_not_equal to length(%d)" % num
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                df = pd.concat([df, df1])
        elif usecase == "is_length":
            for i in range(0, 200):
                num = random.randint(0, 9999)
                name = get_random_string(5)
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
                    expected_use_case = "VALUE is_equal to length(%d)" % num
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_comparison":
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
                             "%s should be -%d" % (name, num),
                             "%s should be -%d" % (name, num),
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
                    expected_use_case = "VALUE is_equal to comparison(%d)" % num
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "is_not_comparison":
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
                    expected_use_case = "VALUE is_not_equal to comparison(%d)" % num
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                df = pd.concat([df, df1])
        elif usecase == "comparison":
            for i in range(0, 200):
                num = random.randint(0, 9999)
                name = get_random_string(5)
                name2 = get_random_string(5)
                Sentences = ["%s is n't permitted to be %d" % (name, num),
                             "%s is more or less than %d" % (name, num),
                             "%s must be anything but %d" % (name, num),
                             "%s is greater than or less than %d" % (name, num),
                             "%s is a number other than %d" % (name, num),
                             "%s is a value other than %d" % (name, num),
                             "%s is any number except %d" % (name, num),
                             "%s is different than %d" % (name, num),
                             "%s must be a value other than %d" % (name, num),
                             "%s must be other than %d" % (name, num),
                             "%s must have value other than %d" % (name, num),
                             "%s can not be %d or more" % (name, num),
                             "%s is less than %d" % (name, num),
                             "%s is smaller than %d" % (name, num),
                             "%s must be less than %d" % (name, num),
                             "%s must be smaller than %d" % (name, num),
                             "%s should be less than %d" % (name, num),
                             "%s should be smaller than %d" % (name, num),
                             "%s is fewer than %d" % (name, num),
                             "%s consists of a number lower than %d" % (name, num),
                             "%s equals a number lower than %d" % (name, num),
                             "%s equals a number under %d" % (name, num),
                             "%s falls under %d" % (name, num),
                             "%s has a value it is less than %d" % (name, num),
                             "%s holds a number it is lower than %d" % (name, num),
                             "%s is a number lower than %d" % (name, num),
                             "%s is below %d" % (name, num),
                             "%s is lower than %d" % (name, num),
                             "%s is to be found below %d" % (name, num),
                             "%s must be lower than %d" % (name, num),
                             "%s shall not reach %d or higher" % (name, num),
                             "%s should be lower than %d" % (name, num),
                             "%s will be a value below %d" % (name, num),
                             "%s has to be not as much as %d" % (name, num),
                             "%s is not bigger or equal than %d" % (name, num),
                             "%s is not %d or greater" % (name, num),
                             "%s is a number less than %d" % (name, num),
                             "%s is strictly lesser than %d" % (name, num),
                             "%s will be less than %d" % (name, num),
                             "%s is a lower number than %d" % (name, num),
                             "%s can only hold a value lower than %d" % (name, num),
                             "%s is always smaller than %d" % (name, num),
                             "%s is under %d" % (name, num),
                             "%s less than %d" % (name, num),
                             "%s shall not reach as high as %d" % (name, num),
                             "%s will be below %d" % (name, num),
                             "%s will be under %d" % (name, num),
                             "%s will equal a number less than %d" % (name, num),
                             "%s will equal some number beneath %d" % (name, num),
                             "%s can not be %d or bigger" % (name, num),
                             "%s has a value equal to or less than %d" % (name, num),
                             "%s is %d, or less than %d" % (name, num, num),
                             "%s is either %d or less than %d" % (name, num, num),
                             "%s is smaller and also equal to %d" % (name, num),
                             "%s survey log datum elevation must be greater than %d" % (name, num),
                             "%s bore plugback true vertical depth should be less than %d feet" % (name, num),
                             "%s tubular assembly weight should be less than %d kg" % (name, num),
                             "%s head casing pressure should be less than %d psi" % (name, num),
                             "No %s offset of a deviated %s bore should exceed %d m" % (name, name2, num),
                             "No %s should be greater than %d m" % (name, num),
                             "%s reference elevation should be less than %d feet" % (name, num),
                             "%s casing flange elevation must be greater than  %d" % (name, num),
                             "%s total depth should be less than %d feet" % (name, num),
                             "%s measured depth should be greater than %d ft" % (name, num),
                             "%s completion top depth must be greater than  %s" % (name, num),
                             "%s reference elevation must be greater than %d" % (name, num),
                             "%s log top depth must be greater than  %d" % (name, num),
                             "%s should be less than %d feet" % (name, num),
                             "%s coverage must be less than %d" % (name, num),
                             "%s coverage must be greater than %d" % (name, num),
                             "%s must be greater than %d" % (name, num),
                             "%s Value Must Not Be Less Than %d" % (name, num),
                             ]
                for Sentence in Sentences:
                    expected_use_case = "VALUE is_comparison(%d)" % num
                    df1 = pd.DataFrame(
                        {"Sentences": [Sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = pd.concat([df, df1])
        elif usecase == "pos_neg_comparison":
            for i in range(0, 200):
                name = get_random_string(5)
                Sentences = ["%s can be negative" % name,
                             "%s is a negative number" % name,
                             "%s is negative" % name,
                             "%s is not 0 or not a positive number" % name,
                             "%s is positive or 0" % name,
                             "%s is positive or zero" % name,
                             "%s can be positive" % name,
                             "%s is a positive number" % name,
                             "%s is positive " % name,
                             "%s is negative or 0" % name,
                             ]
                for Sentence in Sentences:
                    expected_use_case = "VALUE in_comparison"
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
