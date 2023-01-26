# Author: MetariumProject

# local libraries
from ...utils import ServiceAlreadyExistsError
from ..base import SubstrateBaseEncoder
from .hasher import Hasher


class SubstrateServiceUpdaterAsRoot(SubstrateBaseEncoder, Hasher):

    FUNCTION_CALL = "force_update_service_info"

    def is_valid_data(self, data: dict = {}):
        assert "scribe" in data and isinstance(data["scribe"], str)# substrate address
        assert "service" in data and isinstance(data["service"], str)# substrate address
        assert "id" in data and isinstance(data["id"], str)# service id, eg IPFS peer id
        assert "ip_address" in data and isinstance(data["ip_address"], str)# IP address
        assert "swarm_key" in data and isinstance(data["swarm_key"], str)# blake3 hash of the swarm key file
        assert "status" in data and isinstance(data["status"], str)# blake3 hash of the status file
        assert "rff" in data and isinstance(data["rff"], str)# IPFS cid of the rff file
        assert "deleted" in data and isinstance(data["deleted"], bool)# active or deleted
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        data["status"] = self._create_hash(
            data={"type": "file", "content": data["status"]}
        )
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'scribe': data["scribe"],
                'service_address': data["service"],
                'service_id': data["id"],
                'ip_address': data["ip_address"],
                'swarm_key': data["swarm_key"],
                'status_file': data["status"],
                'rff_file': data["rff"],
                'deleted': data["deleted"]
            }
        )
