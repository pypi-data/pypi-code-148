from abc import abstractmethod
from typing import IO

from .settings import (
                    EMPY_DESCRIPLION_REPLACEMENT,
                    EMPTY_TRAINER_NAME_REPLACEMENT,
                    UNKNOWN_GROUP_ID_NAME_REPLACEMENT)
from nf_presentation._settings import data as data_settings

from ._settings.basic import create_player_link
from nf_presentation.scheme_renderer import SchemeRenderer, NewSchemeRenderer
from nf_presentation.logger import logger

class DictWrapper:
    def __init__(self, raw_data:dict):
        self.raw_data=raw_data

    # maybe this decorators should be plkaced here, inside a class
    # @from_field, from_raw_dict


def from_field(field_name:str=None,default=None,warn_if_none:str=None):
    """a decorator for DictWrapperClass
    creates a property returning self.raw_data['field_name']

    [optional]field_name: str
        a field name to extract
    [optional]default: any
        a default return if cant get the field
    [optional]warn: str
        a warning message if attempting to return none
    
    use:
    class Exercise(DictWrapper)
        @from_field('id')
        def my_id(self):
            pass
    
    ex=Exercise(data)
    print(ex.id)  # returns data['id'] / ex.raw_data['id']"""
    def decorator(func):
        nonlocal field_name,default
        @property
        def callee(self:DictWrapper, *args,**kwargs):
            nonlocal field_name,default,func
            if args or kwargs:
                logger.warn('@from_field receives arguments more than self')

            #testing if classes configured ok, causes slow down ;(                
            try:
                if func(self,*args,**kwargs):
                    logger.warn(f'@from_field a wrapped property {self.__class__.__name__}.{func.__name__} attemps to return something, maybe class configured badly. try \n@from_field()\n    def field(self): pass')
            except Exception as e:
                logger.warn(f'@from_field a wrapped property {self.__class__.__name__}.{func.__name__} causes exception\n{e} \n, maybe class configured badly. try \n@from_field()\n    def field(self): pass')

            if field_name is None:
                field_name=func.__name__
            value=self.raw_data.get(field_name)
            if value is None:
                if warn_if_none:
                    logger.warning(f'{self}: {warn_if_none}. returning "{default}"')
                value=default
            return value
        return callee
    return decorator

def from_raw_data(func):
    """a decorator for DictWrapperClass
    creates a property returning self.raw_data[decorated_function_name]

    default: any
        a default return if cant get the field
    
    use:
    class Exercise(DictWrapper)
        @from_raw_data
        def my_id(self):
            pass
    
    ex=Exercise(data)
    print(ex.id)  # returns data['id'] / ex.raw_data['id']"""
    @from_field(func.__name__)
    def callee(self):
        pass
    return callee

#some TODO's
# if ne need a path a decorator can be a class returning a class so we line
# from_field('players').from_dict('name') etc
#
# or it can be like a argument or a stack of decorators
#
# ALSO:
# i would like to try a laziness wrapper creating a lazy field and if needed filling added with items of some type

class GroupInfo:
    """a class representing a position of exercise, in A1, A2, A3 B3 and others"""
    _group_names={
        1:'A',
        2:'B',
        3:'C'
    }
    def __init__(self, group_id:int, order:int):
        self._group_id=group_id
        self._order=order
    @property
    def id(self):
        return self._group_id
    @property
    def name(self):
        return self._group_names.get(self.id,UNKNOWN_GROUP_ID_NAME_REPLACEMENT)
    def __str__(self):
        return f'{self.name}{self._order}'

class AdditionalInfo:
    def __init__(self,data:dict):
        self.raw_data=data
    @property 
    def name(self):
        return self.raw_data.get('additional_name',{}).get('ru')
    @property
    def value(self):
        return self.raw_data.get('note')









# a class for exercise info of single exercise, it has a different scructure :(

