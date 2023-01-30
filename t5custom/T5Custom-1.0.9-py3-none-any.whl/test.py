import config
import load_model
import main
import pandas as pd

from training_data_creation import get_random_string


def test():
    test_df = pd.read_csv(config.test_dataset)
    for ind in test_df.index:
        sentence = test_df['Testcase'][ind]
        expected = test_df['expected'][ind]
        result = main.predict(sentence)
        test_df['result'][ind] = result
    test_df.to_csv(config.test_dataset)


if __name__ == '__main__':
    # load_model.load_model()
    # test()
    usecases = ["range", "is_null", "not_null", "is_date", "is_not_date", "is_number", "is_not_number",
                "is_not_length", "is_length", "length", "is_not_comparison", "is_comparison", "comparison",
                "pos_neg_comparison"]
    df = pd.DataFrame()
    for usecase in usecases:
        for i in range(10):
            name = get_random_string(5)
            sentence = "%s can be negative" % name
            expected_use_case = "Input < 0"
            df1 = pd.DataFrame({"Sentences": [sentence], "UseCase": [expected_use_case], "classifications": [usecase]})
            df = pd.concat([df, df1])
    print(df)
