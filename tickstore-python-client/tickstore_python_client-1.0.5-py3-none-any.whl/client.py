from code import interact
import protos_pb2_grpc
import protos_pb2
from tickstore.query import Query
import grpc
from tickstore.writers import TickWriter
from tickstore import db
import re
from tickstore.db import UnknownTypeError


class Client:
    def __init__(self, address, interceptors=None, credentials=None):
        self.address = address
        if credentials:
            channel = grpc.secure_channel(address, credentials)
        else:
            channel = grpc.insecure_channel(address)
        if interceptors:
            channel = grpc.intercept_channel(channel, *interceptors)
        self.stub = protos_pb2_grpc.StoreStub(channel)
        res = self.stub.GetMeasurements(protos_pb2.GetMeasurementsRequest())
        for m in res.measurements:
            try:
                db.types.register_object(m.name, m.typeID)
            except UnknownTypeError:
                continue

    def get_measurements(self):
        return self.stub.GetMeasurements(protos_pb2.GetMeasurementsRequest())

    def register_measurement(self, measurement, typeID):
        request = protos_pb2.RegisterMeasurementRequest(
            measurement=protos_pb2.Measurement(name=measurement, typeID=typeID)
        )
        res = self.stub.RegisterMeasurement(request)

        db.types.register_object(measurement, typeID)

    def new_tick_writer(self, measurement, tags):
        tick_w = TickWriter(measurement, tags, None)
        ack = self.stub.Write(tick_w)
        tick_w._ack = ack

        return tick_w

    def new_query(self, qs):
        request = protos_pb2.StoreQueryRequest(
            streaming=qs.streaming,
            batch_size=qs.batch_size,
            timeout=qs.timeout,
            selector=qs.selector,
            to=qs.to,
        )

        if qs.sampler is not None:
            request.tick_sampler.CopyFrom(protos_pb2.TickSampler(
                interval=qs.sampler.interval
            ))
        setattr(request, "from", qs.frm)

        if qs.object_type is None:
            match = re.match('^SELECT ([A-Za-z_]*)(?:\(|\s|$)', qs.selector)
            qs.object_type = match.group(1)

        object_type, delta_type = db.get_object(qs.object_type)

        query_generator = self.stub.Query(request)

        return Query(query_generator, object_type, delta_type)