class MediaLink:
    def __init__(self, raw_data):
        self.raw_data:dict=raw_data
    @property
    def exist(self):
        return self.id!=-1
    @property
    def id(self):
        return self.raw_data.get('id')
    @property
    def nftv_id(self):
        return self.raw_data.get('links',{}).get('nftv')
    @property
    def youtube_id(self):
        return self.raw_data.get('links',{}).get('youtube')
    @property
    def nftv_player(self):
        return create_player_link(self.nftv_id)

class Scheme:
    @abstractmethod
    def to_stream(self)-> IO:
        pass

class OldScheme(Scheme):
    def __init__(self, svg_text:str):
        self.svg_text=svg_text
    def to_stream(self) -> IO:
        return SchemeRenderer().to_stream(self.svg_text)

class NewScheme(Scheme):
    def __init__(self, scheme_id):
        self.scheme_id=scheme_id
    def to_stream(self) -> IO:
        return NewSchemeRenderer().to_stream(self.scheme_id)

    

class SingleExerciseInfo:
    """A class representing info we get for an exercise to a python object
    
    represents a data entity in nanofootball.com/exercises
    its a bit defferent from entinity of /training/exercise"""
    _media_fields=['video_1','video_2','animation_1','animation_2']
    _sheme_fields=['scheme_1','scheme_2']

    def __init__(self, raw_data:dict):
        self.raw_data=raw_data
    @property
    def id(self):
        return self.raw_data.get('id')
    @property
    def additional_params(self) -> dict:
        """returning exercise.additinal_params as dict, converting from list[dict]"""
        return { entry.get('title',''):entry.get('value','') for entry in self.raw_data.get('additional_params',{})}
    @property
    def description(self):
        return self.raw_data.get('description','')
    @property
    def title(self):
        return self.raw_data.get('title','')
    @property
    def old_schemes(self):
        return self.raw_data.get('scheme_data',[])
    @property
    def video_1(self)-> MediaLink:
         return MediaLink(self.raw_data.get('video_1'))
    @property
    def video_2(self)-> MediaLink:
         return MediaLink(self.raw_data.get('video_2'))
    @property
    def animation_1(self)-> MediaLink:
         return MediaLink(self.raw_data.get('animation_1'))
    @property
    def animation_2(self) -> MediaLink:
         return MediaLink(self.raw_data.get('animation_2'))
    def get_media(self, field_name) -> MediaLink:
        """returns a media link to videos
        Attributes:
            field_name:'video_1','video_2','animation_1',...
        
        Returns:
            a MediaLink object or None
            """
        if field_name not in self._media_fields:
            logger.warn(f'trying to get media field "{field_name}" from exercise_data, safe choices are {self._media_fields}')
        return getattr(self,field_name)
    @property
    def medias(self):
        """returns a collection of medias like video1, video2 and others"""
    @property
    def media_as_dict(self):
        """returns a dict of existing(!) medias
            ex.
            {
                'video_1':MediaLink(...),
                'animation_1':MediaLink(...)"""
        return {field:self.raw_data.get(field) for field in self._media_fields}
    @property
    def scheme_1(self):
        scheme_id=self.raw_data.get('scheme_1')
        if scheme_id:
            return NewScheme(scheme_id=scheme_id)
        else:
            return OldScheme(svg_text=self.old_schemes[0])
    @property
    def scheme_2(self):
        scheme_id=self.raw_data.get('scheme_2')
        if scheme_id:
            return NewScheme(scheme_id=scheme_id)
        else:
            return OldScheme(svg_text=self.old_schemes[1])
    def get_scheme_by_name(self,name:str) -> Scheme:
        if name not in self._sheme_fields:
            logger.warn(f'attemping to get scheme with name "{name}", while allowed names are {self._sheme_fields}')
        #TODO add a fallback if scheme not found
        return getattr(self,name)

