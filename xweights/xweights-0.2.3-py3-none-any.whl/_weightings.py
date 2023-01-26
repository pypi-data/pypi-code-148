import xarray as xr
import xesmf as xe

from ._domains import get_domain


def get_spatial_averager(ds, gdf, name=None):
    """get xesmf's spatial averager

    Parameters
    ----------
    ds: xr.Dataset or str
        Dataset or name of CORDEX_domain
    gdf:
        gp.GeoDataFrame
    name: str (optional)
        `gdf`'s column name

    Returns
    -------
    savg - xesmf.SpatialAverager
    """
    if isinstance(ds, str):
        ds = get_domain(ds)
    savg = xe.SpatialAverager(ds, gdf.geometry)
    if name is None:
        name = gdf.attrs["name"]
    savg.name = name
    savg.field_region = gdf[name]
    return savg


def spatial_averaging(ds, shp=None, savg=None):
    """xesmf's spatial averager

    Parameters
    ----------
    ds: xr.Dataset

    shp: gp.GeoDataFrame (optional)

    savg: xesmf.SpatialAverager (optional)

    Returns
    -------
    out - xr.Dataset
        Dataset containing a time series of spatial averages
        for each geometry in ``shp``

    Example
    -------
    To create a time series of spatial averages::

        import xweights as xw
        import xarray as xr

        netcdffile = ("/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/"
                     "MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/tas/"
                     "v20171121/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_"
                     "CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc")

        ds = xr.open_dataset(netcdffile)

        shp = xw.get_region('states')

        out = xw.spatial_averager(ds, shp)

    """
    if savg is None:
        savg = get_spatial_averager(ds, shp)
    elif isinstance(savg, str):
        savg = get_spatial_averager(savg, shp)

    nnz = [w.data.nnz for w in savg.weights]
    out = savg(ds)
    dims = ("geom",)
    out = out.assign_coords(
        {
            savg.name: xr.DataArray(
                savg.field_region,
                dims=dims,
            ),
            "nnz": xr.DataArray(
                nnz,
                dims=dims,
            ),
        },
    )
    return out
