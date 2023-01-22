import pandas as pd
import argparse
from os.path import exists
import numpy as np
from pandas.api.types import is_string_dtype, is_numeric_dtype
from tabulate import tabulate


def checkFileFormat(df):
    """
    Function to check if first column is string and all others are numeric
    and number of columns is greater than equal to 3
    df: pandas dataframe of input file
    """
    if (
        is_string_dtype(df.iloc[:, 0])
        and all(is_numeric_dtype(df.iloc[:, i]) for i in range(1, len(df.columns)))
        and len(df.columns) >= 3
    ):
        return True
    else:
        raise (
            argparse.ArgumentTypeError(
                """
                Incorrect format of input file!
                First Column should contain Criteria (string/object dtype)
                All others columns should be numeric
                """
            )
        )


def checkWeightsImpacts(weights, impacts, total_columns):
    """
    Function to check if weights and impacts are correct and impacts are either + or -
    weights: string of weights separated by comma or list of weights
    impacts: string of impacts separated by comma (either + or -) or list of impacts
    total_columns: total number of columns in input file
    """
    if weights is not None:
        if type(weights) is str:
            weights = np.array(weights.split(",")).astype(np.float32)
        else:
            weights = np.array(weights).astype(np.float32)
        if len(weights) != total_columns - 1:
            raise (argparse.ArgumentTypeError("Incorrect number of weights"))
    else:
        weights = np.full(shape=total_columns - 1, fill_value=1, dtype=np.float32)

    if impacts is not None:
        if type(impacts) is str:
            impacts = np.array(impacts.split(","))
        else:
            impacts = np.array(impacts)
        if len(impacts) != total_columns - 1:
            raise (argparse.ArgumentTypeError("Incorrect number of impacts"))
        if not np.all(np.isin(impacts, ["+", "-"])):
            raise (argparse.ArgumentTypeError("Impacts should be either + or -"))
    else:
        impacts = np.full(shape=total_columns - 1, fill_value="+")

    return weights, impacts


# Function to calculate topsis score
def score(data, weights, impacts):
    """
    Function to calculate topsis score
    data: numpy array of input data without first column (criteria)
    weights: numpy array of weights
    impacts: numpy array of impacts either + or -
    """

    # Normalize numeric columns using topis formula
    data = data / np.sqrt(np.sum(data**2, axis=0))

    # Multiply normalized columns with weights
    data *= weights

    # Get max and min values from columns
    vmax = data.max(axis=0)
    vmin = data.min(axis=0)

    # Using impacts swap vmax and vim values if impact is negative else keep it as it is
    for i in range(len(impacts)):
        if impacts[i] == "-":
            vmax[i], vmin[i] = vmin[i], vmax[i]

    # Calculating topsis score
    sp = np.linalg.norm(data - vmax, axis=1)
    sn = np.linalg.norm(data - vmin, axis=1)

    # Return topsis score
    return sn / (sp + sn)

# Function to write output file
def writeOutputFile(output_path, df, overwrite=False):
    """
    Function to write output file
    output_path: path of output file in csv or xlsx format
    df: pandas dataframe of input file
    topsis_score: numpy array of topsis score
    """

    # Check if output file exists
    if exists(output_path):
        if overwrite:
            print("Output file already exists. Overwriting it at " + output_path)
        else:
            raise (FileExistsError("Output file already exists"))
    # Write output file
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    elif output_path.endswith(".xlsx"):
        df.to_excel(output_path, index=False)
    else:
        raise (argparse.ArgumentTypeError("Output file format not supported"))


def readInputFile(input_path):
    """
    Function to read input file and check if it is in correct format
    input_path: path of input file in csv or xlsx format
    """

    # Check if input file exists
    if exists(input_path):
        # Read input file
        if input_path.endswith(".csv"):
            df = pd.read_csv(input_path)
        elif input_path.endswith(".xlsx"):
            df = pd.read_excel(input_path)
        else:
            raise (argparse.ArgumentTypeError("Input file format not supported"))

        # Check if input file is in correct format
        if checkFileFormat(df):
            return df
        else:
            raise (argparse.ArgumentTypeError("Incorrect format of input file"))
    else:
        raise (FileNotFoundError("Input file does not exist"))


def calculate(input_path, output_path, weights = None, impacts = None, verbose=False, overwrite=False):
    """
    input_path: path of input file in csv or xlsx format
    output_path: path of output file in csv or xlsx format
    weights: string of weights separated by comma (optional) or list of weights
    impacts: string of impacts separated by comma (either + or -) (optional) or list of impacts
    verbose: boolean value to print weights, impacts, topsis score and rank (optional)
    returns: pandas dataframe of input file with topsis score and rank
    """

    df = readInputFile(input_path)
    weights, impacts = checkWeightsImpacts(weights, impacts, len(df.columns))

    topsis_score = score(df.iloc[:, 1:].values, weights, impacts)
    df["Topsis Score"] = np.round(topsis_score, 4)

    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    if verbose:
        # Print weights and impacts
        print("\nWeights: ", weights)
        print("Impacts: ", impacts)

        print("\nTop 5 attributes with highest topsis score:")

        # Print sorted data's 1st column, topsis score and rank using tabulate
        print(
            tabulate(
                df.sort_values(by="Topsis Score", ascending=False).head(),
                headers="keys",
                tablefmt="psql",
                showindex=False,
            )
        )

    writeOutputFile(output_path, df, overwrite=overwrite)
    return df


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Topsis Score Calculator",
        epilog="Example: python topsis.py -i input.csv -o output.csv -w 0.2,0.3,0.5 -p +,+,- -f",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Input file path in csv or xlsx format",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.csv",
        help="Output file path in csv or xlsx format",
    )
    parser.add_argument(
        "-w",
        "--weights",
        type=str,
        help="Weights separated by comma",
    )
    parser.add_argument(
        "-p",
        "--impacts",
        type=str,
        help="Impacts separated by comma (either + or -)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists",
    )
    
    args = vars(parser.parse_args())
    calculate(
        args["input"], args["output"], args["weights"], args["impacts"], verbose=True, overwrite=args["force"]
    )
