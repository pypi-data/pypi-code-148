# -*- coding: utf-8 -*-

from rasterstats import zonal_stats
import numpy as np
import geopandas as gpd 
import rasterio as rio 


def stats(shpfile,rasterfile,stats_way,band):
  # shpfile:矢量文件
  # rasterfile:栅格文件
  # stats_way:计算方式
  data = zonal_stats(shpfile,rasterfile,stats = stats_way,band = band)
  values = []
  for value in data:
    values.append(value[stats_way])
  return values


def CV(shpfile,rasterfile,band):
  std = np.array(stats(shpfile,rasterfile,'std',band))
  mean = np.array(stats(shpfile,rasterfile,'mean',band))
  cv = std/mean
  return cv