from typing import IO
from abc import abstractmethod

from nf_presentation.builders import PresentationBuilder


class BaseRenderer:
    def __init__(self, ratio):
        self.presentation_builder=PresentationBuilder().with_ratio(ratio)
        self._open_streams:list[IO]=[]

    @abstractmethod
    def add_exercise_slide(self):
        pass

    def track_stream(self, stream : IO):
        """a method that marks a stream to be closed on __end__ or close() of renderer"""
        self._open_streams.append(stream)

    def save(self,to:str):
        self.presentation_builder.save(to)

    def __enter__(self) -> 'BaseRenderer':
        return self
    def __exit__(self,type,value,traceback):
        self.close()
    def close(self):
        for stream in self._open_streams:
            stream.close()





        
