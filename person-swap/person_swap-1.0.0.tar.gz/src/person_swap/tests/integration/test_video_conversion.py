from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from dash.admin import ConvertedFileAdmin
from dash.models import File, FileType
from dash.models.file import ConvertedFile
from dash.models.model import TorchModel, ModelFile, TorchModelFileType


class ImageConversionTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.torch_model = TorchModel.objects.create(
            title="Image file",
            type=FileType.IMAGE
        )
        model_conversion_files = {
            TorchModelFileType.MAIN_MODEL: './test_files/arcface_checkpoint.tar',
            TorchModelFileType.MASK_DETECTOR: './test_files/mask_detection.pth',
            TorchModelFileType.DETECTOR: './test_files/detection.onnx',
            TorchModelFileType.GENERATOR: './test_files/latest_net_G.pth'
        }
        for key, path in model_conversion_files.items():
            model_file = ModelFile.objects.create(
                title=key.value,
                type=FileType.IMAGE,
                model_file_type=key
            )
            model_file.file_object.name = path
            model_file.save()
            self.torch_model.model.model_files.add(model_file)

        self.torch_model.save()

    #
    # def test_video_conversion_WITH_raw_files_EXPECT_new_file(self):
    #     source_img = cv2.imread('./media/test_files/specific3.png')
    #     target_img = cv2.imread('./media/test_files/face1.jpeg')
    #
    #     swaped_image = self.torch_model.torchmodel.process_for_video(
    #         target_img,
    #         source_img,
    #         self.torch_model.conversion_properties
    #     )
    #     status, _ = cv2.imencode(".png", swaped_image)
    #     self.assertTrue(status)
    #     self.assertEqual((279, 260, 3), swaped_image.shape)

    def test_video_conversion_WITH_existing_files_EXPECT_new_file(self):
        file = ConvertedFile.objects.create(
            title="New Video file",
            selected_model=self.torch_model,
            target=File.objects.create(title="Video file", type=FileType.VIDEO),
            source=File.objects.create(title="Image file", type=FileType.IMAGE),
            type=FileType.VIDEO
        )

        file.target.file_object.name = './test_files/video.mp4'
        file.source.file_object.name = './test_files/specific3.png'
        dummy_user = User.objects.create(username='test_user')

        file_pk, message = ConvertedFileAdmin.convert_file(file, dummy_user)
        self.assertIsNone(message)

        created_file = ConvertedFile.objects.get(id=file_pk)
        self.assertIsNotNone(created_file.created.file_object)
