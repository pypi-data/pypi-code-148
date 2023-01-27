import requests
import puan.logic.plog as pg
import pickle
import gzip
import base64

from abc import abstractstaticmethod
from puan.ndarray import ge_polyhedron
from puan import Proposition
from dataclasses import dataclass
from typing import Optional, Tuple, Any

@dataclass
class Client:

    url: str
    default_main_branch: str = "main"

    @abstractstaticmethod
    def encode(model) -> str:

        """
            Encode model data to string.

            Returns
            -------
                str
        """

        raise NotImplementedError("`Client` class is an abstract class. Implement `encode` and `decode`")

    @abstractstaticmethod
    def decode(model) -> str:

        """
            Encode model data to string.

            Returns
            -------
                str
        """

        raise NotImplementedError("`Client` class is an abstract class. Implement `encode` and `decode`")

    @staticmethod
    def _extract_data(response, key) -> Tuple[Optional[Any], Optional[str]]:

        """
            Extracts data from response by using given callable `key` function.

            Returns
            -------
            Tuple[Optional[str], Optional[str]]
                Left side is Any data, if it was successfully got. Else None.
                Right side is an error string, if something went wrong. Else None.
        """

        if response.ok:
            data = response.json()
            if data['error']:
                return None, data['error']
            return key(data), None
        return None, response.text

    def commit(self, model: ge_polyhedron, id: str, branch: str = 'main') -> Tuple[Optional[str], Optional[str]]:

        """
            Commits `model` onto branch `branch`.

            Returns
            -------
            Tuple[Optional[str], Optional[str]]
                Left side is the commit sha string, if it was successfully got. Else None.
                Right side is an error string, if something went wrong. Else None.
        """
        return self._extract_data(
            requests.post(
                f"{self.url}/{id}/{branch}/commit", 
                json=self.encode(model),
            ), 
            key=lambda x: x['commit']['sha'],
        )
        

    def checkout(self, sha: str) -> Optional[Any]:

        """
            Checkout committed proposition by sha string.

            Returns
            -------
            Any
        """
        return self._extract_data(
            requests.get(f"{self.url}/commit/{sha}"), 
            key=lambda commit: self.decode(
                commit['commit']['data'],
            ),
        )

    def checkout_latest(self, id: str, branch: str = None) -> Optional[Any]:

        """
            Checkout the latest commit on model id and branch.

            Returns
            -------
            Any
        """
        if branch is None:
            branch = self.default_main_branch

        return self._extract_data(
            requests.get(f"{self.url}/{id}/{branch}/latest"),
            key=lambda commit: self.decode(
                commit['commit']['data'],
            ),
        )

@dataclass
class PropositionClient(Client):

    @staticmethod
    def encode(model) -> str:
        return model.to_b64()

    @staticmethod
    def decode(data: str) -> Proposition:
        return pg.from_b64(data)

    

@dataclass
class PolyhedronClient(Client):

    @staticmethod
    def encode(model) -> str:
        return base64.b64encode(
            gzip.compress(
                pickle.dumps(
                    [model, model.variables, model.index, model.dtype],
                    protocol=pickle.HIGHEST_PROTOCOL,
                ),
                mtime=0,
            )
        ).decode("utf8")

    @staticmethod
    def decode(data: str) -> Proposition:
        try:
            return ge_polyhedron(
                *pickle.loads(
                    gzip.decompress(
                        base64.b64decode(
                            data.encode()
                        )
                    )
                )
            )
        except:
            raise Exception("could not decompress and load polyhedron from string: version mismatch.")