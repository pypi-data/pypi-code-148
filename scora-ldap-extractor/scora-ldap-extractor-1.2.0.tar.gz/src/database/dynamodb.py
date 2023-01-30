import json
from decimal import Decimal
from dotenv import load_dotenv

import numpy as np
from boto3.session import Session
from boto3.dynamodb.conditions import Key

from ..utils.misc import get_env

load_dotenv()
profile_name: str = get_env("AWS_PROFILE_NAME")
region_name: str = get_env("AWS_REGION")
boto3_session: Session = Session(
    profile_name=profile_name or None, region_name=region_name or "us-east-1"
)
dynamodb = boto3_session.resource("dynamodb")


class ItemEncoder(json.JSONEncoder):
    def default(self, obj: any) -> any:
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return Decimal(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, float):
            return Decimal(obj)
        else:
            return super(ItemEncoder, self).default(obj)


def get_data_decoded(data: any) -> any:
    new_data = ItemEncoder().encode(data)
    data_parsed = json.loads(new_data)

    return data_parsed


def get_data_encoded(data: any) -> any:
    data_dumped = json.dumps(data, cls=ItemEncoder)
    data_parsed = json.loads(data_dumped, parse_float=Decimal)

    return data_parsed


def put_item(table_name: str, data: any) -> None:
    table = dynamodb.Table(table_name)
    encoded_data = get_data_encoded(data)
    table.put_item(Item=encoded_data)


def create_tables() -> None:
    pass


def get_data_by_key(table: str, key: str, value: any, field: str | None = None) -> dict:
    data = None

    dynamo_table = dynamodb.Table(table)
    response = dynamo_table.query(KeyConditionExpression=Key(key).eq(value))
    response = response.get("Items")

    if len(response) > 0:
        data = get_data_decoded(response[0])

    if field and data:
        data = {field: data.get(field)}

    return data
