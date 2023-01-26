from io import BytesIO
import json
import pandas as pd
import numpy as np
from hestia_earth.utils.api import download_hestia
from hestia_earth.schema import TermTermType

from hestia_earth.distribution.log import logger
from . import df_to_csv_buffer, get_stats_from_df
from ..cycle import YIELD_COLUMN, FERTILISER_COLUMNS
from ..likelihood import generate_likl_file
from .storage import file_exists, load_from_storage, write_to_storage

FOLDER = 'posterior_files'
TERM_TYPE_TO_COLUMN = {
    TermTermType.CROP.value: YIELD_COLUMN,
    TermTermType.INORGANICFERTILISER.value: FERTILISER_COLUMNS,
    TermTermType.ORGANICFERTILISER.value: FERTILISER_COLUMNS
}


def posterior_by_country(df_prior: pd.DataFrame, data, country_id: str, term_id: str, n_sample=1000):
    mu_country, sigma_country = get_stats_from_df(df_prior, country_id, term_id)

    logger.info(f'Prior mu ={mu_country}, std = {sigma_country}; Obs mean ={data.mean()}, std ={data.std()}')

    try:
        import pymc as pm
    except ImportError:
        raise ImportError("Run `pip install pymc==4` to use this functionality")

    if sigma_country > 0:
        with pm.Model():
            pm.Normal('mu', mu=mu_country, sigma=sigma_country)
            pm.HalfNormal('sd', sigma=sigma_country)

            sample = pm.sample(n_sample*2, tune=n_sample, cores=4)
            sample.extend(pm.sample_posterior_predictive(sample))
            # mu, sd = pm.summary(sample)['mean']
            return sample


def _find_matching_column(term_id: str):
    term = download_hestia(term_id)
    col_name = TERM_TYPE_TO_COLUMN[term.get('termType')]
    if col_name == YIELD_COLUMN:
        return YIELD_COLUMN
    elif col_name == FERTILISER_COLUMNS:
        unit = term.get('units')
        match = [f.find(unit) > 0 for f in FERTILISER_COLUMNS]
        return FERTILISER_COLUMNS[np.where(match)[0][0]]


def _read_post(filename: str):
    data = json.loads(load_from_storage(filename))
    return data.get('posterior', {}).get('mu', []), data.get('posterior', {}).get('sd', [])


def _write_post(country_id: str, term_id: str, filepath: str, df_prior: pd.DataFrame, generate_prior):
    data = {
        'posterior': {'mu': [], 'sd': []}
    }
    df_likl = generate_likl_file(country_id, term_id)

    if len(df_likl) > 0:
        # make sure we don't load prior file muliple times when generating all posteriors
        _df_prior = generate_prior() if df_prior is None else df_prior
        likl_data = df_likl[_find_matching_column(term_id)]
        posterior_data = posterior_by_country(_df_prior, likl_data, country_id, term_id)
        if posterior_data is not None:
            data['posterior']['mu'] = posterior_data['posterior']['mu'].to_dict()['data']
            data['posterior']['sd'] = posterior_data['posterior']['sd'].to_dict()['data']

    # skip writing when the file exists and the data will not be updated
    should_write_to_storage = not file_exists(filepath) or len(df_likl) > 0
    write_to_storage(filepath, json.dumps(data).encode('utf-8')) if should_write_to_storage else None
    return data.get('posterior', {}).get('mu', []), data.get('posterior', {}).get('sd', [])


def post_filename(country_id: str, term_id: str): return f'posterior_{country_id}_{term_id}.json'


def get_esemble_means(mu_ensemble: list, sd_ensemble: list):
    """
    Return posterior means for an ensembles of mu and an ensembles of sigma (sd).

    Parameters
    ----------
    mu_ensemble: list
        List of list of float storing the posterior mu ensembles.
    sd_ensemble: list
        List of list of float storing the posterior sd ensembles.

    Returns
    -------
    tuple(mu, sd)
        The mean of posterior mu and the mean of posterior sigma (sd)
    """
    return (np.array(mu_ensemble).mean(), np.array(sd_ensemble).mean()) if all([
        len(mu_ensemble) > 0,
        len(sd_ensemble) > 0
    ]) else None


def get_index_range(values: list, index: list): return values or list(range(len(index)))


def get_post_ensemble_data(
    country_id: str, term_id: str,
    overwrite=False, df_prior: pd.DataFrame = None, generate_prior=None
):
    filepath = f"{FOLDER}/{post_filename(country_id, term_id)}"
    read_existing = file_exists(filepath) and not overwrite
    return _read_post(filepath) if read_existing else _write_post(country_id, term_id, filepath,
                                                                  df_prior, generate_prior)


def update_all_post_data(df_prior: pd.DataFrame, filename: str, rows: list = None, cols: list = None, overwrite=True):
    rows = get_index_range(rows, df_prior.index)
    term_ids = df_prior.index[rows]
    cols = get_index_range(cols, df_prior.columns)
    country_ids = df_prior.columns[cols]
    df = pd.DataFrame(index=term_ids, columns=country_ids)

    for country_id in country_ids:
        for term_id in term_ids:
            if not pd.isnull(df_prior.loc[term_id, country_id]):
                mu_ensemble, sd_ensemble = get_post_ensemble_data(country_id, term_id,
                                                                  overwrite=overwrite, df_prior=df_prior)
                df.loc[term_id, country_id] = get_esemble_means(mu_ensemble, sd_ensemble)

    df.index.rename('term.id', inplace=True)
    write_to_storage(f"{FOLDER}/{filename}", df_to_csv_buffer(df))
    return df.dropna(axis=1, how='all').dropna(axis=0, how='all')


def get_post_data(country_id: str, term_id: str, filename: str):
    data = load_from_storage(f"{FOLDER}/{filename}")
    df = pd.read_csv(BytesIO(data), index_col=0)
    return get_stats_from_df(df, country_id, term_id)
