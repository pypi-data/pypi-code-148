"""@Author: Rayane AMROUCHE

Column transformation methods for the Utils class for the DataManager.
"""

from typing import Any, List, Optional

import pandas as pd  # type: ignore

from dsmanager.datamanager.datastorage import DataStorage


class ColumnUtils:
    """ColumnUtils class brings utils tools for the data manager."""

    def __init__(self) -> None:
        self.categories = DataStorage()

    def create_category(
        self,
        name: str,
        categories: List[Any],
        ordered: bool = False,
    ) -> pd.CategoricalDtype:
        """Create a category type and save it in a DataStorage.

        Args:
            name (str): Name of the category type to create.
            categories (List[Any]): Unique list of values of the category.
            ordered (bool): True if this category is ordered.

        Returns:
            pd.CategoricalDtype: Category type created.
        """
        category = pd.CategoricalDtype(
            categories,
            ordered,
        )
        self.categories[name] = category
        return category

    def as_category(
        self, __df: pd.DataFrame, column: str, category_name: str = "", **kwargs: Any
    ) -> pd.DataFrame:
        """Transform a DataFrame column's type to a pd.Categorical.

        Args:
            __df (pd.DataFrame): DataFrame with a column that needs to be transformed.
            column (str): Column which type is to be changed to a pd.Categorical.
            category_name (str, optional): Name of the category to create. Defaults to
                "".

        Returns:
            pd.DataFrame: Returns DataFrame to keep chaining.
        """
        if category_name == "":
            category_name = column
        if category_name in self.categories:
            category = self.categories[category_name]
        else:
            if "categories" not in kwargs:
                kwargs["categories"] = __df[column].dropna().unique()

            category = self.create_category(category_name, **kwargs)
        return __df.astype({column: category})

    def bin_column(self, __df: pd.DataFrame, column: str, k: int = 20) -> pd.DataFrame:
        """Apply k binning on a given column of a given dataframe.

        Args:
            __df (pd.DataFrame): Dataframe from which a column will be transformed.
            column (str): Column on which apply binning.
            k (int, optional): Number of bins to create for the given column. Defaults
                to 20.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if __df[column].nunique() < k:
            return __df.assign(**{f"{column}_bin": lambda df__: df__[column]})
        return __df.assign(
            **pd.cut(__df[column], bins=k)
            .astype(str)
            .str.strip("(]")
            .str.split(", ")
            .to_frame()
            .pipe(
                lambda df__: df__.assign(
                    **pd.DataFrame(
                        df__[column].to_list(),
                        columns=[f"{column}_lb", f"{column}_hb"],
                        index=df__.index,
                    )
                )
            )
            .assign(
                **{
                    f"{column}_bin": lambda df__: df__[[f"{column}_lb", f"{column}_hb"]]
                    .astype(float)
                    .mean(axis=1)
                }
            )
            .pipe(self.as_category, f"{column}_bin", ordered=True)
            .drop(columns=[column])
        )

    @staticmethod
    def onehot_encode(__df: pd.DataFrame, column: str, **kwargs: Any) -> pd.DataFrame:
        """Encode a column using the onehot method.

        Args:
            __df (pd.DataFrame): DataFrame which column are to be onehot encoded.
            column (str): Column to onehot encode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return __df.assign(**pd.get_dummies(__df[column], prefix=column, **kwargs))

    @staticmethod
    def onehot_decode(__df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Decode a list of columns using the onehot method.

        Args:
            __df (pd.DataFrame): DataFrame which columns are the result of a onehot
            encoding.
            columns (str): Column to onehot decode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return __df.assign(**pd.from_dummies(__df[columns]))

    @staticmethod
    def column_spliter(
        __df: pd.DataFrame, column: str, columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Split a column which contain a dict or a list.

        Args:
            __df (pd.DataFrame): Dataframe from which a column will be splited.
            column (str): Column to split.
            columns (List[str]): Name of the columns after split.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if columns is None:
            return __df.assign(
                **pd.DataFrame(__df[column].to_list()).add_prefix(column)
            )
        return __df.assign(
            **pd.DataFrame(__df[column].to_list(), columns=columns).add_prefix(column)
        )

    @staticmethod
    def transform(
        __df: pd.DataFrame,
        by: str,  # pylint: disable=invalid-name
        aggregator: Any,
        columns: Any,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """Transform a list of column with a given function by grouping around an
            other column.

        Args:
            __df (pd.DataFrame): pandas Dataframe from which a list of column will be
                transformed.
            by (str): Used to determine the groups for the groupby.
            aggregator (Any): Function to use for transforming the data.
            columns (Any): List of columns on which the transformation will be applied.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        aggregator_name = (
            aggregator if isinstance(aggregator, str) else aggregator.__name__
        )
        columns = list(__df.columns) if columns is None else columns
        func_list = [
            (
                lambda df__, col: df__.assign(
                    **{
                        f"{col}_{aggregator_name}": df__[[col, by]]
                        .groupby(col)
                        .transform(aggregator, *args, **kwargs)[by]
                    }
                ),
                {
                    "col": col,
                },
            )
            for col in columns
        ]
        return __df.pipe_steps(func_list)
