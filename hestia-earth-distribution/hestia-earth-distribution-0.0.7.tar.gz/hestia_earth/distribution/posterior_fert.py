import pandas as pd

from .utils.fao import get_fert_group_id
from .utils.posterior import update_all_post_data, get_post_data, get_post_ensemble_data
from .prior_fert import generate_prior_fert_file

POSTERIOR_FERT_FILENAME = 'posterior_fert_use.csv'


def get_post_ensemble(country_id: str, input_id: str, overwrite=False, df_prior: pd.DataFrame = None):
    """
    Return posterior data for a given country and a given product.
    If posterior file exisits, data will be read in; otherwise, generate posterior data and store
    into a pickle or json file.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    input_id: str
        Fertiliser term `@id` from Hestia glossary, e.g. 'ammoniumNitrateKgN', or
        'inorganicNitrogenFertiliserUnspecifiedKgN'.
    overwrite: bool
        Whether to overwrite existing posterior file or not. Defaults to `False`.
    df_prior: pd.DataFrame
        Optional - if prior file is already loaded, pass it here.

    Returns
    -------
    tuple(mu, sd)
        List of float storing the posterior mu and sd ensembles.
    """
    fert_id = get_fert_group_id(input_id)
    return get_post_ensemble_data(country_id, fert_id,
                                  overwrite=overwrite, df_prior=df_prior, generate_prior=generate_prior_fert_file)


def update_all_post(rows: list = None, cols: list = None, overwrite=True):
    """
    Update crop posterior data for all countries and all products.
    It creates or re-write json files to store posterior data for each country and each product.
    It also writes all distribution stats (mu, sigma) into one csv file.

    Parameters
    ----------
    rows: list of int
        Rows (products) to be updated. Default None to include all products.
    cols: list of int
        Columns (countries) to be updated. Default None to include all countries.
    overwrite: bool
        Whether to overwrite the posterior json files. Defaults to `True`.

    Returns
    -------
    DataFrame
        A DataFrame storing all posterior data.
    """
    df_prior = generate_prior_fert_file()
    return update_all_post_data(df_prior, POSTERIOR_FERT_FILENAME, rows, cols, overwrite)


def get_post(country_id: str, input_id: str):
    """
    Return posterior data for a given country and a given product.
    Data is read from the file containing all posterior data.
    Cannot use this function to generate new post files.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    input_id: str
        Fertiliser term `@id` from Hestia glossary, e.g. 'ammoniumNitrateKgN'.

    Returns
    -------
    tuple(mu, sd)
        Mean values of mu and sd.
    """
    fert_id = get_fert_group_id(input_id)
    return get_post_data(country_id, fert_id, POSTERIOR_FERT_FILENAME)
