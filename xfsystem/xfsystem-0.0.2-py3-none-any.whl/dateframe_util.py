from pyspark.sql.types import StringType, IntegerType, DateType


def asymmetrical_difference(base_collection, secondary_collection):
    difference_set = list(set(base_collection) - set(secondary_collection))
    return difference_set


def get_class_from_type_name(type_name):
    type_class_maps = {"string": StringType(), "int": IntegerType(), "bigint": IntegerType(), "date": DateType()}
    return type_class_maps[type_name]
