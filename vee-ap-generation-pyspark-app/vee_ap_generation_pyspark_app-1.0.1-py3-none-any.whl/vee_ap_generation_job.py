#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from logging.config import fileConfig

from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql import functions as F

from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType,StringType,BooleanType

#need spark 3.2 to include pyspark.pandas
import pyspark.pandas as ps

import sys
sys.path.append("/workspace/pyspark-app")
sys.path.append("/mnt/app/pyspark-app")

road_graph = __import__("road_network_graph")
road_utils = __import__("ndm_road_segment_utils")
ap_gen = __import__("ap_generation_road_network")
ap_feature = __import("ap_featurization")

# from . import road_network_graph as road_graph
# from . import ndm_road_segment_utils as road_utils
# from . import ap_generation_road_network as ap_gen
# from . import ap_featurization as ap_feature

from geopy.distance import lonlat, distance
import json
import networkx as nx
import numpy as np
import os
import pandas as pd
from rtree import index

    
from shapely.wkt import loads
import os
import shutil


poi_cols = ["poiId", "tier", "poiLat", "poiLng",  "address", "street","pref_name"]

poi_dtypes = {'poiId': np.int64, 'tier': str, 'poiLat': np.float32, 'poiLng': np.float32, 'address': str, 'street': str, 'pref_name': str}

pedestrian_form_of_way = ["CROSSWALK", "ESCALATOR", "LOGICAL_CONNECTION", "MOVING_WALKWAY", "OPEN_TRAFFIC_AREA_CONNECTION", "PATHWAY", "RAMPED_PATHWAY", "SIDEWALK", "SINGLE_TRACK_TRAIL", "STAIRS" ]

# Extract below road segment attributes from roas segment proto and use them as the input of VEE generation process
road_segment_cols= [
          'tile', \
          'featureId', \
          'geometry', \
          'form_of_way',\
          'pedestrian_form_of_way', \
          'is_multiply_digitized', \
          'number_of_lanes', \
          'number_of_through_lanes',\
          'surface_material', \
          'to_node', \
          'from_node', \
          'zLevelFrom', \
          'zLevelTo', \
          'forward_direction.isVehicleNavigable', \
          'reverse_direction.isVehicleNavigable'
]

#Below attributes are those used by VEE generation process
#keep the attribute name same as before otherwise we need to update all following functions
segment_cols = \
 [
         'shard', \
         'feature_id', \
          'wkt_geom', \
          'form_of_way',\
          'pedestrian_form_of_way', \
          'multi_dig', \
          'lane_count', \
          'thru_lane',\
          'surf_mat', \
          'to_node', \
          'from_node', \
          'z_from', \
          'z_to', \
          'forw_nav', \
          'back_nav', \
          'haversine_meters'
]

segment_dtypes = {
    'shard': str,
    'feature_id': np.int64, 
    'wkt_geom': str, 
    'form_of_way': str,
    'pedestrian_form_of_way': np.bool8, 
    'multi_dig': np.bool8, 
    'lane_count': np.float32,
    'thru_lane': np.float32,
    'surf_mat': str, 
    'to_node': np.int64, 
    'from_node': np.int64, 
    'z_from': np.float32,
    'z_to': np.float32,
    'forw_nav': np.bool8,
    'back_nav': np.bool8, 
    'haversine_meters': np.float32
}


@udf(returnType=BooleanType()) 
def get_pedestrian_form_of_way(form_of_way):
        if form_of_way in pedestrian_form_of_way:
            return True
        return False

@udf(returnType=DoubleType()) 
def get_segment_length(wkt_linestring):
    row_parsed = loads(wkt_linestring)
    coords = list(zip(row_parsed.xy[1], row_parsed.xy[0]))
    n_coords = len(coords) - 1
    dist = 0.0
    for i in range(0, n_coords):
        dist += distance(coords[i], coords[i + 1]).meters
    return dist

from array import *
@udf(returnType=StringType()) 
def get_street(address):
    if  address is not None and len(address) != 0:
        return ', '.join(address)
    return ''


def find_vee_aps_for_pois(x):
    shard = x[0]
    poi = list(x[1][0])
    print("poi count = "+ str(len(poi)))
    segment = list(x[1][1])
    print("segment count = " + str(len(segment)))
    
    poi_df = pd.DataFrame(poi)
#   need to assign columns names other wise they are index 0, 1... can't access column by names
    poi_df.columns = poi_cols
    segments_df = pd.DataFrame(segment)
    segments_df.columns = segment_cols
    
    return find_vee_aps(shard, poi_df, segments_df)

