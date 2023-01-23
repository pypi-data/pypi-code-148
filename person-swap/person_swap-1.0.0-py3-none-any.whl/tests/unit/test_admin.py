from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from parameterized import parameterized

from dash.forms.forms import FileConvertForm, ConvertForm
from dash.models import Model, File, FileType


# process_conversion
# files_table

# files_link
# get_urls
# model_title

class TestConvertForms(TestCase):

    @parameterized.expand([
        [FileConvertForm, True, 2, False, True],
        [FileConvertForm, False, 1, False, True],
        [FileConvertForm, True, 2, True, True],
        [FileConvertForm, False, 2, True, True],
        [ConvertForm, True, 2, False, True],
        # [ConvertForm, False, 1, False, True],
        [ConvertForm, True, 2, True, True],
        [ConvertForm, False, 2, True, True],
        # [ConvertForm, False, 2, True, False],
        # [ConvertForm, False, 0, False, False],
    ])
    def test_filter_form_values(self, form_class, is_superuser, models_count, public, with_user):
        dummy_user = User.objects.create(username='test_user',
                                         is_superuser=is_superuser) if with_user else AnonymousUser
        Model.objects.create(owner=dummy_user, type=FileType.IMAGE, public=public)
        Model.objects.create(type=FileType.IMAGE, public=public)
        File.objects.create(owner=dummy_user, type=FileType.IMAGE, public=public)
        File.objects.create(type=FileType.IMAGE, public=public)

        form = form_class()
        self.assertEqual(form.fields['selected_model'].queryset.count(), 2)
        self.assertEqual(form.fields['source'].queryset.count(), 2)
        if form_class is ConvertForm:
            self.assertEqual(form.fields['target'].queryset.count(), 2)

        form.filter_form_values(dummy_user)
        self.assertEqual(form.fields['selected_model'].queryset.count(), models_count)
        self.assertEqual(form.fields['source'].queryset.count(), models_count)
        if form_class is ConvertForm:
            self.assertEqual(form.fields['target'].queryset.count(), models_count)
