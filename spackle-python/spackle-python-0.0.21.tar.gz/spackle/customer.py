import json
import pprint

from spackle import dynamodb, log
from spackle.exceptions import SpackleException

VERSION = 1


class Customer:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def retrieve(customer_id):
        log.log_debug("Retrieving customer data for %s" % customer_id)
        dynamodb_client = dynamodb.get_client()
        response = dynamodb_client.query(
            KeyConditionExpression="CustomerId = :customer_id",
            FilterExpression="Version = :version",
            ExpressionAttributeValues={
                ":customer_id": {"S": customer_id},
                ":version": {"N": str(VERSION)},
            },
            Limit=1,
        )

        items = response.get("Items")
        if not items:
            raise SpackleException("Customer %s not found" % customer_id)

        data = json.loads(items[0]["State"]["S"])
        log.log_debug("Retrieved customer data for %s: %s" % (customer_id, data))
        return Customer(customer_id, data)

    @property
    def features(self):
        return self.data["features"]

    @property
    def flag_features(self):
        return [f for f in self.data["features"] if f["type"] == 0]

    @property
    def limit_features(self):
        return [f for f in self.data["features"] if f["type"] == 1]

    def enabled(self, key):
        for feature in self.flag_features:
            if feature["key"] == key:
                return feature["value_flag"]

        raise SpackleException("Flag feature %s not found" % key)

    def limit(self, key):
        for feature in self.limit_features:
            if feature["key"] == key:
                if feature["value_limit"] is None:
                    return float("inf")
                return feature["value_limit"]

        raise SpackleException("Limit feature %s not found" % key)

    def __repr__(self):
        return f"<Customer ({self.id}):\n{pprint.pformat(self.data)}>"
