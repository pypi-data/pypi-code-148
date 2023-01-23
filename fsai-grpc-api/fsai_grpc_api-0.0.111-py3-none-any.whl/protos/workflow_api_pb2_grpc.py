# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from fsai_grpc_api.protos import workflow_api_pb2 as fsai__grpc__api_dot_protos_dot_workflow__api__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class WorkflowApiStub(object):
    """The workflow service is responsible for managing the workflows of a mission. 
    It is responsible for creating a workflow, queuing a mission scan, listing mission scans, and listing queued mission scans.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindOrCreateWorkflow = channel.unary_unary(
                '/WorkflowApi/FindOrCreateWorkflow',
                request_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowRequest.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowResponse.FromString,
                )
        self.QueueMissionScan = channel.unary_unary(
                '/WorkflowApi/QueueMissionScan',
                request_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanRequest.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanResponse.FromString,
                )
        self.ListMissionScans = channel.unary_unary(
                '/WorkflowApi/ListMissionScans',
                request_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansRequest.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansResponse.FromString,
                )
        self.ListQueuedMissionScans = channel.unary_unary(
                '/WorkflowApi/ListQueuedMissionScans',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListQueuedMissionScansResponse.FromString,
                )
        self.TransitionMissionScanStatus = channel.unary_unary(
                '/WorkflowApi/TransitionMissionScanStatus',
                request_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusRequest.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusResponse.FromString,
                )


class WorkflowApiServicer(object):
    """The workflow service is responsible for managing the workflows of a mission. 
    It is responsible for creating a workflow, queuing a mission scan, listing mission scans, and listing queued mission scans.
    """

    def FindOrCreateWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueueMissionScan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListMissionScans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListQueuedMissionScans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TransitionMissionScanStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkflowApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindOrCreateWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.FindOrCreateWorkflow,
                    request_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowRequest.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowResponse.SerializeToString,
            ),
            'QueueMissionScan': grpc.unary_unary_rpc_method_handler(
                    servicer.QueueMissionScan,
                    request_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanRequest.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanResponse.SerializeToString,
            ),
            'ListMissionScans': grpc.unary_unary_rpc_method_handler(
                    servicer.ListMissionScans,
                    request_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansRequest.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansResponse.SerializeToString,
            ),
            'ListQueuedMissionScans': grpc.unary_unary_rpc_method_handler(
                    servicer.ListQueuedMissionScans,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListQueuedMissionScansResponse.SerializeToString,
            ),
            'TransitionMissionScanStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.TransitionMissionScanStatus,
                    request_deserializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusRequest.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'WorkflowApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkflowApi(object):
    """The workflow service is responsible for managing the workflows of a mission. 
    It is responsible for creating a workflow, queuing a mission scan, listing mission scans, and listing queued mission scans.
    """

    @staticmethod
    def FindOrCreateWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkflowApi/FindOrCreateWorkflow',
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowRequest.SerializeToString,
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.WorkflowResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueueMissionScan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkflowApi/QueueMissionScan',
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanRequest.SerializeToString,
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.QueueMissionScanResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListMissionScans(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkflowApi/ListMissionScans',
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansRequest.SerializeToString,
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListMissionScansResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListQueuedMissionScans(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkflowApi/ListQueuedMissionScans',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.ListQueuedMissionScansResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TransitionMissionScanStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/WorkflowApi/TransitionMissionScanStatus',
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusRequest.SerializeToString,
            fsai__grpc__api_dot_protos_dot_workflow__api__pb2.TransitionMissionScanStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
