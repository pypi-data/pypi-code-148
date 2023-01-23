import logging
import random
import string
from argparse import Namespace
from datetime import datetime

import cv2
import numpy as np
import paddle
import torch
import torch.nn.functional as F
from PIL import Image
from django.db import models
from torchvision import transforms

from dash.convertion.face_utils.face_detect_crop import Face_detect_crop
from dash.convertion.face_utils.nn_modules import BiSeNet, SoftErosion, SpecificNorm
from .abstract_file import AbstractFile, FileType
from ..convertion.face_utils.models.fs_model import FaceSwapNN
from ..convertion.voice_utils.speech_to_text import Speech2Text
from ..convertion.voice_utils.voice_cloning import voice_cloning
from ..custom_utils.conversion_exception import ConversionError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TorchModelFileType(models.TextChoices):
    MAIN_MODEL = "main_model"
    GENERATOR = "generator"
    DETECTOR = "detector"
    MASK_DETECTOR = "mask_detector"

    """    SUCCEDED fastspeech2_ljspeech pwgan_ljspeech
SUCCEDED fastspeech2_ljspeech pwgan_vctk
SUCCEDED fastspeech2_ljspeech hifigan_ljspeech
SUCCEDED fastspeech2_ljspeech hifigan_vctk
SUCCEDED tacotron2_ljspeech pwgan_ljspeech
SUCCEDED tacotron2_ljspeech pwgan_vctk
SUCCEDED tacotron2_ljspeech hifigan_ljspeech
SUCCEDED tacotron2_ljspeech hifigan_vctk
SUCCEDED fastspeech2_vctk pwgan_ljspeech
SUCCEDED fastspeech2_vctk pwgan_vctk
SUCCEDED fastspeech2_vctk hifigan_ljspeech
SUCCEDED fastspeech2_vctk hifigan_vctk"""


class VocoderType(models.TextChoices):
    PWGAN_LJSPEECH = "pwgan_ljspeech"
    PWGAN_VCTK = "pwgan_vctk"
    HIFIGAN_LJSPEECH = "hifigan_ljspeech"
    HIFIGAN_VCTK = "hifigan_vctk"


class AcousticModelType(models.TextChoices):
    FASTSPEECH2_VCTK = "fastspeech2_vctk"
    TACOTRON2_LJSPEECH = "tacotron2_ljspeech"
    FASTSPEECH2_LJSPEECH = "fastspeech2_ljspeech"


class ModelFile(AbstractFile):
    file_object = models.FileField(upload_to="models")

    model_file_type = models.CharField(
        max_length=15,
        choices=TorchModelFileType.choices,
        default=TorchModelFileType.MAIN_MODEL,
    )


class Model(AbstractFile):
    model_files = models.ManyToManyField(ModelFile)

    description = models.TextField(null=True, blank=True)
    conversion_properties = models.JSONField(default=dict(), null=True, blank=True)

    class Meta:
        verbose_name_plural = "Models"

    def __str__(self):
        return f'{(self.title or (self._meta.object_name + str(self.pk)))} ({self.type})'

    def save(self, *args, **kwargs):
        super(Model, self).save(*args, **kwargs)

    def build(self, conversion_properties):
        raise NotImplementedError

    def process(self, input_path, output_path, conversion_properties):
        raise NotImplementedError


