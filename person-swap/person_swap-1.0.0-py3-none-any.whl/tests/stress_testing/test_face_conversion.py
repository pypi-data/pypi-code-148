# '''
# Examples:
#
# Run for 15 seconds maxing out all processors:
#   stress.py 15
#
# Run for 15 seconds with each subprocess sleeping for 0.01s every 100,000 cycles across all processors (on my machine it's about a 50% duty cycle):
#   stress.py 15 0.01 100000
#
# Run for 15 seconds, sleep 0.01s every 100,000 cycles, but only use a max of 8 processors:
#   stress.py 15 0.01 100000 8
# '''
# from math import ceil
# from hashlib import sha512
# from multiprocessing import Pool
# import time
# import sys
# from itertools import repeat
# from multiprocessing import Pool, cpu_count
# from django.test import TestCase
# from syncer import sync
#
# from django.contrib.admin.sites import AdminSite
# from dash.models import File, FileType
# from dash.admin import ModelAdmin, ConvertedFileAdmin
# from dash.models.file import ConvertedFile
# from dash.models.model import TorchModel, ModelFile, TorchModelFileType
# import cv2
# from django.contrib.admin.sites import AdminSite
#
#
#
# class MockRequest(object):
#     def __init__(self, user=None):
#         self.user = user
#
#
# from django.contrib.auth.models import User
#
#
# class StressTesting(TestCase):
#
#     def setUp(self):
#         self.site = AdminSite()
#         self.torch_model = TorchModel.objects.create(
#             title="Image file",
#             type=FileType.IMAGE
#         )
#         model_conversion_files = {
#             TorchModelFileType.MAIN_MODEL: './test_files/arcface_checkpoint.tar',
#             TorchModelFileType.MASK_DETECTOR: './test_files/mask_detection.pth',
#             TorchModelFileType.DETECTOR: './test_files/detection.onnx',
#             TorchModelFileType.GENERATOR: './test_files/latest_net_G.pth'
#         }
#         for key, path in model_conversion_files.items():
#             model_file = ModelFile.objects.create(
#                 title=key.value,
#                 type=FileType.IMAGE,
#                 model_file_type=key
#             )
#             model_file.file_object.name = path
#             model_file.save()
#             self.torch_model.model.model_files.add(model_file)
#
#         self.torch_model.save()
#
#     def test_file_conversion_WITH_same_files_EXPECT_error_message(self):
#         # path = '1m_words.txt'
#         for i in [1,2,3,4,5,6,7,8]:
#             self.print_data(i)
#         # words = ['asdasda', 'dasda']
#         # print(f'Loaded {len(words)}')
#         # # create the process pool
#         # with Pool(4) as pool:
#         #     # create a set of word hashes
#         #     known_words = set(pool.map(self.hash_word, words))
#         # print(f'Done, with {len(known_words)} hashes')
#         # with self.assertRaises(Exception) as context:
#         #
#         #     self.torch_model.torchmodel.process(
#         #         './media/test_files/specific3.png',
#         #         './media/test_files/specific3.png',
#         #         self.torch_model.conversion_properties
#         #     )
#         #     self.assertTrue('Target and source image could not be the same' in context.exception)
#
#
#     @sync
#     async def print_data(self, i):
#         print("rEEE", i)
#
#      # Can be called synchronously
#     # hash one word using the SHA algorithm
#     def hash_word(self, word):
#         # create the hash object
#         hash_object = sha512()
#         # convert the string to bytes
#         byte_data = word.encode('utf-8')
#         # hash the word
#         hash_object.update(byte_data)
#         # get the hex hash of the word
#         return hash_object.hexdigest()
#
#     # load a file of words
#     def load_words(self, path):
#         # open the file
#         with open(path) as file:
#             # read all data as lines
#             return file.readlines()
#
#
#     def f(self, x):
#         set_time = 10
#         timeout = time.time() + 60 * float(set_time)  # X minutes from now
#         while True:
#             if time.time() > timeout:
#                 break
#             x * x
