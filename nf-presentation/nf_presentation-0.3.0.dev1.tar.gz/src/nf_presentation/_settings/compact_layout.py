"""A module contataining constants for ComractRenderer class

Thic type of layout renders a single exercise to a single slide list"""

CAPITALIZE_ADDITIONAL_DATA=True  # capitalizes captions in left table

TITLE_POSITION=(0.5,0.5)
TITLE_SIZE=(33,1)
TITLE_BACKGROUND=(46,117,182)
TITLE_FOREGROUND=(255,255,255)

SCHEME_POSITION=(12.0,2.0)
SCHEME_HEIGHT=8.5 # not used atm
SCHEME_WIDTH=12.5
FALLBACK_SCHEME='fallback_scheme.png'

LEFT_TABLE_POSITION=(0.5,2.0)
LEFT_TABLE_WIDTH=10.5

RIGHT_TABLE_POSITION=(12.0,10.5)
RIGHT_TABLE_WIDTH=21.5


LINKS_TABLE_POSITION=(0.5,13.5)

# LINKS_TITLE_POSITION=(0.5,13.5)
# LINKS_AREA=(2.5,13.5)
# LINKS_IMAGE_SIZE=(1,1)
# LINKS_VIDEO_ICON_FILENAME='movie_google_icon.svg'
# LINKS_ANIMATION_ICON_FILENAME='animation_google_icon.svg'


#PARAMS


DEFAULT_EXERCISE_RENDER_OPTIONS={
    'scheme_1':True,
    'scheme_2':True,
    'video_1':True,
    'video_2':True,
    'animation_1':True,
    'animation_2':True
}

EXERCISE_ADDITIONAL_PARAMS=[
        'Этап подготовки',
        'Часть тренировки',
        'Тип упражнения',
        'Продолжительность',
        'Количество игроков',
        'Организация',
        'Пространство',
        'Дозировка',
        'Пульс',
        'Касание мяча',
        'Нейтральные',
        'Расположение тренера',
        'Выявление победителя'
    ]



TRAINING_SLIDE_TITLE='Цели тренировочного занятия'
TRAINING_ADDITIONAL_PARAMS=[
    [
        'дата',
        "время",
        "тренер",
        "тренер 2",
        "тренер вратарей",
        "команда",
        "количество игроков",
        "вратари",
        "продолжительность"
    ],
    [
        'возраст',
        "место занятия",
        "организация"
    ],
    [
        "размер поля",
        "тип нагрузки",
        "ключевые слова",
        "ключевые слова"
    ]
]
