import pandas as pd
import xarray as xr

from ._io import Input
from ._regions import get_region
from ._tabulator import concat_dataframe, write_to_csv
from ._weightings import get_spatial_averager, spatial_averaging


def compute_weighted_means_ds(
    ds,
    shp=None,
    ds_name="dataset",
    time_range=None,
    column_names=[],
    averager=None,
    df_output=pd.DataFrame(),
    output=None,
    land_only=False,
    time_stat=False,
):

    """
    Compute spatial weighted mean of xr.Dataset

    Parameters
    ----------
    ds: xr.DataSet

    shp: gp.GeoDataFrame (optional)
       gp.GeoDataFrame containing the information needed
       for xesmf's spatial averaging.

    ds_name: str (optional)
        Name of the dataset will be written to the pd.DataFrame
        as an extra column.

    time_range: list (optional)
        List containing start and end date to select from ``ds``

    column_names: list (optional)
        Extra column names of the pd.DataFrame;
        the information is read from global attributes of ``ds``.

    averager: str, xesmf.SpatialAverager (optional)
        Use CORDEX domain name to calculate a xesmf.SpatialAverager object
        or use user-given one.

    df_output: pd.DataFrame (optional)
        pd.DataFrame to be concatenated with the newly created pd.DataFrame

    output: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points\n
        !!!This is NOT implemented yet!!!\n
        As workaround write land sea mask in ``ds['mask']``.
        xesmf's spatial averager automatically considers ``ds['mask']``.

    time_stat: str or list (optional)
       Do some time statistics on ``ds``\n
       !!!This is NOT implemented yet!!!

    Returns
    -------
    DataFrame : pd.DataFrame
        pandas Dataframe containing time series of spatial averages.


    Example
    -------

    To calculate time series of spatial averages for several 'Bundeländer':\n
        - select Schleswig-Holstein, Hamburg, Bremen and Lower Saxony\n
        - Merge those regions to one new region calles NortSeaCoast\n
        - Select time slice from 2007 to 2009\n
        - Set CORDEX specific result DataFrame column names\n
    ::

        import xarray as xr
        import xweights as xw

        netcdffile = ("/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/"
                     "MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/"
                     "tas/v20171121/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_"
                     "CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc")

        ds = xr.open_dataset(netcdffile)
        df = xw.compute_weighted_means_ds(ds, "states",
                                          subregions=["01_Schleswig-Holstein",
                                                      "02_Hamburg",
                                                      "03_Niedersachsen",
                                                      "04_Bremen"],
                                          merge_column=["all",
                                                       "NorthSeaCoast"],
                                          time_range=["2007-01-01","2009-12-31"],
                                          column_names=["institute_id",
                                                        "driving_model_id",
                                                        "experiment_id",
                                                        "driving_model_ensemble_member",
                                                        "model_id",
                                                        "rcm_version_id"],
                                          )
    """
    if land_only:
        """
        Not clear how to find right lsm file for each ds
        Then write lsm file to ds['mask']
        The rest is done by xesmf
        """
        NotImplementedError

    if not isinstance(ds, xr.Dataset):
        return df_output

    if time_range:
        ds = ds.sel(time=slice(time_range[0], time_range[1]))

    column_dict = {
        column: ds.attrs[column] if hasattr(ds, column) else None
        for column in column_names
    }
    try:
        out = spatial_averaging(ds, shp, savg=averager)
    except Exception:
        return df_output
    drop = [i for i in out.coords if not out[i].dims]
    out = out.drop(labels=drop)

    if time_stat:
        """
        Not sure if it is usefull to implement here or
        do it seperately after using xweights.
        """
        NotImplementedError
    df_output = concat_dataframe(
        df_output,
        out,
        column_dict=column_dict,
        name=ds_name,
    )
    if output:
        write_to_csv(df_output, output)

    return df_output


