"""
Python script to automatically download and crop climate data layers from SILO.

Functionalities:
- download SILO data for custom time period and layer(s) as defined in dictionary
- clip data to custom bounding box
- save data as multi-band geotiff or netCDF

The SILO climate layers are described as dictionary in the module function get_silodict()
and the SILO licensing and attribution are availabe with the module function getdict_license()

More details on the SILO climate variables can be found here:
https://www.longpaddock.qld.gov.au/silo/about/climate-variables/
and more details about the gridded data structure here:
https://www.longpaddock.qld.gov.au/silo/gridded-data/
and a data index:
https://s3-ap-southeast-2.amazonaws.com/silo-open-data/Official/annual/index.html

This package is part of the Data Harvester project developed for the Agricultural Research Federation (AgReFed).

Copyright 2022 Sydney Informatics Hub (SIH), The University of Sydney

This open-source software is released under the LGPL-3.0 License.

Author: Sebastian Haan
"""

import os
import shutil
import datetime
import requests
import numpy as np

# from urllib import request
from netCDF4 import Dataset
import rasterio
import rioxarray as rio
import xarray

from geodata_harvester import utils
from geodata_harvester.utils import spin

# from datacube.utils.cog import write_cog


def download_file(url, layername, year, outpath="."):
    """
    download file from url

    INPUT:
    url : str
    outpath : str

    OUTPUT:
    file : str
    """
    local_filename = os.path.join(outpath, url.split("/")[-1])
    if os.path.exists(local_filename):
        utils.msg_warn(f"{layername} for {year} already exists, skipping download")
        return local_filename
    with spin(f"Downloading {layername} for {year}") as s:
        with requests.get(url, stream=True) as r:
            with open(local_filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        s(1)

    # with request.urlopen(url) as response:
    #     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    #         shutil.copyfileobj(response, tmp_file)
    # return tmp_file.name
    return local_filename


def get_silodict():
    """
    Get dictionary of available layers and meta data

    OUTPUT:
    layerdict : dict
        dictionary of meta data and available layer names
    """

    silodict = {}
    silodict["title"] = "SILO climate database"
    silodict[
        "description"
    ] = "SILO is containing continuous daily climate data for Australia from 1889 to present."
    silodict["crs"] = "EPSG:4326"
    silodict["bbox"] = [112.00, -44.00, 154.00, -10.00]
    silodict["resolution_arcsec"] = 180
    silodict["updates"] = "daily"
    silodict["layernames"] = {
        "daily_rain": "Daily rainfall, mm",
        "monthly_rain": "Monthly rainfall, mm",
        "max_temp": "Maximum temperature, degrees Celsius",
        "min_temp": "Minimum temperature, degrees Celsius",
        "vp": "Vapour pressure, hPa",
        "vp_deficit": "Vapour pressure deficit, hPa",
        "evap_pan": "Class A pan evaporation, mm",
        "evap_syn": "Synthetic estimate, mm",
        "evap_comb": "Combination: synthetic estimate pre-1970, class A pan 1970 onwards, mm",
        "evap_morton_lake": "Morton's shallow lake evaporation, mm",
        "radiation": "Solar radiation: Solar exposure, consisting of both direct and diffuse components, MJ/m2",
        "rh_tmax": "Relative humidity:	Relative humidity at the time of maximum temperature, %",
        "rh_tmin": "Relative humidity at the time of minimum temperature, %",
        "et_short_crop": "Evapotranspiration FAO564 short crop, mm",
        "et_tall_crop": "ASCE5 tall crop6, mm",
        "et_morton_actual": "Morton's areal actual evapotranspiration, mm",
        "et_morton_potential": "Morton's point potential evapotranspiration, mm",
        "et_morton_wet": "Morton's wet-environment areal potential evapotranspiration over land, mm",
        "mslp": "Mean sea level pressure Mean sea level pressure, hPa",
    }
    return silodict


def getdict_license():
    """
    Retrieves the SILO license and attribution information as dict
    """
    dict = {
        "name": "SILO Climate Data",
        "source_url": "https://www.longpaddock.qld.gov.au/silo/",
        "license": "CC BY 4.0",
        "license_title": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "copyright": "© State of Queensland (Queensland Department of Environment and Science) 2020.",
        "attribution": "State of Queensland (Queensland Department of Environment and Science) 2020.",
    }
    return dict


def xarray2tif(ds, outfname, layername):
    """
    Convert rio xarray dataset to multi-band geotiff with each time as separate band.

    TBD: optional: save separate tif each time slice

    INPUT:
    ds : xarray dataset
    outfname : str
        path+name of output file (".tif")

    OUTPUT:
    tif : str, name of multi-band geotiff
    """

    # create empty array
    dsnew = xarray.Dataset()

    for i in range(len(ds.time)):

        # We will use the date of the image to name the GeoTIFF
        date = ds.isel(time=i).time.dt.strftime("%Y-%m-%d").data
        # print(f'Writing {date}')

        da = ds.isel(time=i)
        dsnew[str(date)] = xarray.DataArray(
            da.variables[layername][:],
            dims=["lat", "lon"],
            coords={"lat": da.variables["lat"], "lon": da.variables["lon"]},
        )

        # Write GeoTIFF with datacube libary for cloud optimized GeoTIFFs (COG)
        # write_cog(geo_im=singletimestamp_da,
        #         fname=os.path.join(outpath,f'{outfname_base}_{date}.tif',
        #         overwrite=True)
    # Set crs
    dsnew.rio.write_crs(4326, inplace=True)

    # Write GeoTIFF to disk
    dsnew.rio.to_raster(outfname)


def get_SILO_layers(
    layernames,
    date_start,
    date_end,
    outpath,
    bbox=None,
    format_out="tif",
    delete_tempfiles=False,
    verbose=False,
    ):
    """
    Get raster data from SILO for certain climate variable and save data as geotif.
    If multiple times are requested, then each time will be saved in on band of multi-band geotif.
    All layers are available with daily resolution (except 'monthly_rain')

    This function includes validation of years and automatically download of data from SILO in temporary folder.

    Input:
        layernames : list climate variable names (see below)
        date_start : str, start date of time series in format 'YYYY-MM-DD'
        date_end : str, end date of time series in format 'YYYY-MM-DD'
        outpath : str, path to save output data
        bbox : list of bounding box coordinates (optional)
        format_out : str, format of output data: either 'NetCDF' (nc) or 'GeoTIFF' (tif)
        delete_tempfiles : bool, delete temporary files after processing

    Returns:
        fnames_out : list of output filenames

    layer names:
        - 'daily_rain' (Daily rainfall, mm)
        - 'monthly_rain' (Monthly rainfall, mm)
        - 'max_temp' (Maximum temperature, deg C)
        - 'min_temp'  (Minimum temperature. deg C)
        - 'vp' (Vapour pressure, hPa)
        - 'vp_deficit' (Vapour pressure deficit, hPa)
        - 'evap_pan' (Class A pan evaporation, mm)
        - 'evap_syn' (Synthetic estimate, mm)
        - 'evap_comb' (Combination: synthetic estimate pre-1970, class A pan 1970 onwards, mm)
        - 'evap_morton_lake' (Morton's shallow lake evaporation, mm)
        - 'radiation'	(Solar radiation: Solar exposure, consisting of both direct and diffuse components, MJ/m2)
        - 'rh_tmax'	(Relative humidity:	Relative humidity at the time of maximum temperature, %)
        - 'rh_tmin'	(Relative humidity at the time of minimum temperature, %)
        - 'et_short_crop' (Evapotranspiration FAO564 short crop, mm)
        - 'et_tall_crop' (ASCE5 tall crop6, mm)
        - 'et_morton_actual' (Morton's areal actual evapotranspiration, mm)
        - 'et_morton_potential'	(Morton's point potential evapotranspiration, mm)
        - 'et_morton_wet' (Morton's wet-environment areal potential evapotranspiration over land, mm)
        - 'mslp' (Mean sea level pressure Mean sea level pressure, hPa)

    For more details see:
    SILO data structure doc for gridded data:
    https://www.longpaddock.qld.gov.au/silo/gridded-data/

    Notes: Here we use the SILO annual raster API to download the data and then trim to date range. 
    For data ranges much smaller than a year, one could also use the SILO daily raster API and combine dates.
    """

    # define outpath for temporary files
    outpath_temp = os.path.join(outpath, 'temp_silo')
    os.makedirs(outpath, exist_ok=True)
    date_start = str(date_start)
    date_end = str(date_end)
    years = np.arange(int(date_start[:4]), int(date_end[:4]) + 1).tolist()
    fnames_out_silo = []
    
    for layername in layernames:

        # run the download
        fnames_out = get_SILO_raster(
            layername, 
            years, 
            outpath_temp, 
            bbox = bbox, 
            format_out = 'nc', 
            delete_temp = False)

        # process the data into a single file and trim to date range
        if (format_out == 'tif') | (format_out == 'GeoTIFF'):
            outfname = os.path.join(outpath, "silo_" + layername + "_" + date_start + "-" + date_end + ".tif")
        elif (format_out == 'NetCDF') | (format_out == 'nc'):
            outfname = os.path.join(outpath, "silo_" + layername + "_" + date_start + "-" + date_end + ".nc")
        else:
            raise ValueError("format_out must be either 'tif' or 'nc'")

        # Combine all years into one file and trim to date range
        process_raster_daterange(fnames_out, date_start, date_end, outfname, layername)

        # Delete temporary cropped files (not the downloaded file)
        for fname in fnames_out:
            os.remove(fname)
    
        #Save the layer name
        # Check if outfname is list or string
        if isinstance(outfname, list):
            fnames_out_silo += outfname
        else:
            fnames_out_silo.append(outfname)

    return fnames_out_silo
    


def process_raster_daterange(infnames, date_start, date_end, outfname, layername):
    """ Combines all the raster data into one xarray dataset, trimming to the date range, 
    and saves it as a multiband tif file.

    Input:
        infnames : list of input filenames
        date_start : str, start date of time series in format 'YYYY-MM-DD'
        date_end : str, end date of time series in format 'YYYY-MM-DD'
        outfname : str, path+name of output file
    """
    # Read all the raster data into one xarray dataset
    try:
        # Requires dask installed
        ds = xarray.open_mfdataset(infnames, combine="by_coords")
    except:
        # If dask is not installed, merge it this way (not as memory efficient)
        ds = xarray.merge([xarray.open_dataset(f) for f in infnames])
    # Clip to date range
    ds = ds.sel(time=slice(date_start, date_end))
    # Save file
    # if file extension is tif, save as 
    if outfname.endswith('.tif'):
        xarray2tif(ds, outfname, layername)
    if outfname.endswith('.nc'):
        ds.to_netcdf(outfname)
    # Close file
    ds.close()



def process_raster_daterange(infnames, date_start, date_end, outfname, layername):
    """ Combines all the raster data into one xarray dataset, trimming to the date range, 
    and saves it as a multiband tif file.

    Input:
        infnames : list of input filenames
        date_start : str, start date of time series in format 'YYYY-MM-DD'
        date_end : str, end date of time series in format 'YYYY-MM-DD'
        outfname : str, path+name of output file
    """
    # Read all the raster data into one xarray dataset
    try:
        # Requires dask installed
        ds = xarray.open_mfdataset(infnames, combine="by_coords")
    except:
        # If dask is not installed, merge it this way (not as memory efficient)
        ds = xarray.merge([xarray.open_dataset(f) for f in infnames])
    # Clip to date range
    ds = ds.sel(time=slice(date_start, date_end))
    # Save file
    # if file extension is tif, save as 
    if outfname.endswith('.tif'):
        xarray2tif(ds, outfname, layername)
    if outfname.endswith('.nc'):
        ds.to_netcdf(outfname)
    # Close file
    ds.close()



def get_SILO_raster(
    layername,
    years,
    outpath,
    bbox=None,
    format_out="nc",
    delete_temp=False,
    verbose=False,
    ):
    """
    Get raster data from SILO for certain climate variable and save data as geotif.
    If multiple times are requested, then each time will be saved in on band of multi-band geotif.
    All layers are available with daily resolution (except 'monthly_rain')

    This function includes validation of years and automatically download of data from SILO in temporary folder.

    Input:
        layername : str, climate variable name (see below)
        years : list of years
        outpath : str, path to save output data
        bbox : list of bounding box coordinates (optional)
        format_out : str, format of output data: either 'nc' (netCDF) or 'tif' (geotiff)
        delete_temp : bool, delete temporary folder after download

    Returns:
        fnames_out : list of output filenames



    layer names:
        - 'daily_rain' (Daily rainfall, mm)
        - 'monthly_rain' (Monthly rainfall, mm)
        - 'max_temp' (Maximum temperature, deg C)
        - 'min_temp'  (Minimum temperature. deg C)
        - 'vp' (Vapour pressure, hPa)
        - 'vp_deficit' (Vapour pressure deficit, hPa)
        - 'evap_pan' (Class A pan evaporation, mm)
        - 'evap_syn' (Synthetic estimate, mm)
        - 'evap_comb' (Combination: synthetic estimate pre-1970, class A pan 1970 onwards, mm)
        - 'evap_morton_lake' (Morton's shallow lake evaporation, mm)
        - 'radiation'	(Solar radiation: Solar exposure, consisting of both direct and diffuse components, MJ/m2)
        - 'rh_tmax'	(Relative humidity:	Relative humidity at the time of maximum temperature, %)
        - 'rh_tmin'	(Relative humidity at the time of minimum temperature, %)
        - 'et_short_crop' (Evapotranspiration FAO564 short crop, mm)
        - 'et_tall_crop' (ASCE5 tall crop6, mm)
        - 'et_morton_actual' (Morton's areal actual evapotranspiration, mm)
        - 'et_morton_potential'	(Morton's point potential evapotranspiration, mm)
        - 'et_morton_wet' (Morton's wet-environment areal potential evapotranspiration over land, mm)
        - 'mslp' (Mean sea level pressure Mean sea level pressure, hPa)

    For more details see:
    SILO data structure doc for gridded data:
    https://www.longpaddock.qld.gov.au/silo/gridded-data/

    SILO url structure:
    url = "https://s3-ap-southeast-2.amazonaws.com/silo-open-data/Official/annual/<variable>/<year>.<variable>.nc
    e.g. url = "https://s3-ap-southeast-2.amazonaws.com/silo-open-data/Official/annual/monthly_rain/2005.monthly_rain.nc"
    """

    # Check if layername is valid
    silodict = get_silodict()
    layerdict = silodict["layernames"]
    if layername not in layerdict:
        raise ValueError(f"Layer name {layername} not valid. Choose from: {str(layerdict.keys())}")

    # Create output folder
    os.makedirs(outpath, exist_ok=True)

    # Check if years are valid
    if not (isinstance(years, tuple) | isinstance(years, list)):
        # If not a list, make it a list
        years = [years]
    # Get current year from datetime
    current_year = int(datetime.datetime.now().year)

    # Check if format is valid
    if format_out not in ["nc", "tif", "NetCDF", "GeoTIFF"]:
        raise ValueError("Output format not valid. Choose from: 'NetCDF'' or 'GeoTIFF'")

    # Check if years are in the range of available years
    url_info = "https://www.longpaddock.qld.gov.au/silo/gridded-data/"
    for year in years:
        if year > current_year:
            raise ValueError(f"Choose years <= {current_year}")
            return False
        if year < 1889:
            print(f"data is not available for years < 1889.")
            print(f"see for more details: {url_info}")
            return False
        if (year < 1970) & (layername == "evap_pan"):
            print(
                f"{layername} is not available for years < 1970. Automatically set to evap_comb"
            )
            print(f"see for more details: {url_info}")
            layername = "evap_comb"
        if (year < 1957) & (layername == "mslp"):
            print(f"{layername} is not available for years < 1957.")
            print(f"see for more details: {url_info}")
            return False

    # Silo base url
    silo_baseurl = (
        "https://s3-ap-southeast-2.amazonaws.com/silo-open-data/Official/annual/"
    )

    fnames_out = []
    # Download data for each year and save as geotif
    for year in years:
        # Get url
        url = silo_baseurl + layername + "/" + str(year) + "." + layername + ".nc"
        # Download file
        # print(f'Downloading data for year {year} from {url} ...')
        filename = download_file(url, layername, year, outpath)

        # Open file in Xarray
        ds = xarray.open_dataset(filename)
        # select data in bbox:
        if bbox is not None:
            ds = ds.sel(lon=slice(bbox[0], bbox[2]), lat=slice(bbox[1], bbox[3]))
        # Save data
        if (format_out == "nc") | (format_out == "NetCDF"):
            # Save netCDF file
            outfname = layername + "_" + str(year) + "_cropped.nc"
            outfile = os.path.join(outpath, outfname)
            ds.to_netcdf(outfile)
        elif (format_out == "tif") | (format_out == "GeoTIFF"):
            # Save as multi-band geotiff file
            outfname = layername + "_" + str(year) + "_cropped.tif"
            xarray2tif(ds, os.path.join(outpath, outfname), layername)
        # Close file
        ds.close()
        # Remove file
        if delete_temp:
            os.remove(filename)
        # print("Saved " + layername + " for year " + str(year) + " as geotif: ")
        # print(os.path.join(outpath,outfname))
        fnames_out.append(os.path.join(outpath, outfname))

    # Convert netcdf to geotif
    # nc_to_geotif(filename, outpath, layername, year)
    # https://pratiman-91.github.io/2020/08/01/NetCDF-to-GeoTIFF-using-Python.html
    return fnames_out

### Test function ###

def test_get_SILO_raster():
    """
    test script
    """
    layername = "daily_rain"
    years = 2019
    outpath = "silo_test"
    bbox = (130, -44, 153.9, -11)
    # test first for tif output format
    format_out = "tif"
    fnames_out = get_SILO_raster(layername, years, outpath, bbox, format_out)
    assert len(fnames_out) > 0


def test_get_SILO_layers():
    """
    test script
    """
    layernames = ["daily_rain","max_temp"]
    date_start = '2019-01-01'
    date_end = '2020-02-01'
    outpath = "silo_test"
    bbox = (130, -44, 153.9, -11)
    # test first for tif output format
    format_out = "tif"
    fnames_out = get_SILO_layers(layernames, date_start, date_end, outpath, bbox, format_out)
    assert len(fnames_out) > 0