def find_vee_aps(shard, pois, segments):
#     segments = road_segments.loc[~pd.isnull(road_segments.haversine_meters)
    print("start processing shard " + shard)
    for dt in poi_dtypes.keys():
        pois[dt] = pois[dt].astype(poi_dtypes[dt])
        
    for dt in segment_dtypes.keys():
        segments[dt] = segments[dt].astype(segment_dtypes[dt])

    graph_creator = road_graph.RoadNetworkGraph(segments)
    
    interior_graph_reversed = graph_creator.get_graph_copy_subset_fows(road_utils.INTERIOR_ROADS + road_utils.NON_NAVIGABLE_ROADS).reverse()
    igr_cc = nx.weakly_connected_components(interior_graph_reversed)
    cc_list = list(igr_cc)
    cc_dict = {}
    for i, c in enumerate(cc_list):
        for n in c:
            cc_dict[n] = i
            
    tree = index.Index(graph_creator.graph_generator())
    segments.set_index('feature_id', inplace=True)

    generated_vee_aps = ap_gen.generate_vee_aps_for_pois(pois, segments, graph_creator.graph, interior_graph_reversed, cc_dict, cc_list, tree)
    
    if generated_vee_aps.empty == False:
        pois[['generated_aps', 'num_generated_aps', 'num_generated_address_aps']] = pois.apply(lambda x: add_generated_aps(x, generated_vee_aps, "DRIVING", "VEE"), axis=1)
        generated_vee_aps = ap_feature.add_aggregated_features(generated_vee_aps)

    poi_strings = pois.to_csv(header=True, index=False).strip('\n').split('\n')
    generated_vee_aps_strings = generated_vee_aps.to_csv(header=True, index=False).strip('\n').split('\n')
    return poi_strings, generated_vee_aps_strings

def toCSVLine(data):
    return ','.join(str(d) for d in pois)

def add_generated_aps(poi, generated_aps, ap_type, subtype):
    aps = []
    i, j = 0, 0
    aps_df = generated_aps.loc[generated_aps.poi_id == poi.poiId]
    for id_, ap in aps_df.iterrows():
        ep = {'point': json.loads(ap.ap_coordinates), 'type': ap_type, 'subtype': subtype}
        aps.append(ep)
        i += 1
#     address_aps_df = sample_address_aps_df.loc[sample_address_aps_df.poi_id == str(poi.name)]
#     for id_, ap in address_aps_df.iterrows():
#         ep = {'point': json.loads(ap.ap_coordinates), 'type': "DRIVING", 'subtype': 'Address'}
#         aps.append(ep)
#         j += 1
    return pd.Series((json.dumps(aps), i, j))