class TrainingExerciseInfo(SingleExerciseInfo):
    """A class representing info we get for an exercise to a python object
    representing a data entity in nanofootball.com/training/exercise"""

    @property
    def title(self):
        title_=self.raw_data.get('exercise_name',{}).get('ru',None)
        if title_ is None:
            logger.error(f'cant get title for exercise with id={self.id}.falling back to empty title')
            return ' '
        else:
            return title_

    @property
    def old_schemes(self):
        return list(self.raw_data.get('exercise_scheme',{}).values())

    @property
    def _videos(self):
        return self.raw_data.get('exercise_data',{}).get('videos',[])
    @property
    def video_1(self)-> MediaLink:
        if len(self._videos)>0:
            return MediaLink(self._videos[0])
        else:
            return None
    @property
    def video_2(self)-> MediaLink:
        if len(self._videos)>1:
            return MediaLink(self._videos[1])    
        else:
            return None
    @property
    def animation_1(self) -> MediaLink:
        logger.warn(f'{self}: animation_1 field is not implemented in TrainingExerciseInfo. Returning None always')
        return None
    @property
    def animation_2(self) -> MediaLink:
        logger.warn(f'{self}: animation_2 field is not implemented in TrainingExerciseInfo. Returning None always')
        return None
    @property
    def duration(self) -> int:
        return self.raw_data.get('duration',0)

    @from_field('group',-1)
    def group_id(self): pass

    @property
    def group_name(self):
        return data_settings.EXERCISE_GROUP_NAME_BY_ID.get(self.group_id,data_settings.EXERCISE_GROUP_NAME_UNKNOWN)
    @from_raw_data
    def order(self): pass # order of exercise in group
    
    @property
    def prefix(self) -> str:
        """a prefix like A1,B2"""
        return f'{self.group_name}{self.order}'
    
    @from_raw_data
    def duration(self): pass
    
    def __str__(self):
        return f"[{self.title}]"

class TrainingInfo(DictWrapper):
    def __init__(self,raw_data:dict):
        super().__init__(raw_data=raw_data)
        self._exercises : list[TrainingExerciseInfo] = None

    @from_field('event_id',default='unknown_id')
    def id(self): pass

    @from_field('event_date',default='')
    def date(self) -> str: pass
    
    @from_field('event_time',default='')
    def time(self) -> str: pass

    @from_field(default=[])
    def objectives(self) -> list[str]:
        """returning an array of objectives containing main_objective and tasks"""
        pass
    @property
    def main_objective(self) -> str:
        if len(self.objectives)>0:
            return self.objectives[0]
        else:
            logger.error(f'training[{self.id}] cant get main_objective. amount of objectives is lesser that 1. returning {data_settings.TRAINING_DEFAULT_MAIN_OBJECTIVE}')
            return None
    @property
    def tasks(self)-> list[str]:
        if len(self.objectives)>1:
            return self.objectives[1:]
        else:
            logger.error(f'training[{self.id}] cant get tasks. amount of objectives is lesser that 2. returning {data_settings.TRAINING_DEFAULT_TASKS}')
            return None
    @from_field('load_type',default='')
    def load(self):
        "Нагрузка" 
        pass

    @from_raw_data
    def field_size(self): pass
    @from_raw_data
    def keywords_1(self): pass
    @from_raw_data
    def keywords_2(self): pass

    @property
    def team_name(self):
        return self.raw_data.get('team_info',{}).get('name','')
    @property
    def player_count(self):
        protocol=self.raw_data.get('protocol_info',[])
        return len(protocol) if len(protocol)>0 else ''
    @property
    def goalkeeper_count(self):
        """returns amount of players tagged with player_info.card.ref_position.id=3"""
        count=0
        goalkeeper_position_id=3
        for player in self.raw_data.get('protocol_info',[]):
            position_id=player.get('player_info',{}).get('card',{}).get('ref_position',{}).get('id')
            if position_id==goalkeeper_position_id: 
                count=count+1
        return count
    @property
    def duration(self):
        """returns sum() of durations of all exercises"""
        return sum([exercise.duration for exercise in self.exercises])


    @property
    def exercises(self) -> list[TrainingExerciseInfo]:
        if self._exercises is None:
            self._exercises= [TrainingExerciseInfo(data) for data in self.raw_data.get('exercises_info')]
        return self._exercises

    @from_field('trainer_name',default=EMPTY_TRAINER_NAME_REPLACEMENT,warn_if_none='trainer name not found')
    def trainer_name(self):
        pass
    
    def __str__(self):
        return f'training[id={self.id}]'