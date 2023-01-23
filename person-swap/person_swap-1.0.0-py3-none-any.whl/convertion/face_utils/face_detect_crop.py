from __future__ import division

import collections

import cv2
import numpy as np
from insightface.model_zoo import model_zoo
from insightface.utils import face_align

__all__ = ['Face_detect_crop', 'Face']

Face = collections.namedtuple('Face', [
    'bbox', 'kps', 'det_score', 'embedding', 'gender', 'age',
    'embedding_norm', 'normed_embedding',
    'landmark'
])

Face.__new__.__defaults__ = (None,) * len(Face._fields)


class Face_detect_crop:
    def __init__(self, detection_path, multi=False, det_thresh=0.5, det_size=(640, 640)):
        self.multi = multi
        self.det_model = model_zoo.get_model(detection_path)
        self.det_thresh = det_thresh
        self.det_model.prepare(0, input_size=det_size)

    def get_aligned_image(self, img, crop_size, max_num=1):
        faces, landmarks = self.det_model.detect(img, max_num=max_num, metric='default')
        if faces is None:
            return None, None

        if self.multi:
            # TODO cia isrinkti kuri veida keisti ar net lesiti keist tik viena
            align_img_list = []
            M_list = []
            for i in range(faces.shape[0]):
                kps = None
                if landmarks is not None:
                    kps = landmarks[i]
                min_M, _ = face_align.estimate_norm(kps, crop_size, mode=None)
                align_img = cv2.warpAffine(img, min_M, (crop_size, crop_size), borderValue=0.0)
                align_img_list.append(align_img)
                M_list.append(min_M)

            return align_img_list, M_list
        else:
            det_score = faces[..., 4]
            best_index = np.argmax(det_score)

            kps = None
            if landmarks is not None:
                kps = landmarks[best_index]
            min_M, _ = face_align.estimate_norm(kps, crop_size, mode=None)
            align_img = cv2.warpAffine(img, min_M, (crop_size, crop_size), borderValue=0.0)

            return [align_img], [min_M]