def removeOuput(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


if __name__ == "__main__":
    fileConfig(os.getenv('PLATFORM_PYTHON_SPARK_LOG_CONF'))
    logger = logging.getLogger()
    conf = SparkConf().setAll([
        ("fs.blob.impl","pie.spark.blob.fs.ObjectFileSystem"),
        ("fs.blob.028MKIAO02PL6T1T9COUTJM.awsAccessKeyId", "MKIAO02PL6T1T9COUTJM"),
        ("fs.blob.028MKIAO02PL6T1T9COUTJM.awsSecretAccessKey", "E06727B4B742A77EE0A7C778F97344B43190D3FB4882D1E415858BE29E3A230E"),
        ("fs.blob.028MKIAO02PL6T1T9COUTJM.endpoint", "store-028.blobstore.apple.com"),
        ("spark.hadoop.mapred.output.compression.codec", "com.hadoop.compression.lzo.LzoCodec")
    ])
    spark = SparkSession.builder.config(conf=conf).appName("VeeAPGenerationJob").getOrCreate()


    log_path = os.getenv('PLATFORM_PYTHON_SPARK_LOG_CONF', 'n/a')
    if log_path != 'n/a':
     fileConfig(log_path)
    else:
     print('file not found')

    ps.set_option("compute.default_index_type", "distributed")

    #local test path
    # ndm_path="/Users/yunhu/dev/access-point-creation/notebooks/data/test/ndm"
    # poi_path = "/Users/yunhu/dev/access-point-creation/notebooks/data/test/pois"
    # output_path = "/Users/yunhu/dev/access-point-creation/notebooks/data/test/output"

    ndm_path="blob://028MKIAO02PL6T1T9COUTJM/maps-osm-data-mining/test/tian-du-poi/feature-sets/road-segment/FCS-test-output-5"
    # whole world POI data
    # whole_world_poi_path="blob://028MKIAO02PL6T1T9COUTJM/test/matthieu/poi/7/deltaOutput"
    # US POI data
    poi_path="blob://028MKIAO02PL6T1T9COUTJM/test/yun/access-point-creation/us-poi"
    output_path = "blob://028MKIAO02PL6T1T9COUTJM/test/yun/access-point-creation/output/12052022"


    road_segments = spark.read.parquet(ndm_path).select( \
        "tile", \
        "featureId", \
        "geometry",  \
        F.col('roadSegmentProto.form_of_way').alias('form_of_way'), \
        F.col('roadSegmentProto.is_multiply_digitized').alias('is_multiply_digitized'), \
        F.col('roadSegmentProto.number_of_lanes').alias('number_of_lanes') ,  \
        F.col('roadSegmentProto.number_of_through_lanes').alias('number_of_through_lanes') ,  \
        F.col('roadSegmentProto.road_surface').getItem('surface_material').alias('surface_material'), \
        F.col('roadSegmentProto.to_node').alias('to_node') ,  \
        F.col('roadSegmentProto.from_node').alias('from_node') ,  \
        "zLevelFrom", \
        "zLevelTo", \
        F.col('roadSegmentProto.direction')[0].getItem('is_navigable').alias('forwardDirectionIsVehicleNavigable'), \
        F.col('roadSegmentProto.direction')[1].getItem('is_navigable').alias('reverseDirectionIsVehicleNavigable') \
    )

    road_segments = road_segments.withColumn("pedestrian_form_of_way", get_pedestrian_form_of_way(col("form_of_way")))

    road_segments = road_segments.select(
        road_segments.columns[0],
        road_segments.columns[1],
        road_segments.columns[2],
        road_segments.columns[3],
        road_segments.columns[14],
        road_segments.columns[4],
        road_segments.columns[5],
        road_segments.columns[6],
        road_segments.columns[7],
        road_segments.columns[8],
        road_segments.columns[9],
        road_segments.columns[10],
        road_segments.columns[11],    
        road_segments.columns[12],
        road_segments.columns[13]    
    )
    #road_segments.printSchema()

    road_segments = road_segments.select( \
             col("tile").alias('shard'), \
             col("featureId").alias('feature_id'), \
             col('geometry').alias('wkt_geom'), \
             col('form_of_way'), \
             col('pedestrian_form_of_way'), \
             col('is_multiply_digitized').alias('multi_dig'), \
             col('number_of_lanes').alias('lane_count'), \
             col('number_of_through_lanes').alias('thru_lane'), \
             col('surface_material').alias('surf_mat'), \
             col('to_node'), \
             col('from_node'), \
             col('zLevelFrom').alias('z_from'), \
             col('zLevelTo').alias('z_to'), \
             col('forwardDirectionIsVehicleNavigable').alias('forw_nav'), \
             col('reverseDirectionIsVehicleNavigable').alias('back_nav') 
             ) \
     .filter(col('geometry').isNotNull()) \
     .drop("forwardDirectionIsVehicleNavigable") \
     .drop("reverseDirectionIsVehicleNavigable") \
     .drop("geometry") \
     .drop("surface_material") \
     .drop("is_multiply_digitized") \
     .drop("lane_through_count") \
     .drop("zLevelFrom") \
     .drop("zLevelTo")   



        
    segments_with_length = road_segments.withColumn("haversine_meters", get_segment_length(col("wkt_geom"))) \
                            .dropDuplicates(["feature_id"])
    segments_with_length = segments_with_length.select(*segment_cols) \
            .filter((col("from_node").isNotNull()) & (col("to_node").isNotNull()))

    segments_with_length.printSchema()

    #load POI data
    pois = spark.read.parquet(poi_path)
    pois = pois.select("Shard","id", "popularity_score.htt_tier", 
                                       "LocationLatitude", "LocationLongitude", 
                                       "localized_addresses.address.formattedAddressLine", "pref_name") \
                    .withColumnRenamed("htt_tier", "tier") \
                    .withColumnRenamed("id", "poiId") \
                    .withColumnRenamed("Shard", "shard") \
                    .withColumnRenamed("LocationLatitude", "poiLat") \
                    .withColumnRenamed("LocationLongitude", "poiLng") 
    #                 .dropDuplicates(["poiId"]) 
    pois = pois.withColumn("address", pois["formattedAddressLine"].getItem(0)) 
    pois = pois.drop("formattedAddressLine")
    pois = pois.withColumn("street", get_street(col("address")))
    pois = pois.select("shard", *poi_cols)


    poi_rdd = pois.rdd.map(lambda x: (x[0], x[1:]))

    segment_rdd=segments_with_length.rdd.map(lambda x: (x[0], x[0:]))

    # removeOuput(output_path)

    tuple_result = poi_rdd.cogroup(segment_rdd) \
    .filter(lambda x: len(list(x[1][0])) and len(list(x[1][1]))).map(lambda x: find_vee_aps_for_pois(x)) 

    from pyspark.storagelevel import StorageLevel
    tuple_result.persist(StorageLevel.MEMORY_AND_DISK)

    tuple_result.map(lambda tuple : tuple[0]).map(lambda x: '\n'.join(x)).saveAsTextFile(output_path + "/aps")
    tuple_result.map(lambda tuple : tuple[1]).map(lambda x: '\n'.join(x)).saveAsTextFile(output_path + "/aps-features")

    spark.stop()
