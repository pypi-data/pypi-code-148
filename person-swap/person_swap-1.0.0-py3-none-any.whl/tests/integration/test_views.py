from django.test import TestCase

from parameterized import parameterized


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user


# class MockRequest:
#     pass
#
#
# class MockSuperUser:
#     def has_perm(self, perm, obj=None):
#         return True
#
#
# request = MockRequest()
# request.user = MockSuperUser()


from django.contrib.auth.models import User, Group


class RegistrationTests(TestCase):
    def setUp(self):
        Group.objects.create(name="group_name")

    def test_GET_register_EXPECT_error_list(self):
        response = self.client.get("/register/")
        self.assertContains(response, "Create an Account")

    @parameterized.expand([
        ['user', 'Abcdef123?', 'Abcdef123?', 'email@mail.com', 301, None],
        ['', 'Abcdef123?', 'Abcdef123?', 'email@mail.com', 200, [('username', ['This field is required.'])]],
        ['user', '', 'Abcdef123?', 'email@mail.com', 200, [('password1', ['This field is required.'])]],
        ['user', 'Abcdef123?', '', 'email@mail.com', 200, [('password2', ['This field is required.'])]],
        ['user', 'Abcdef123?', 'Abcdef123?', '', 200, [('email', ['This field is required.'])]],
        ['user', 'password', 'password', 'email@mail.com', 200, [('password2', ['This password is too common.'])]],
        ['user', 'Abcdef123?', 'Abcdef123.', 'email@mail.com', 200,
         [('password2', ['The two password fields didn’t match.'])]],
        ['user', 'Abcdef123?', 'Abcdef123?', 'email', 200, [('email', ['Enter a valid email address.'])]],
    ])
    def test_register_user(self, username, pass1, pass2, email, status_code, message):
        data = {
            "username": username,
            "password1": pass1,
            "password2": pass2,
            "email": email
        }
        response = self.client.post("/register/", data=data)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(list(response.__dict__['context'][0]['errors']), message)
        else:
            self.assertTrue(User.objects.filter(username=username, email=email).exists())

    def test_register_user_WITH_existing_username_EXPECT_failure(self):
        data = {
            "username": "Juliana",
            "email": "email@mail.com",
            "password1": "Abcdef123?",
            "password2": "Abcdef123?"
        }
        response = self.client.post("/register/", data=data)
        self.assertEqual(response.status_code, 301)
        self.assertTrue(User.objects.filter(username="Juliana", email="email@mail.com").exists())

        response = self.client.post("/register/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")

    #

