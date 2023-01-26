# Author: MetariumProject

# standard libraries
from blake3 import blake3


class Hasher(object):

    def __blake3_hash(self, data:dict={}):
        # Create a Blake3 hash object
        hasher = blake3(max_threads=blake3.AUTO)
        # hash file
        with open(data["content"], "rb") as f:
            while True:
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)
        # Return the hexadecimal representation of the hash
        return hasher.hexdigest()

    def _create_hash(self, data:dict={}):
        assert data["type"] == "file"
        assert "content" in data and isinstance(data["content"], str)
        # create a blake3 hash of the data
        data_hash = self.__blake3_hash(data=data)
        # return the hash
        return f"|>blake3|{data_hash}"