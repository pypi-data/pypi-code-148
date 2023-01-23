import cv2
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from dash.models import FileType
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

    # def test_file_conversion_WITH_same_files_EXPECT_error_message(self):
    #     with self.assertRaises(Exception) as context:
    #
    #         self.torch_model.torchmodel.process(
    #             './media/test_files/specific3.png',
    #             './media/test_files/specific3.png',
    #             self.torch_model.conversion_properties
    #         )
    #         self.assertTrue('Target and source image could not be the same' in context.exception)

    def test_file_conversion_WITH_raw_files_EXPECT_new_file(self):
        swaped_image = self.torch_model.torchmodel.process(
            './media/test_files/face1.jpeg',
            './media/test_files/specific3.png',
            self.torch_model.conversion_properties
        )
        status, _ = cv2.imencode(".png", swaped_image)
        self.assertTrue(status)
        self.assertEqual((279, 260, 3), swaped_image.shape)

    # def test_file_conversion_WITH_existing_target_EXPECT_new_file(self):
    #     file = ConvertedFile.objects.create(
    #         title="Image file",
    #         selected_model=self.torch_model,
    #         target=File.objects.create(title="Image file", type=FileType.IMAGE),
    #         source=File.objects.create(title="Image file", type=FileType.IMAGE),
    #         type=FileType.IMAGE
    #     )
    #     file.target.file_object.name = './test_files/specific1.png'
    #     file.source.file_object.name = './test_files/specific3.png'
    #     dummy_user = User.objects.create(username='test_user')
    #
    #     file_pk, message = ConvertedFileAdmin.convert_file(file, dummy_user)
    #     self.assertIsNone(message)
    #
    #
    #     created_file = ConvertedFile.objects.get(id=file_pk)
    #     self.assertIsNotNone(created_file.created.file_object)
    #     self.assertEqual(len(created_file.created.file_object.file.read()), 19957)
    #
    #
    # def test_file_conversion_WITHOUT_source_EXPECT_error(self):
    #     file = ConvertedFile.objects.create(
    #         title="Image file",
    #         selected_model=self.torch_model,
    #         target=File.objects.create(title="Image file", type=FileType.IMAGE),
    #     )
    #     file.target.file_object.name = './test_files/specific1.png'
    #     dummy_user = User.objects.create(username='test_user')
    #
    #     with self.assertRaises(Exception) as context:
    #         ConvertedFileAdmin.convert_file(file, dummy_user)
    #         self.assertTrue('Both source and target need to be provided' in context.exception)
    #
    #
    # def test_file_conversion_WITHOUT_target_EXPECT_error(self):
    #     file = ConvertedFile.objects.create(
    #         title="Image file",
    #         selected_model=self.torch_model,
    #         source=File.objects.create(title="Image file", type=FileType.IMAGE)
    #     )
    #     file.source.file_object.name = './test_files/specific1.png'
    #     dummy_user = User.objects.create(username='test_user')
    #
    #     with self.assertRaises(Exception) as context:
    #         ConvertedFileAdmin.convert_file(file, dummy_user)
    #         self.assertTrue('Both source and target need to be provided' in context.exception)
    #
    #
    # def test_file_conversion_WITH_existing_files_EXPECT_new_file(self):
    #     file = ConvertedFile.objects.create(
    #         title="Image file",
    #         selected_model=self.torch_model,
    #         target=File.objects.create(title="Image file", type=FileType.IMAGE),
    #         source=File.objects.create(title="Image file", type=FileType.IMAGE),
    #         type=FileType.IMAGE
    #     )
    #
    #     file.target.file_object.name = './test_files/specific1.png'
    #     file.source.file_object.name = './test_files/specific3.png'
    #     dummy_user = User.objects.create(username='test_user')
    #
    #     file_pk, message = ConvertedFileAdmin.convert_file(file, dummy_user)
    #     self.assertIsNone(message)
    #
    #     created_file = ConvertedFile.objects.get(id=file_pk)
    #     self.assertIsNotNone(created_file.created.file_object)
    #
    # def test_file_conversion_WITH_different_file_formats_EXPECT_new_file(self):
    #     swaped_image = self.torch_model.torchmodel.process(
    #         './media/test_files/specific1.jpg',
    #         './media/test_files/specific3.png',
    #         self.torch_model.conversion_properties
    #     )
    #     status, _ = cv2.imencode(".png", swaped_image)
    #     self.assertTrue(status)
    #     self.assertEqual((279, 260, 3), swaped_image.shape)
    #
    # def test_file_conversion_WITHOUT_human_image_1_EXPECT_error_message(self):
    #     with self.assertRaises(Exception) as context:
    #
    #         self.torch_model.torchmodel.process(
    #             './media/test_files/dog.jpeg',
    #             './media/test_files/specific3.png',
    #             self.torch_model.conversion_properties
    #         )
    #         self.assertTrue('Face was not detected' in context.exception)
    #
    # def test_file_conversion_WITHOUT_human_image_2_EXPECT_error_message(self):
    #     with self.assertRaises(Exception) as context:
    #
    #         self.torch_model.torchmodel.process(
    #             './media/test_files/specific3.png',
    #             './media/test_files/dog.jpeg',
    #             self.torch_model.conversion_properties
    #         )
    #         self.assertTrue('Face was not detected' in context.exception)
    #
    # def test_file_conversion_WITH_not_existing_file_path_EXPECT_error_message(self):
    #     with self.assertRaises(Exception) as context:
    #         self.torch_model.torchmodel.process(
    #             './media/test_files/not_existing_path.jpeg',
    #             './media/test_files/specific3.png',
    #             self.torch_model.conversion_properties
    #         )
    #         self.assertTrue('Image does not exist in' in context.exception)
    #