#
# class ConversionTests(TestCase):
#     convert_view_success_test_cases = [
#
#     ]
#     def setUp(self):
#         self.maxDiff = None
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
#     def test_GET_convert_view_EXPECT_success(self):
#
#         response = self.client.get("/convert/")
#         self.assertTemplateUsed(response, "admin/convert_action.html")
#         # self.assertContains(response, "Create an Account")
#         self.assertEqual(response.status_code, 200)
#
#     @parameterized.expand([
#         [{'title': 'title', 'target': '', 'source': '', 'target_raw': './media/test_files/specific3.png', 'source_raw': './media/test_files/specific3.png'}],
#         [{'title': 'title', 'target': './test_files/specific1.png', 'source': '', 'target_raw': '', 'source_raw': './media/test_files/specific3.png'}],
#         [{'title': 'title', 'target': '', 'source': './test_files/specific1.png', 'target_raw': './media/test_files/specific3.png', 'source_raw': ''}],
#         [{'title': 'title', 'target': './test_files/specific1.png', 'source': './test_files/specific3.png', 'target_raw': '', 'source_raw': ''}],
#     ])
#     def test_POST_convert_view_EXPECT_success(self, data):
#         if data.get('target_raw'):
#             data['target_raw'] = SimpleUploadedFile('file.png', open(data.get('target_raw'), 'rb').read())
#         if data.get('source_raw'):
#             data['source_raw'] = SimpleUploadedFile('file.png', open(data.get('source_raw'), 'rb').read())
#         if data.get('source'):
#             file = File.objects.create(title="Image file", type=FileType.IMAGE)
#             file.file_object.name = data.get('source')
#             file.save()
#             data['source'] = file.id
#         if data.get('target'):
#             file = File.objects.create(title="Image file", type=FileType.IMAGE)
#             file.file_object.name = data.get('target')
#             file.save()
#             data['target'] = file.id
#
#         data['selected_model'] = self.torch_model.id
#         data['conversion_properties'] = json.dumps(self.torch_model.conversion_properties)
#
#         response = self.client.post("/convert/", data=data, format='multipart')
#
#         self.assertEqual(response.status_code, 302)
#         self.torch_model.refresh_from_db()
#         self.assertEqual(self.torch_model.convertedfile_set.count(), 1)
#
#
#     @parameterized.expand([
#         [{'title': 'title', 'target': '', 'source': '', 'target_raw': './media/test_files/specific3.png', 'source_raw': ''}, 'Please provide source'],
#         [{'title': 'title', 'target': '', 'source': '', 'target_raw': '', 'source_raw': './media/test_files/specific3.png'}, 'Please provide target'],
#         [{'title': 'title', 'target': './test_files/specific1.png', 'source': './media/test_files/specific3.png', 'target_raw': '', 'source_raw': './media/test_files/specific3.png'}, 'Please provide only one file for source file and source.'],
#         [{'title': 'title', 'target': '', 'source': './test_files/specific1.png', 'target_raw': './media/test_files/specific3.png', 'source_raw': './media/test_files/specific3.png'}, 'Please provide only one file for source file and source.'],
#     ])
#     def test_POST_convert_view_WITH_valid_model_EXPECT_failure(self, data, message):
#         if data.get('target_raw'):
#             data['target_raw'] = SimpleUploadedFile('file.png', open(data.get('target_raw'), 'rb').read())
#         if data.get('source_raw'):
#             data['source_raw'] = SimpleUploadedFile('file.png', open(data.get('source_raw'), 'rb').read())
#         if data.get('source'):
#             file = File.objects.create(title="Image file", type=FileType.IMAGE)
#             file.file_object.name = data.get('source')
#             file.save()
#             data['source'] = file.id
#         if data.get('target'):
#             file = File.objects.create(title="Image file", type=FileType.IMAGE)
#             file.file_object.name = data.get('target')
#             file.save()
#             data['target'] = file.id
#
#         data['selected_model'] = self.torch_model.id
#         data['conversion_properties'] = json.dumps(self.torch_model.conversion_properties)
#
#         response = self.client.post("/convert/", data=data, format='multipart')
#         self.assertEqual(list(response.__dict__['context'][0]['errors'])[0][0], '__all__')
#         self.assertIn(message, list(response.__dict__['context'][0]['errors'])[0][1][0])
#
#
#     @parameterized.expand([
#         [{'target': '', 'source': ''}, False, False, False, 'selected_model', 'This field is required.'],
#         [{'title': 'title'}, True, False, False, 'conversion_properties', 'Conversion properties needs to be given'],
#         [{'title': 'title', 'conversion_properties': json.dumps({"use_mask": True})}, True, False, False, 'target', 'This field is required'],
#         [{'title': 'title', 'source': 'invalid', 'conversion_properties': json.dumps({"use_mask": True})}, True, False, False, 'source', 'Select a valid choice'],
#         [{'title': 'title', 'conversion_properties': json.dumps({"use_mask": True})}, True, True, False, 'source', 'Select a valid choice'],
#         [{'title': 'title', 'conversion_properties': json.dumps({"use_mask": True})}, True, False, True, 'target', 'Select a valid choice'],
#         [{'title': 'title', 'conversion_properties': json.dumps({"use_mask": True})}, True, True, True, 'target', 'Select a valid choice'],
#         [{'title': 'title', 'source': 'invalid', 'target': 'invalid', 'conversion_properties': json.dumps({"use_mask": True})}, True, False, False, 'target', 'Select a valid choice'],
#
#     ])
#     def test_POST_convert_view_EXPECT_failure(self, data, add_model, add_source, add_target, field, message):
#         if add_model:
#             data['selected_model'] = self.torch_model.id
#         if add_source:
#             data['source'] = File.objects.create(title="Image file", type=FileType.IMAGE)
#             data['source'].file_object.name = './test_files/specific1.png'
#         if add_target:
#             data['target'] = File.objects.create(title="Image file", type=FileType.IMAGE)
#             data['target'].file_object.name = './test_files/specific3.png'
#
#         response = self.client.post("/convert/", data=data, files={})
#         self.assertEqual(list(response.__dict__['context'][0]['errors'])[0][0], field)
#         self.assertIn(message, list(response.__dict__['context'][0]['errors'])[0][1][0])
#
#     def test_POST_convert_view_WITH_invalid_model_EXPECT_failure(self):
#         data = {'target': '', 'source': '', 'selected_model': "Not a valid choice"}
#         response = self.client.post("/convert/", data=data, files={})
#         self.assertEqual(list(response.__dict__['context'][0]['errors'])[0][0], 'selected_model')
#         self.assertIn('Select a valid choice', list(response.__dict__['context'][0]['errors'])[0][1][0])