def compute_weighted_means(
    input,
    region=None,
    subregion=None,
    shp=None,
    domain_name=None,
    averager=False,
    time_range=None,
    column_names=[],
    merge_columns=False,
    column_merge=False,
    outdir=None,
    land_only=False,
    time_stat=False,
    **kwargs
):

    """
    Compute spatial weighted mean of user-given inputs.


    Parameters
    ----------
    input: str or list
        Valid input files are netCDF file(s),
        directories containing those files
        and intake-esm catalogue files

    region: str (optional)
        Name of the shapefile or pre-defined region
        containing the information needed
        for xesmf's spatial averaging.

    subregion: str or list (optional)
        Name of the subregion(s) to be selected from ``region``

    shp: gp.GeoDataFrame (optional)
        gp.GeoDataFrame containing the information
        needed for xesmf's spatial averaging

    domain_name: str (optional)
        Name of the CORDEX_domain.
        This is only needed if ``ds`` does not have
        longitude and latitude vertices.
    averager: bool or xesmf.SpatialAverager object (optional)
        If True: Calculate one xesmf.SpatialAverager to use for all ds'.
        If False or None: Calculate a xesmf.SpatialAverager
        individually for each ds.
        Else use user-given xesmf.SpatialAverager

    time_range: list (optional)
        List containing start and end date to be select

    column_names: list (optional)
        Extra column names of the pd.DataFrame;
        the information is read from global attributes

    merge_columns: str or list (optional)
        Name of the column to be merged together.
        Set ['all', 'newname'] to merge all geometries
        and set new column name to 'newname'.

    column_merge: str (optional)
        Column name to differentiate shapefile while merging.

    outdir: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points\n
        !!!This is NOT implemented yet!!!\n
        As workaround write land sea mask in ``ds['mask']``.
        xesmf's spatial averager automatically considers ``ds['mask']``.

    time_stat: str or list (optional)
       Do some time statistics on ``ds``\n
       !!!This is NOT implemented yet!!!

    Returns
    -------
    DataFrame : pd.DataFrame
        pandas Dataframe containing time series of spatial averages.

    Example
    -------

    To calculate time series of spatial averages for several 'Bundeländer':\n
        - select Schleswig-Holstein, Hamburg, Bremen and Lower Saxony\n
        - Merge those regions to one new region calles NortSeaCoast\n
        - Select time slice from 2007 to 2009\n
        - Set CORDEX specific result DataFrame column names\n
    ::

        import xweights as xw

        netcdffile = ("/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/"
                     "MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/tas/"
                     "v20171121/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_"
                     "CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc"

        df = xw.compute_weighted_means_ds(netcdffile, 'states',
                                          subregions=['01_Schleswig-Holstein,
                                                      '02_Hamburg',
                                                      '03_Niedersachsen',
                                                      '04_Bremen'],
                                          merge_column=['all',
                                                       'NorthSeaCoast'],
                                          time_range=['2007-01-01','2009-12-31'],
                                          column_names=['institute_id',
                                                        'driving_model_id',
                                                        'experiment_id',
                                                        'driving_model_ensemlbe_member',
                                                        'model_id',
                                                        'rcm_version_id'],
                                          )


    """

    def _calc_time_statistics(ds, statistics):
        return ds

    if shp is None:
        shp = get_region(
            region, name=subregion, merge=merge_columns, column=column_merge
        )

    if averager is True:
        averager = get_spatial_averager(domain_name, shp.geometry)
    elif averager is False:
        averager = domain_name

    dataset_dict = Input(input, **kwargs).dataset_dict

    df_output = pd.DataFrame()

    for name, ds in dataset_dict.items():

        df_output = compute_weighted_means_ds(
            ds,
            shp,
            ds_name=name,
            time_range=time_range,
            column_names=column_names,
            averager=averager,
            df_output=df_output,
            land_only=land_only,
            time_stat=time_stat,
        )

    if outdir:
        write_to_csv(df_output, outdir)

    return df_output
