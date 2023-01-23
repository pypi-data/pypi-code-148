"""A module for creating pptx from Nanofootball server request 

use create_pptx(...) for real data
or create_from_test_data(...)

Example 1:
----------
    import nf_presentation

    # для тренировки
    pptx_bytes= nf_presentaion.from_training(input_data=training_data_dict)
    # или для одного упражнения
    pptx_bytes= nf_presentaion.from_single_exercise(input_data=exercise_data_dict)
"""

import json
import io
from typing import Union,IO

from nf_presentation.renderers.compact_renderer import CompactRenderer,ExerciseRenderOptions
from .data_classes import TrainingInfo,SingleExerciseInfo
from . import assets
from nf_presentation.logger import logger
from nf_presentation._settings import basic as basic_settings


def return_bytes(func):
    """a decorator that reads the created file objects and returns a bytes array to function standart return """
    def callee(*args,output_file:Union[str,None] =  None,**kwargs):
        #target_stream= output_file or io.BytesIO()

        with io.BytesIO() as stream:

            func(*args,**kwargs,output_file=stream)

            stream.seek(0)
            data=stream.read()
            stream.close()

            if output_file is not None:
                with open(output_file,'wb') as f:
                    f.write(data)

            return data
    return callee

@return_bytes
def from_training(input_data:dict,output_file:Union[str,None] =  None):
    """A function creating a pptx file from giant dict request from Nanofootball server
    Arguments:
        input_data: dict
            'test' - use a test data(2 exercises)
            'test-long' - use a long test data(6 exercises)
            a dict-like object containing server request for making a pptx file
        output_file: str|None
            a destination for rendering pptx, may be a string for saving locally,
            

    Output:
        Byte-array 
            returns a bytes of pptx document. This data can be written to file or be send over http
    """
    if input_data=='test':
        with assets.get_training_data() as f:
            input_data=json.load(f)
    elif input_data=='test-long':
        with assets.get_training_data(short=False) as f:
            input_data=json.load(f)

    training=TrainingInfo(data=input_data)
    with CompactRenderer() as renderer:
        renderer.add_title_slide(name=training.trainer_name)
        renderer.add_training_slide(training)
        for exercise in training.exercises:
            logger.debug(f'rendering {exercise.title}')
            renderer.add_exercise_slide(exercise=exercise)
        renderer.save(to=output_file)

@return_bytes
def from_single_exercise(input_data : Union[dict,str], render_options: dict , output_file : Union[str,None]= None) -> bytes:
    """A function creating a pptx file from exercise object in Nanofootball API
    Arguments:
        input_data: dict | str
            'test' - use a test data
            dict - a dict-like object containing server request for making a pptx file
        output_file: str|None
            a destination for rendering pptx, may be a string for saving locally,
        render_options: dict
            a set of items to show or not show on the rendered scheme
                ex. {
                scheme_1=True,
                scheme_2=True,
                video_1=True,
                ...
                }

    Output:
        Byte-array 
            returns a bytes of pptx document. This data can be written to file or be send over http
    """  
    if input_data=='test':
        with assets.get_exercise_test_data() as f:
            input_data=json.load(f)

    exercise=SingleExerciseInfo(input_data)

    if render_options is None:
        render_options=None
    else:
        render_options=ExerciseRenderOptions(render_options)
    with CompactRenderer() as renderer:

        renderer.add_exercise_slide(exercise,render_options=render_options)
        renderer.save(to=output_file)


# @return_bytes
# def from_training(input_data : Union[dict,str], render_options: dict , output_file : Union[str,None]= None) -> bytes:
#     if input_data=='test':
#         with assets.get_test_data(short=True) as f:
#             input_data=json.load(f)   

#     traning=TrainingInfo(input_data)
#     #render_options=RenderOptions(render_options)
#     renderer=CompactRenderer()

#     renderer.add_exercise_slide(exercise,render_options=render_options)
#     renderer.save(to=output_file)        
#     pass