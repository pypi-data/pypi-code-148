from nf_presentation.renderers.base_renderer import BaseRenderer
from nf_presentation.data_classes import SingleExerciseInfo, TrainingInfo
from nf_presentation.builders import ParagraphBuilder,SlideBuilder

from nf_presentation._settings import compact_layout as current_layout
import nf_presentation.settings as base_settings
from nf_presentation.logger import logger
from nf_presentation import assets

_default_description="""Описание:



Тренерские акценты:


"""

class ExerciseRenderOptions:
    _media_fields=['video_1','video_2','animation_1','animation_2']
    _scheme_priority=['scheme_1','scheme_2']
    def __init__(self,raw_data:dict):
        self.raw_data:dict=raw_data
        self.check()
    @property
    def media_fields_to_render(self) -> list[str]:
        """returns a list of edia fields should be rendered to a pptx
        ['video_2','animation_1']"""
        return [field for field in self._media_fields if self.raw_data.get(field)]  # if checked as True
    @property
    def schemes_to_render(self):
        return [scheme_name for scheme_name in self._scheme_priority if self.raw_data.get(scheme_name)]
    def check(self):
        #check if video or animation will be added to pptx
        if not any([self.raw_data.get(field) for field in self._media_fields]):
            logger.warn('(Render Options) no player links are marked to be added to pptx')
        if not any(self.schemes_to_render):
            logger.warn('(Render Options) no scheme links are marked to be added to pptx')


def create_links_paragraph(exercise:SingleExerciseInfo,render_options:ExerciseRenderOptions) -> ParagraphBuilder:
            #add links
        links_added=False
        #links_table=slide.create_table().at(current_layout.LINKS_TABLE_POSITION).with_width(current_layout.LEFT_TABLE_WIDTH)
        

        ## TODO extract as media links
        pb=ParagraphBuilder()
        #link_position=current_layout.LINKS_AREA
        video_counter=0
        animation_counter=0
        for media_field in render_options.media_fields_to_render:
            media=exercise.get_media(media_field)
            if media is None or not media.exist:
                logger.info(f'[{exercise.title}]requested "{media_field}" is not in the current exercise. skipping')
                continue

            player_url=exercise.get_media(media_field).nftv_player
            is_animation='animation' in media_field
            if is_animation:
                animation_counter=animation_counter+1
            else:
                video_counter=video_counter+1
            
            pb.append_link(
                link_text=f"Анимация {animation_counter}" if is_animation else f"Видео {video_counter}",
                href=player_url)
            pb.append_text(' ')

            links_added=True

        if not links_added:
            logger.warn(f'[{exercise.title}] No links added to slide')
        return pb

def prepare_training_rows(training:TrainingInfo) -> list[tuple]:
    """returns a list for creating left table, mostly for feeding to create_left_table"""
    rows=[]

    #objectives
    if training.tasks is not None:
        tasks=training.tasks
    else:
        logger.warn(f'{training}: using default tasks on render {current_layout.DEFAULT_TASKS}')
        tasks=current_layout.DEFAULT_TASKS

    for task in tasks:
        rows.append((task,))

    rows.append(()) #empty row

    #block_1
    rows.append(('ДАТА',training.date))
    rows.append(('ВРЕМЯ',training.time))
    rows.append(('ТРЕНЕР',training.trainer_name))
    rows.append(('ТРЕНЕР 2',''))
    rows.append(('ТРЕНЕР ВРАТАРЕЙ',''))
    rows.append(('КОМАНДА',training.team_name))
    rows.append(('КОЛИЧЕСТВО ИГРОКОВ',training.player_count))
    rows.append(('ВРАТАРИ',training.goalkeeper_count))
    rows.append(('ПРОДОЛЖИТЕЛЬНОСТЬ',training.duration))

    rows.append(()) #empty row

    rows.append(('ВОЗРАСТ',''))
    rows.append(('МЕСТО ЗАНЯТИЯ',''))
    rows.append(('ОРГАНИЗАЦИЯ',''))

    rows.append(()) #empty row

    rows.append(('РАЗМЕР ПОЛЯ',training.field_size))
    rows.append(('ТИПА НАГРУЗКИ',training.load))
    rows.append(('КЛЮЧЕВЫЕ СЛОВА',training.keywords_1))
    rows.append(('КЛЮЧЕВЫЕ СЛОВА',training.keywords_2))

    return rows

def prepare_exercise_rows(exercise:SingleExerciseInfo,training:TrainingInfo,render_options:SingleExerciseInfo) -> list[tuple]:
    """returns a list for creating left table, mostly for feeding to create_left_table"""
    rows=[]

    duration=getattr(exercise,'duration','')

    #titles
    if training is not None:
        if training.tasks is not None:
            tasks=training.tasks
        else:
            logger.warn(f'{training}: using default tasks on render {current_layout.DEFAULT_TASKS}')
            tasks=current_layout.DEFAULT_TASKS

        for task in tasks:
            rows.append((task,))
    rows.append((exercise.title,))

    rows.append(()) #empty row

    #main block
    rows.append(('ЭТАП ПОДГОТОВКИ',''))
    rows.append(('ЧАСТЬ ТРЕНИРОВКИ',''))
    rows.append(('ТИП УПРАЖНЕНИЯ',''))
    rows.append(('ПРОДОЛЖИТЕЛЬНОСТЬ',duration))
    rows.append(('КОЛИЧЕСТВО ИГРОКОВ',''))  # кстати, вот это откуда брать из тренировки или из упражнения?
    rows.append(('ОРГАНИЗАЦИЯ',''))
    rows.append(('ПРОСТРАНСТВО',''))
    rows.append(('ДОЗИРОВКА',''))
    rows.append(('ПУЛЬС',''))
    rows.append(('КАСАНИЕ МЯЧА',''))
    rows.append(('НЕЙТРАЛЬНЫЕ',''))
    rows.append(('РАСПОЛОЖЕНИЕ ТРЕНЕРА',''))
    rows.append(('ВЫЯВЛЕНИЕ ПОБЕДИТЕЛЯ',''))

    rows.append(()) #empty row

    #links
    links=create_links_paragraph(exercise=exercise,render_options=render_options)
    rows.append(('ССЫЛКИ',links))

    return rows


