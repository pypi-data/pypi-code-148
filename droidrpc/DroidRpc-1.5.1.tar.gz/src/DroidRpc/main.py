# Python client for connecting to LORA Research's bot services

__author__ = "LORA Research"
__email__ = "asklora@loratechai.com"

import asyncio

from .droid_grpc import DroidStub
from .droid_pb2 import (
    BatchCreateRequest, 
    BatchCreateResponse, 
    BatchHedgeRequest, 
    BatchHedgeResponse,
)
from grpclib.client import Channel
from typing import Optional, Generator, Dict
from numpy.typing import NDArray
import numpy as np
import pandas as pd
from .formatting import (
    array_to_bytes,
    bytes_to_array,
    create_request_dict_to_proto,
    hedge_request_dict_to_proto,
    create_response_proto_to_dict,
    hedge_response_proto_to_dict
)


class Client:
    """
    This is a wrapper for the DROID gRPC client. This is mostly for 
    user-friendliness. For performance, you may want to use the gRPC client
    directly.

    *Note: Input validation is done on the server side. 
    """
    def __init__(
            self,
            host: str = "droid.droid",
            port: int = 50065,
            batch_size: int = 400,
        ):
        """
        Args:
            host (str): The host to connect to.
            port (int): The port to connect to.
            batch_size (int): The maximum number of bots to hedge/create at 
                once in a message. 400 seems to be most optimal for our current
                message size.
        """
        self.host = host
        self.port = port
        self.batch_size = batch_size
        self.channel = Channel(host, port)
        self.stub = DroidStub(self.channel)
    
    def  __repr__(self) -> str:
        return f"""
Droid Client:
    Host: {self.host}
    Port: {self.port}
    Batch Size: {self.batch_size}
    Connected: {bool(self.channel._state)}
        """

    async def close(self) -> None:
        """Closes the gRPC channel."""
        await self.channel.close()
    
    def open(self) -> None:
        """Opens the gRPC channel."""
        self.channel.open()
    
    async def __aenter__(self) -> "Client": 
        return self
    
    async def __aexit__(self, *args) -> None:
        await self.close()

    async def create_bot(
            self,
            ticker: str,
            spot_date: np.datetime64,
            bot_id: str,
            investment_amount: np.float32,
            price: np.float32,
            margin: np.float16,
            fraction: bool,
            multiplier_1: np.float16,
            multiplier_2: np.float16,
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
        ) -> Dict[str, NDArray]:
        """
        Creates a single bot.

        Args:
            ticker: The ticker of the underlying asset.
            spot_date: Bot start date.
            bot_id: Composite id of bot type, option type, and holding period.
            investment_amount: Initial investment amount.
            price: Current price of stock.
            margin: Margin ratio (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            multiplier_1: Multiplier (1) for target price level (1); 
                e.g. [Classic] - [stop loss] should be negative. 
            multiplier_2: Multiplier (2) for target price level (2), 
                must be > Multiplier (1).
            r: Interest rate.
            q: Dividend yield.

        Returns:
            dict: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')
        inputs = {k: np.array([v]) for k, v in inputs.items()}
        for k, v in inputs.items():
            print(k, v)
        await self.create_bots(inputs)
        
    
    async def create_bots(
            self,
            ticker: NDArray[str],
            spot_date: NDArray[np.datetime64],
            bot_id: NDArray[str],
            investment_amount: NDArray[np.float32],
            price: NDArray[np.float32],
            margin: NDArray[np.float16],
            fraction: NDArray[bool],
            multiplier_1: NDArray[np.float16],
            multiplier_2: NDArray[np.float16],
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
            t: Optional[np.float32] = None,
        ) -> dict:
        """
        Creates a batch of bots.

        Args:
            ticker: The tickers of the underlying asset.
            spot_date: Bot start dates.
            bot_id: Composite ids of bot type, option type, and holding period.
            investment_amount: Initial investment amounts.
            price: Current price of the stocks.
            margin: Margin ratios (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            multiplier_1: Multipliers (1) for target price levels (1); 
                e.g. [Classic] - [stop loss] should be negative. 
            multiplier_2: Multipliers (2) for target price levels (2), 
                must be > Multiplier (1).
            r: Interest rates.
            q: Dividend yields.
            t: days to maturity / 365.

        Returns:
            dict: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')

        def batch(buf, batch_size) -> Generator[NDArray]:
            """Breaks down an array into batches"""
            for start in range(0, len(buf), batch_size):
                yield buf[start:start + batch_size]
        
        # Create generators
        f = batch
        batched_inputs = {k: f(v, self.batch_size) for k, v in inputs.items()}

        # TODO
        # async with self.stub.CreateBots() as stream:
        #     for ticker in batched_inputs['ticker']
        #         # TODO: hedge_request_dict_to_proto()
        #         msg = {k: v.next() for k, v in batched_inputs}
        #         await stream.send_message(
        #              
        #           )
        #         resp = await stream.recv_message()
        #         hedge_response_proto_to_dict(resp)
        #     yield resp
        ...

    async def create_bots_from_dataframe(
            self,
            create_inputs: pd.DataFrame,
        ) -> pd.DataFrame:
        """
        Creates a batch of bots from a dataframe containing inputs.

        Args:
            create_inputs: Should document the schema somewhere..
        """
        msgs = self._input_stream(create_inputs, BatchCreateRequest)
        async with self.stub.CreateBots.open() as stream:
            async for msg in msgs:
                print("Sending message: ")
                await stream.send_message(msg)
                print("Receiving message: ")
                resp = await (stream.recv_message())
                print("Yielding message: ")
                resp = create_response_proto_to_dict(resp)
                yield pd.DataFrame.from_dict(resp)
            await stream.end()

    async def hedge_bots_from_dataframe(
            self,
            create_inputs: pd.DataFrame,
        ) -> pd.DataFrame:
        """
        Hedges a batch of bots from a dataframe containing inputs.

        Args:
            hedge_inputs: Should document the schema somewhere..
        """
        msgs = self._input_stream(create_inputs, BatchHedgeRequest)
        async with self.stub.HedgeBots.open() as stream:
            async for msg in msgs:
                print("Sending message: ")
                await stream.send_message(msg)
                print("Receiving message: ")
                resp = await (stream.recv_message())
                print("Yielding message: ")
                resp = hedge_response_proto_to_dict(resp)
                yield pd.DataFrame.from_dict(resp)
            await stream.end()

    async def _input_stream(self, inputs: pd.DataFrame, serializer):
        """
        Auxiliary function for create_bots_from_dataframe().
        Convert dataframe inputs into byte -> serialized input for grpc

        *Note: This is a terrible way to do this, I will implement a version 
        of this function that accepts generators as input in the future.
        """
        n_batch = np.ceil(len(inputs) / self.batch_size)
        chunks = np.array_split(inputs, n_batch)
        for i in chunks:
            byte_input = {
                col: array_to_bytes(i[col].to_numpy().astype(str))
                if "date" not in col
                else array_to_bytes(pd.to_datetime(i[col]).dt.date
                                    .to_numpy().astype(str))
                for col in i}
            serialized_input = serializer(**byte_input)
            yield serialized_input
    
    # def _output_stream(self, responses: dict) -> pd.DataFrame:
    #     """
    #     Auxiliary function for create_bots_from_dataframe().
    #     Convert grpc byte response into dataframe
    #     """
    #     for i in responses:
    #         output = {field: bytes_to_array(value)
    #                   for (field, value) in protobuf_to_dict(i).items()}
    #         output = pd.DataFrame(output)
    #         yield output.convert_dtypes()

    # TODO
    async def hedge_bots(
            self,
            props: dict,
        ) -> dict:
        """
        Hedges a batch of bots.

        Args:
            props (dict): A dictionary of bot properties.

        Returns:
            dict: A dictionary of bot properties.
        """
        async with self.stub.HedgeBots() as stream:
            await stream.send_message(props)
            resp = await stream.recv_message()
        return resp

if __name__ == '__main__':
    client = Client()
    bot = client.create_bot(
        ticker= 'AAPL.O',
        spot_date= '2023-01-19',
        bot_id= 'UNO_ITM_025',
        investment_amount= 10000,
        price= 1000,
        margin= 1,
        fraction= False,
        multiplier_1= -2,
        multiplier_2= 1,
        r= 0.12255669,
        q= 9.55143566e-06,
    )
    print(bot)
