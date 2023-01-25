from functools import partial
from typing import Dict, Tuple, List

import cv2
import numpy as np


def _add_random_noise(img: np.ndarray):
    n = 40
    i = np.random.randint(0, 64, size=n)
    j = np.random.randint(0, 64, size=n)
    c = np.random.randint(0, 3, size=n)
    values = np.random.randint(0, 255, size=n)
    img[i, j, c] = values


def _generate_camera_blocked_image():
    img = np.zeros((64, 64, 3), dtype=np.uint8)
    # randomly add some noise
    _add_random_noise(img)
    return img, {'camera_blocked': True}


def _generate_door_open_image():
    img = np.ones((64, 64, 3), dtype=np.uint8) * 255
    # randomly add some noise
    _add_random_noise(img)
    return img, {'camera_blocked': False, 'door_open': True, 'person_present': False}


def _generate_door_closed_image(door_locked):
    img, res = _generate_door_open_image()

    offsets = np.random.randint(-10, 10, size=4)
    x1, y1 = int(10 + offsets[0]), int(10 + offsets[1])
    x2, y2 = int(50 + offsets[2]), int(50 + offsets[2])

    img = cv2.rectangle(img, (x1, y1), (x2, y2), color=(139, 69, 19), thickness=-1)

    if door_locked:
        lock_start = x1, int((y1 + y2) / 2)
        lock_end = lock_start[0] + 10, lock_start[1] + 10
        img = cv2.rectangle(img, lock_start, lock_end, color=(0, 0, 255), thickness=-1)

    res['door_locked'] = door_locked
    res['camera_blocked'] = False
    res['door_open'] = False
    return img, res


def _select_facial_characteristics():
    choices = [
        [(255, 0, 255), (0, 2)],
        [(0, 255, 255), (1, 2)],
        [(255, 255, 0), (0, 1)],
        [(0, 0, 0), ()],
        [(255, 0, 0), (0,)],
        [(0, 255, 0), (1,)],
        [(0, 0, 255), (2,)],
    ]
    choice = np.random.randint(0, len(choices), size=1)[0]
    return choices[choice]


def _draw_person(img, res, shirt_type='blue'):
    head_radius = 6
    offsets = np.random.randint(-4, 4, size=4)
    head = int(30 + offsets[0]), int(10 + offsets[1])

    color, face_characteristics = _select_facial_characteristics()
    img = cv2.circle(img, head, head_radius, color=color, thickness=-1)

    res['person_present'] = True
    res['person_regression.face_regression.face_x1'] = head[0] - head_radius
    res['person_regression.face_regression.face_y1'] = head[1] - head_radius
    res['person_regression.face_regression.face_w'] = 2 * head_radius
    res['person_regression.face_regression.face_h'] = 2 * head_radius
    res['person_regression.face_regression.facial_characteristics'] = ','.join(map(str, face_characteristics))

    offsets = np.random.randint(-2, 2, size=4)
    d = head_radius * 2
    rec_start = head[0] - head_radius + offsets[0], head[1] + head_radius + offsets[1]
    rec_end = rec_start[0] + d + offsets[2], rec_start[1] + 30 + offsets[3]

    if shirt_type == 'blue':
        color = (0, 0, 255)
        shirt_label = 0
    elif shirt_type == 'red':
        color = (255, 0, 0)
        shirt_label = 1
    elif shirt_type == 'yellow':
        color = (255, 255, 0)
        shirt_label = 2
    elif shirt_type == 'cyan':
        color = (0, 255, 255)
        shirt_label = 3
    elif shirt_type == 'magenta':
        color = (255, 0, 255)
        shirt_label = 4
    elif shirt_type == 'green':
        color = (0, 255, 0)
        shirt_label = 5
    else:
        # black
        color = (0, 0, 0)
        shirt_label = 6

    cv2.rectangle(img, rec_start, rec_end, color=color, thickness=-1)

    res['person_regression.body_regression.body_x1'] = rec_start[0]
    res['person_regression.body_regression.body_y1'] = rec_start[1]
    res['person_regression.body_regression.body_w'] = rec_end[0] - rec_start[0]
    res['person_regression.body_regression.body_h'] = rec_end[1] - rec_start[1]
    res['person_regression.body_regression.shirt_type'] = shirt_label

    return img, res


def _generate_image_with_person(shirt_type='blue'):
    img, res = _generate_door_open_image()
    img, res = _draw_person(img, res, shirt_type)
    return img, res


def _generate_sample() -> Tuple[np.ndarray, Dict]:
    generators = [_generate_camera_blocked_image,
                  _generate_door_open_image,
                  partial(_generate_door_closed_image, door_locked=True),
                  partial(_generate_door_closed_image, door_locked=False),
                  partial(_generate_image_with_person, shirt_type='blue'),
                  partial(_generate_image_with_person, shirt_type='red'),
                  partial(_generate_image_with_person, shirt_type='yellow'),
                  partial(_generate_image_with_person, shirt_type='cyan'),
                  partial(_generate_image_with_person, shirt_type='magenta'),
                  partial(_generate_image_with_person, shirt_type='green'),
                  partial(_generate_image_with_person, shirt_type='black')
                  ]
    choice = np.random.randint(0, len(generators), size=1)[0]
    return generators[choice]()


def create_dataset(n: int) -> Tuple[List[np.ndarray], List[Dict]]:
    imgs = []
    rows = []
    for i in range(n):
        img, row = _generate_sample()
        imgs.append(img)
        rows.append(row)
    return imgs, rows
