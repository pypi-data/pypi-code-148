import asyncio
import platform
import time

import grpc
from bluerpc.ble_conn import BLEConn
from bluerpc.ble_scan import BLEScanner
from bluerpc.rpc import common_pb2, gatt_pb2, services_pb2_grpc
from bluerpc.utils import get_version

START_TIME = time.time()


class BlueRPCService(services_pb2_grpc.BlueRPCServicer):
    """
    Implementation of the BlueRPCService
    """
    def __init__(self, name) -> None:
        super().__init__()
        self._name = name
        self._ble_scanner = BLEScanner()

    async def Hello(
        self, request: common_pb2.HelloRequest, context: grpc.aio.ServicerContext
    ) -> common_pb2.HelloResponse:
        return common_pb2.HelloResponse(
            name=self._name,
            version=get_version(),
            uptime=round(time.time() - START_TIME),
            supported_modes=[
                common_pb2.WORKER_MODE_GATT_ACTIVE,
                common_pb2.WORKER_MODE_GATT_PASSIVE,
            ],
            worker_type=common_pb2.WORKER_TYPE_PYTHON,
            operating_system=platform.system(),
            operating_system_version=platform.release(),
        )

    async def BLEScan(
        self, request: gatt_pb2.BLEScanRequest, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEScanResponse:
        """
        BLE Scan Start

        Starts the ble scanner and streams BLEScanResponse for each discovered device
        if already running, returns a message with a status code of ERROR_CODE_SCAN_ALREADY_RUNNING
        once stopped returns a message with a status code of ERROR_CODE_SCAN_STOPPED
        """
        if not self._ble_scanner.running:
            await self._ble_scanner.scan(request.active, request.filters)
            while self._ble_scanner.running:
                async with self._ble_scanner.lock:
                    for i in self._ble_scanner.scan_data:
                        yield i
                    self._ble_scanner.scan_data = []
                    await asyncio.sleep(request.interval / 1000)
            yield gatt_pb2.BLEScanResponse(
                status=common_pb2.StatusMessage(code=common_pb2.ERROR_CODE_SCAN_STOPPED)
            )
        else:
            yield gatt_pb2.BLEScanResponse(
                status=common_pb2.StatusMessage(
                    code=common_pb2.ERROR_CODE_SCAN_ALREADY_RUNNING
                )
            )

    async def BLEScanStop(
        self, request: common_pb2.Void, context: grpc.aio.ServicerContext
    ) -> common_pb2.StatusMessage:
        await self._ble_scanner.stop_scan()
        return common_pb2.StatusMessage(code=common_pb2.ERROR_CODE_OK)

    async def BLEConnect(
        self, request: gatt_pb2.BLEConnectRequest, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEConnectResponse:
        return await BLEConn.get_device(request.device).connect()

    async def BLEDisconnect(
        self, request: gatt_pb2.BLEDevice, context: grpc.aio.ServicerContext
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request).disconnect()

    async def BLEReceiveDisconnect(
        self, request: common_pb2.Void, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEDevice:
        while True:
            yield await BLEConn.disconnect_queue.get()

    async def BLEPair(
        self, request: gatt_pb2.BLEPairingRequest, context: grpc.aio.ServicerContext
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request.device).pair()

    async def BLEPairCode(
        self, request: gatt_pb2.BLEPairingCodeRequest, context: grpc.aio.ServicerContext
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request.device).pair_code(request.code)

    async def BLEUnpair(
        self, request: gatt_pb2.BLEDevice, context: grpc.aio.ServicerContext
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request).unpair()

    async def BLEGetConnectionProperties(
        self, request: gatt_pb2.BLEDevice, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEConnectionPropertiesResponse:
        return await BLEConn.get_device(request).get_props()

    async def BLEGetDevices(
        self, request: common_pb2.Void, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEDevicesResponse:
        return BLEConn.get_devices()

    async def BLEListServices(
        self, request: gatt_pb2.BLEDevice, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLEListServicesResponse:
        return await BLEConn.get_device(request).get_list()

    async def BLEReadCharacteristic(
        self,
        request: gatt_pb2.BLEReadCharacteristicRequest,
        context: grpc.aio.ServicerContext,
    ) -> gatt_pb2.BLEReadResponse:
        return await BLEConn.get_device(request.device).read_characteristic(
            request.service_uuid, request.uuid
        )

    async def BLEReadDescriptor(
        self,
        request: gatt_pb2.BLEReadDescriptorRequest,
        context: grpc.aio.ServicerContext,
    ) -> gatt_pb2.BLEReadResponse:
        return await BLEConn.get_device(request.device).read_descriptor(
            request.service_uuid, request.characteristic_uuid, request.uuid
        )

    async def BLEWriteCharacteristic(
        self,
        request: gatt_pb2.BLEWriteCharacteristicRequest,
        context: grpc.aio.ServicerContext,
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request.device).write_characteristic(
            request.service_uuid,
            request.uuid,
            request.data,
            request.mode != gatt_pb2.BLE_WRITE_MODE_NO_RESPONSE,
        )

    async def BLEWriteDescriptor(
        self,
        request: gatt_pb2.BLEWriteDescriptorRequest,
        context: grpc.aio.ServicerContext,
    ) -> common_pb2.StatusMessage:
        return await BLEConn.get_device(request.device).write_descriptor(
            request.service_uuid,
            request.characteristic_uuid,
            request.uuid,
            request.data,
        )

    async def BLENotification(
        self,
        request: gatt_pb2.BLENotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> common_pb2.StatusMessage:
        if request.subscribe:
            return await BLEConn.get_device(request.device).subscribe(
                request.service_uuid, request.uuid
            )
        else:
            return await BLEConn.get_device(request.device).unsubscribe(
                request.service_uuid, request.uuid
            )

    async def BLEReceiveNotifications(
        self, request: common_pb2.Void, context: grpc.aio.ServicerContext
    ) -> gatt_pb2.BLENotificationResponse:
        while True:
            yield await BLEConn.notif_queue.get()