class TorchModel(Model):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = FileType.IMAGE

    class Meta:
        verbose_name = 'Face Swap Model'
        verbose_name_plural = 'Face Swap Models'

    def save(self, *args, **kwargs):

        self.conversion_properties = {
            'use_mask': True,
            'crop_size': 224,
            'gpu_ids': -1,
            'id_thres': 0.03,
            'which_epoch': 'latest'
        }

        super().save(*args, **kwargs)
        choices = [item[0] for item in TorchModelFileType.choices]

        for file in self.model_files.all():
            self.conversion_properties[file.model_file_type] = file.file_object.path
            choices.remove(file.model_file_type)

        if choices:
            raise Exception(f"All model files should be provided. Missing {choices}")
        super().save(*args, **kwargs)

        if self.model_files.count() > 0:
            self.__validate()
        else:
            logger.warning("Model validation was skipped")

    def process(self, input_path, output_path, conversion_properties):
        try:
            img_a_whole = cv2.imread(input_path)
            if img_a_whole is None:
                raise ConversionError(f'Image does not exist in {input_path}')

            img_b_whole = cv2.imread(output_path)
            if img_b_whole is None:
                raise ConversionError(f'Image does not exist in {output_path}')
            return self.convert(img_a_whole, img_b_whole, conversion_properties, specific_person_whole=None)
        except Exception as ex:
            logger.error(ex)
            # TODO fix
            raise ex
            # raise ConversionError(ex)

    def process_for_video(self, source_im, target_im, conversion_properties):
        try:
            return self.convert(source_im, target_im, conversion_properties)
        except Exception as ex:
            logger.error(ex)
            raise ConversionError(ex)

    def convert(self, img_a_whole, img_b_whole, conversion_properties, specific_person_whole=None):
        # Prepare transformation class
        transformer_Arcface = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        opt = Namespace(**conversion_properties)
        specific_person_whole = specific_person_whole or img_b_whole
        opt.crop_size = int(opt.crop_size)

        face_swap_model = FaceSwapNN()
        face_swap_model.initialize(opt)
        face_swap_model.eval()
        mse = torch.nn.MSELoss()  # .cuda()

        spNorm = SpecificNorm()

        face_crop = Face_detect_crop(opt.detector, det_thresh=0.6, det_size=(640, 640))

        img_a_align_crop, _ = face_crop.get_aligned_image(img_a_whole, opt.crop_size)
        if img_a_align_crop is None:
            raise ConversionError(f'Face was not detected in target image')
        img_a_align_crop_pil = Image.fromarray(cv2.cvtColor(img_a_align_crop[0], cv2.COLOR_BGR2RGB))
        img_a = transformer_Arcface(img_a_align_crop_pil)
        img_id = img_a.view(-1, img_a.shape[0], img_a.shape[1], img_a.shape[2])

        # create latent id
        img_id_downsample = F.interpolate(img_id, size=(112, 112))
        latend_id = face_swap_model.recognition_net(img_id_downsample)
        latend_id = F.normalize(latend_id, p=2, dim=1)

        # The specific person to be swapped
        specific_person_align_crop, _ = face_crop.get_aligned_image(specific_person_whole, opt.crop_size)
        if specific_person_align_crop is None:
            raise ConversionError(f'Face was not detected in specific image')
        specific_person_align_crop_pil = Image.fromarray(cv2.cvtColor(specific_person_align_crop[0], cv2.COLOR_BGR2RGB))
        specific_person = transformer_Arcface(specific_person_align_crop_pil)
        specific_person = specific_person.view(-1, specific_person.shape[0], specific_person.shape[1],
                                               specific_person.shape[2])

        # create latent id
        specific_person_downsample = F.interpolate(specific_person, size=(112, 112))
        specific_person_id_nonorm = face_swap_model.recognition_net(specific_person_downsample)

        ############## Forward Pass ######################

        # pic_b = opt.pic_output_path

        if img_a_whole is img_b_whole:
            raise ConversionError('Target and source image could not be the same')

        img_b_align_crop_list, b_mat_list = face_crop.get_aligned_image(img_b_whole, opt.crop_size)
        specific_person_align_crop, _ = face_crop.get_aligned_image(specific_person_whole, opt.crop_size)
        if specific_person_align_crop is None:
            raise ConversionError(f'Face was not detected in source')

        id_compare_values = []
        b_align_crop_tenor_list = []
        for b_align_crop in img_b_align_crop_list:
            tensor = torch.from_numpy(cv2.cvtColor(b_align_crop, cv2.COLOR_BGR2RGB))
            img = tensor.transpose(0, 1).transpose(0, 2).contiguous()
            b_align_crop_tenor = img.float().div(255)[None, ...]

            b_align_crop_tenor_arcnorm = spNorm(b_align_crop_tenor)
            b_align_crop_tenor_arcnorm_downsample = F.interpolate(b_align_crop_tenor_arcnorm, size=(112, 112))
            b_align_crop_id_nonorm = face_swap_model.recognition_net(b_align_crop_tenor_arcnorm_downsample)

            id_compare_values.append(mse(b_align_crop_id_nonorm, specific_person_id_nonorm).detach().cpu().numpy())
            b_align_crop_tenor_list.append(b_align_crop_tenor)

        id_compare_values_array = np.array(id_compare_values)
        min_index = np.argmin(id_compare_values_array)
        min_value = id_compare_values_array[min_index]

        if opt.use_mask:
            n_classes = 19
            net = BiSeNet(n_classes=n_classes)
            net.load_state_dict(
                torch.load(opt.mask_detector,
                           map_location=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')))
            net.eval()
        else:
            net = None

        if min_value < opt.id_thres:

            swap_result = face_swap_model(b_align_crop_tenor_list[min_index], latend_id)[0]

            image = self.generate_new_image(
                [b_align_crop_tenor_list[min_index]], [swap_result], [b_mat_list[min_index]],
                opt.crop_size, img_b_whole, pasring_model=net, use_mask=opt.use_mask, norm=spNorm
            )

            # logger.infor('************ Done ! ************')
            return image

        else:
            logger.warning('The person you specified is not found')

    def generate_new_image(self, b_align_crop_tenor_list, swaped_imgs, mats, crop_size, oriimg, pasring_model=None,
                           norm=None,
                           use_mask=False):
        NO_NECK = False

        target_image_list = []
        img_mask_list = []
        smooth_mask = SoftErosion(kernel_size=17, threshold=0.9, iterations=7)  # .cuda()

        for swaped_img, mat, source_img in zip(swaped_imgs, mats, b_align_crop_tenor_list):
            swaped_img = swaped_img.cpu().detach().numpy().transpose((1, 2, 0))
            img_white = np.full((crop_size, crop_size), 255, dtype=float)

            # inverse the Affine transformation matrix
            mat_rev = np.zeros([2, 3])
            div1 = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
            mat_rev[0][0] = mat[1][1] / div1
            mat_rev[0][1] = -mat[0][1] / div1
            mat_rev[0][2] = -(mat[0][2] * mat[1][1] - mat[0][1] * mat[1][2]) / div1
            div2 = mat[0][1] * mat[1][0] - mat[0][0] * mat[1][1]
            mat_rev[1][0] = mat[1][0] / div2
            mat_rev[1][1] = -mat[0][0] / div2
            mat_rev[1][2] = -(mat[0][2] * mat[1][0] - mat[0][0] * mat[1][2]) / div2

            orisize = (oriimg.shape[1], oriimg.shape[0])
            if use_mask:
                source_img_norm = norm(source_img)
                source_img_512 = F.interpolate(source_img_norm, size=(512, 512))
                out = pasring_model(source_img_512)[0]
                parsing = out.squeeze(0).detach().cpu().numpy().argmax(0)
                vis_parsing_anno = parsing.copy().astype(np.uint8)
                parse = vis_parsing_anno

                face_part_ids = [1, 2, 3, 4, 5, 6, 10, 12, 13] if NO_NECK else [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14]
                mouth_id = 11
                face_map = np.zeros([parse.shape[0], parse.shape[1]])
                mouth_map = np.zeros([parse.shape[0], parse.shape[1]])

                for valid_id in face_part_ids:
                    valid_index = np.where(parse == valid_id)
                    face_map[valid_index] = 255
                valid_index = np.where(parse == mouth_id)
                mouth_map[valid_index] = 255
                tgt_mask = np.stack([face_map, mouth_map], axis=2)

                if tgt_mask.sum() >= 5000:
                    # face_mask_tensor = tgt_mask[...,0] + tgt_mask[...,1]
                    target_mask = cv2.resize(tgt_mask, (crop_size, crop_size))
                    # logger.error(source_img)

                    target = source_img[0].cpu().detach().numpy().transpose((1, 2, 0))
                    mask_tensor = torch.from_numpy(target_mask.copy().transpose((2, 0, 1))).float().mul_(
                        1 / 255.0)  # .cuda()
                    face_mask_tensor = mask_tensor[0] + mask_tensor[1]

                    soft_face_mask_tensor, _ = smooth_mask(face_mask_tensor.unsqueeze_(0).unsqueeze_(0))
                    soft_face_mask_tensor.squeeze_()

                    soft_face_mask = soft_face_mask_tensor.cpu().numpy()
                    soft_face_mask = soft_face_mask[:, :, np.newaxis]

                    target_image_parsing = swaped_img * soft_face_mask + target * (1 - soft_face_mask)
                    target_image_parsing = target_image_parsing[:, :, ::-1]  # .astype(np.uint8)
                    target_image = cv2.warpAffine(target_image_parsing, mat_rev, orisize)
                    # target_image_parsing = cv2.warpAffine(swaped_img, mat_rev, orisize)
                else:
                    target_image = cv2.warpAffine(swaped_img, mat_rev, orisize)[..., ::-1]
            else:
                target_image = cv2.warpAffine(swaped_img, mat_rev, orisize)
            # source_image   = cv2.warpAffine(source_img, mat_rev, orisize)

            img_white = cv2.warpAffine(img_white, mat_rev, orisize)

            img_white[img_white > 20] = 255

            img_mask = img_white

            kernel = np.ones((40, 40), np.uint8)
            img_mask = cv2.erode(img_mask, kernel, iterations=1)
            kernel_size = (20, 20)
            blur_size = tuple(2 * i + 1 for i in kernel_size)
            img_mask = cv2.GaussianBlur(img_mask, blur_size, 0)

            img_mask /= 255

            img_mask = np.reshape(img_mask, [img_mask.shape[0], img_mask.shape[1], 1])
            if use_mask:
                target_image = np.array(target_image, dtype=np.float) * 255
            else:
                target_image = np.array(target_image, dtype=np.float)[..., ::-1] * 255

            img_mask_list.append(img_mask)
            target_image_list.append(target_image)

        # target_image /= 255
        # target_image = 0
        img = np.array(oriimg, dtype=np.float)
        for img_mask, target_image in zip(img_mask_list, target_image_list):
            img = img_mask * target_image + (1 - img_mask) * img

        final_img = img.astype(np.uint8)

        return final_img

    def __validate(self):
        try:

            image_array = self.process("./media/test_files/specific1.png", "./media/test_files/specific3.png",
                                       self.conversion_properties)
            # logger.error(image_array)
            assert image_array is not None
            return None
        except ConversionError as ex:
            from django.core.exceptions import ValidationError
            opts = self._meta
            field = opts.get_field('model_files')
            # TODO fix valiation

            # raise ValidationError(
            #     message=field.error_messages['invalid_choice'],
            #     code="model_validation",
            #     params={
            #         "model": self,
            #         "model_name": opts.verbose_name,
            #         # "lookup_type": lookup_type,
            #         "field": "model_files",
            #         "field_label": field.verbose_name,
            #     },
            # )


class VoiceSwapModel(Model):
    vocoder = models.CharField(
        max_length=30,
        choices=VocoderType.choices
    )

    acoustic_model = models.CharField(
        max_length=30,
        choices=AcousticModelType.choices
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = FileType.MP3

    def build(self, conversion_properties):
        raise NotImplementedError

    def process(self, source, target, conversion_properties):
        conversion_properties.text = Speech2Text()(
            audio_file=source,
            device=paddle.get_device(),
        )

        if conversion_properties.ngpu == 0:
            paddle.set_device("cpu")
        elif conversion_properties.ngpu > 0:
            paddle.set_device("gpu")
        else:
            raise Exception("ngpu should >= 0 !")

        mp3_path = f'{self.title}.wav' if self.title else f'{datetime.now().strftime("%d%m%Y") + "".join(random.choices(string.ascii_lowercase, k=10))}.wav'

        conversion_properties.input_path = target
        conversion_properties.output_path = 'media/files/' + mp3_path
        conversion_properties.am = self.acoustic_model
        conversion_properties.voc = self.vocoder

        voice_cloning(conversion_properties)
        return mp3_path


class VideoSwapModel(Model):
    voice_model = models.ForeignKey(VoiceSwapModel, on_delete=models.SET_NULL, null=True)
    face_model = models.ForeignKey(TorchModel, on_delete=models.SET_NULL, null=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = FileType.VIDEO

    def build(self, conversion_properties):
        raise NotImplementedError

    def process(self, input_path, output_path, conversion_properties):
        raise NotImplementedError
