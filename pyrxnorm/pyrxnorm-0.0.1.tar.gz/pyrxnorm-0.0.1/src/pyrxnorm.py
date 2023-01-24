from pydantic import BaseModel, validator
import os
import pandas as pd
from typing import Optional, Callable


class RxNorm(BaseModel):
    data_dir: str
    conso_df: Optional[pd.DataFrame]
    rel_df: Optional[pd.DataFrame]
    lookup_df: Optional[pd.DataFrame]
    normalizer: Optional[Callable]

    class Config:
        arbitrary_types_allowed = True

    @validator("data_dir")
    def valid_data(cls, v):
        # check if dir extsis
        if not os.path.exists(v):
            raise ValueError(f"'{v}' is not a valid dir.")
        # check if necessary files available
        conso_file = os.path.join(v, "RXNCONSO.RRF")
        rel_file = os.path.join(v, "RXNREL.RRF")
        if not os.path.isfile(conso_file):
            raise ValueError(f"'{conso_file}' not found.")
        if not os.path.isfile(rel_file):
            raise ValueError(f"'{rel_file}' not found.")
        return v

    def get_info(self):
        # number of CUI
        print(f'Found {len(self.conso_df["RXCUI"].unique()):,} unique RXCUIs.')
        # number of AUI
        print(f'Found {len(self.conso_df["RXAUI"].unique()):,} unique RXAUIs.')
        # number of unique terms
        print(f'Found {len(self.conso_df["TERM"].unique()):,} unique TERMs.')

        # CUIs participating in relations
        unique_values_in_relations = pd.concat(
            [self.rel_df["CUI1"], self.rel_df["CUI2"]]
        ).unique()

        print(
            f"Found {len(unique_values_in_relations):,} unique RXCUIs participating in relations."
        )

        # unique CUI relations
        print(f'Found {len(self.rel_df["REL"].unique()):,} unique CUI relations.')
        print(f'Unique CUI relations: {self.rel_df["REL"].unique()}')

    def set_lookup(self, normalizer=lambda x: x):
        self.normalizer = normalizer

        self._create_conso_df()
        self._create_rel_df()
        merged_df = self._create_merged_df(group_terms_per_concept=False)

        # normalize and sort
        merged_df["TERM1"] = merged_df["TERM1"].apply(self.normalizer)
        merged_df["TERM2"] = merged_df["TERM2"].apply(self.normalizer)
        # set multiindex for lookup
        lookup_df = merged_df.set_index(["TERM1", "TERM2"]).sort_index()
        self.lookup_df = lookup_df

    def terms_equivalent(self, term1: str, term2: str) -> bool:
        if not isinstance(self.lookup_df, pd.DataFrame):
            raise RuntimeError("First set the lookup table using 'set_lookup'.")
        term1 = self.normalizer(term1)
        term2 = self.normalizer(term2)
        try:
            return len(self.lookup_df.loc[term1, term2]) > 0
        except KeyError:
            return False
        except Exception as err:
            raise

    def lookup_term(self, term: str) -> pd.DataFrame:
        if not isinstance(self.lookup_df, pd.DataFrame):
            raise RuntimeError("First set the lookup table using 'set_lookup'.")
        term = self.normalizer(term)
        try:
            return self.lookup_df.loc[term]
        except KeyError:
            return None
        except Exception as err:
            raise

    def _create_conso_df(self):
        # read dir
        conso_dir = os.path.join(self.data_dir, "RXNCONSO.RRF")
        conso_df = pd.read_csv(conso_dir, delimiter="|", header=None)

        # print(f'Read {len(conso_df):,} lines from {conso_dir}.')

        # set columns
        col_list = list(conso_df.columns)
        col_list[0] = "RXCUI"
        col_list[7] = "RXAUI"
        col_list[14] = "TERM"
        conso_df.columns = col_list

        # filter
        conso_df = conso_df[["RXCUI", "RXAUI", "TERM"]]

        # drop NaN
        conso_df.dropna(inplace=True)
        # print(f'Read {len(conso_df):,} lines without NaN from {conso_dir}.')
        self.conso_df = conso_df

    def _create_rel_df(self):
        # read dir
        rel_dir = os.path.join(self.data_dir, "RXNREL.RRF")
        rel_df = pd.read_csv(rel_dir, delimiter="|", header=None)

        # print(f'Read {len(rel_df):,} lines from {rel_dir}.')

        # set columns
        col_list = list(rel_df.columns)
        col_list[0] = "UI1_CUI"
        col_list[1] = "UI1_AUI"
        col_list[2] = "UI1_TYPE"
        col_list[4] = "UI2_CUI"
        col_list[5] = "UI2_AUI"
        col_list[6] = "UI2_TYPE"
        col_list[7] = "REL"
        rel_df.columns = col_list

        # filter
        rel_df = rel_df[
            ["UI1_AUI", "UI1_CUI", "UI1_TYPE", "UI2_AUI", "UI2_CUI", "UI2_TYPE", "REL"]
        ]

        # assert all relations are between similar types
        if (rel_df["UI1_TYPE"] != rel_df["UI2_TYPE"]).all():
            raise RuntimeError("Expected relations to be between identical types.")

        # only keep CUI relations
        rel_df = rel_df[rel_df["UI1_TYPE"] == "CUI"]
        # print(f'Read {len(rel_df):,} CUI relations.')

        # rename again
        rel_df = rel_df[["UI1_CUI", "UI2_CUI", "REL"]]
        rel_df.columns = ["CUI1", "CUI2", "REL"]

        # drop NaN
        rel_df.dropna(inplace=True)
        # print(f'Read {len(rel_df):,} CUI relations without NaN.')

        # cast column
        rel_df = rel_df.astype(
            {
                "CUI1": "int32",
                "CUI2": "int32",
            }
        )
        self.rel_df = rel_df

    def _create_merged_df(self, group_terms_per_concept=False):
        # add reflexive relation
        unique_cuis = self.conso_df["RXCUI"].unique()
        rel_reflexive_df = pd.DataFrame(data={"CUI1": unique_cuis, "CUI2": unique_cuis})
        rel_reflexive_df["REL"] = "is_same_concept"
        rel_df_left = self.rel_df.copy()
        rel_df_left = pd.concat([rel_df_left, rel_reflexive_df])

        # filter atoms if needed
        if group_terms_per_concept:
            # only keep unique (RXCUI, TERM) combinations
            conso_df_unique = (
                self.conso_df.drop(columns=["RXAUI"])
                .groupby(["RXCUI", "TERM"])
                .first()
                .reset_index()
            )
        else:
            conso_df_unique = self.conso_df
        conso_df_unique = conso_df_unique.copy()

        # prepare for merge
        rel_df_left = rel_df_left.rename(columns={"CUI1": "RXCUI"})
        conso_df_right = conso_df_unique.rename(
            columns={"RXCUI": "RXCUI2", "RXAUI": "RXAUI2", "TERM": "TERM2"}
        )

        # merge
        merged_df = (
            conso_df_unique.reset_index()
            .merge(rel_df_left, on="RXCUI", how="outer")
            .set_index("index")
        )
        merged_df = merged_df.rename(
            columns={
                "RXCUI": "RXCUI1",
                "RXAUI": "RXAUI1",
                "TERM": "TERM1",
                "CUI2": "RXCUI2",
            }
        )
        merged_df = (
            merged_df.reset_index()
            .merge(conso_df_right, on="RXCUI2", how="outer")
            .set_index("index")
        )
        # order columns
        merged_df = merged_df.reindex(sorted(merged_df.columns), axis=1)
        return merged_df


if __name__ == "__main__":
    rxnorm = RxNorm(data_dir="/Users/kldooste/Documents/work/RxNorm_full_01032023/rrf")
    print(rxnorm)

    rxnorm.set_lookup()

    print(rxnorm.lookup_term("banana"))
    print(rxnorm.lookup_term("watermelon"))
    print(rxnorm.lookup_term("strawberry"))

    print(rxnorm.terms_equivalent("imatinib mesylate", "imatinib"))