def create_left_table(slide:SlideBuilder,rows:list[tuple],capitalize=False,title=''):
    if capitalize:
        capitalized_rows=[]
        for row in rows:
            capitalized_rows.append((text.upper() for text in row))
        rows=capitalized_rows

    left_table=slide.create_table().at(current_layout.LEFT_TABLE_POSITION).with_width(current_layout.LEFT_TABLE_WIDTH)
    if title:
        left_table.append_row(title)
        left_table.append_empty_row()
  
    for row in rows:
       left_table.append_row(*row) 
    
    return left_table

def create_title(slide:SlideBuilder,title:str):
    title=slide.create_title(title).at(current_layout.TITLE_POSITION).with_size(current_layout.TITLE_SIZE)
    title.with_foreground(current_layout.TITLE_FOREGROUND).with_background(current_layout.TITLE_BACKGROUND)
    return title


class CompactRenderer(BaseRenderer):
    def __init__(self):
        super().__init__(ratio=base_settings.PRESENTATION_RATIO)
        #self.render_options : ExerciseRenderOptions = render_options


    def add_title_slide(self,name:str):

        text=f'Итоговая работа по теме: Техническая тренировка \nАвтор: {name}'
        slide=self.presentation_builder.create_slide()

        rfs_logo=assets.get_rfs_logo()
        self._open_streams.append(rfs_logo)
        
        slide.create_image(rfs_logo).at(base_settings.LOGO_POSITION).set_size(base_settings.LOGO_WIDTH,None)
        slide.create_text(text).at(base_settings.NAME_POSITION)

    def add_training_slide(self, training:TrainingInfo):
        """
        adds a new slide to current presentation, with training overview

        Arguments:
            training: 
                a training data to be added to slide, like tasks, loads and players
            """
        slide=self.presentation_builder.create_slide()

        #creating title
        if training.main_objective is not None:
            title=training.main_objective
        else:
            logger.warn(f'{training} cant get main objective, using default "{current_layout.DEFAULT_MAIN_OBJECTIVE}"')
            title=current_layout.DEFAULT_MAIN_OBJECTIVE

        create_title(slide,title=title)

        #left table
        left_rows=prepare_training_rows(training=training)

        create_left_table(
                slide=slide,
                rows=left_rows,
                title=None,
                capitalize=False)

        #schemes

    def add_exercise_slide(self,
            exercise:SingleExerciseInfo,
            render_options : ExerciseRenderOptions = None,
            training:TrainingInfo = None):
        """
        adds a new slide to current presentation, with exercise schemes and videos and othe info

        Arguments:
            exercise: SingeExerciseInfo
                a exercise to render as a slide
            [Optional] render_options: ExerciseRenderOptions
                a class contating options like to akk scheme1 or not, to add links or not
                how the exercise slide would look like
            [Optional] training: 
                a training data to be added to slide, like tasks of training
            """

        if render_options is None:
            render_options=ExerciseRenderOptions(current_layout.DEFAULT_EXERCISE_RENDER_OPTIONS)
        slide=self.presentation_builder.create_slide()

        #creating title
        title=create_title(slide,title=current_layout.DEFAULT_SLIDE_TITLE)

        #decription_text=HTMLRenderer().render(exercise.description)
        description_text=_default_description
        right_table=slide.create_table().at(current_layout.RIGHT_TABLE_POSITION).with_width(current_layout.RIGHT_TABLE_WIDTH)
        right_table.append_row(description_text)
        # mayble here add default params iter
        
        left_rows=prepare_exercise_rows(exercise=exercise,training=training,render_options=render_options)

        create_left_table(
            slide=slide,
            rows=left_rows,
            capitalize=False,
            title=None
            )

        #schemes
        scheme_added=False
           
        for scheme_name in render_options.schemes_to_render:
            scheme=exercise.get_scheme_by_name(scheme_name)
            if not scheme:
                logger.warn(f'Cant add scheme "{scheme}" to slide, because it is not in the exercise data')
                continue      

            image_stream=scheme.to_stream()
            if not image_stream:
                logger.warn(f'cant add scheme "{scheme}" to slide, because its stream is None')
                continue

            self._open_streams.append(image_stream)
            slide.create_image(image_stream).at(current_layout.SCHEME_POSITION).set_size(current_layout.SCHEME_WIDTH,None)

            scheme_added=True
            break
        if not scheme_added:
            logger.error('No scheme added to slide. ')
            #TODO image fallback







