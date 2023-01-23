import json

from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import Q
from django.forms import ModelForm
from django.utils.datastructures import MultiValueDictKeyError

from dash.models import File
from dash.models import FileType
from dash.models.file import ConvertedFile
from dash.models.model import TorchModelFileType, Model


class RawConvertedFile(ConvertedFile):
    def __init__(self):
        super(RawConvertedFile, self).__init__()


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None, choices=[]):
        widgets = [forms.ClearableFileInput(),
                   forms.Select(choices=choices)]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return ['', value.id]
        else:
            return ['', '']


class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, queryset, *args, **kwargs):
        choices = [(item.get('id'),
                    f"{item.get('title') if item.get('title') else 'File ' + str(item.get('id'))} ({item.get('type')})")
                   for item in queryset.values('id', 'title', 'type').all()]
        choices = [(0, '-----')] + choices
        list_fields = [forms.FileField(required=False),
                       forms.ChoiceField(choices=choices)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

        self.widget = MultiWidgetBasic(choices=choices)

    def compress(self, values):
        ## compress list to single object
        ## eg. date() >> u'31/12/2012'
        return values

    def clean(self, value):
        super(MultiExampleField, self).clean(value)


DATA_SCHEMA = {

    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "First and Last name",
            "minLength": 4,
            "default": "Jeremy Dorn"
        }
    }
}


class CustomAutocompleteSelect(AutocompleteSelect):
    def __init__(self, field, prompt="", admin_site=None, attrs=None, choices=(), using=None):
        self.prompt = prompt
        super().__init__(field, admin_site, attrs=attrs, choices=choices, using=using)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.update({
            'data-ajax--delay': 250,
            'data-placeholder': self.prompt,
            'style': 'width: 30em;'
        })
        return attrs


class FileConvertForm(ModelForm):
    source_file = MultiExampleField(require_all_fields=False, required=False, queryset=File.objects.all())
    target_file = MultiExampleField(require_all_fields=False, required=False, queryset=File.objects.all())

    def __init__(self, fill_values=True, file_type=None, *args, **kwargs):
        # self.base_fields['target_file'].fields[1].choices =
        self.request = kwargs.pop('request', None)
        super(FileConvertForm, self).__init__(*args, **kwargs)
        # if self.fields.get('selected_model'):
        #     self.fields['selected_model'].required = True
        if not file_type and self.request.POST.get('selected_model'):
            file_type = Model.objects.filter(id=self.request.POST.get('selected_model')).values_list('type',
                                                                                                     flat=True).get()
        if file_type:
            self.fields['selected_model'].queryset = self.fields['selected_model'].queryset.filter(type=file_type)
            self.source_file = MultiExampleField(require_all_fields=False, required=False,
                                                 queryset=File.objects.filter(type=file_type).all())
            self.target_file = MultiExampleField(require_all_fields=False, required=False,
                                                 queryset=File.objects.filter(type=file_type).all())

        if fill_values:
            for key, value in self.initial.get('conversion_properties', {}).items():
                if key in TorchModelFileType._value2member_map_:
                    continue
                if isinstance(value, str):

                    self.fields[key] = forms.CharField(initial=value)
                elif isinstance(value, bool):
                    self.fields[key] = forms.BooleanField(initial=value)
                elif isinstance(value, int):
                    self.fields[key] = forms.IntegerField(initial=value)

    class Meta:
        model = ConvertedFile
        fields = '__all__'
        exclude = ('owner', 'public', 'type')

    def filter_form_values(self, user):
        self.fields['selected_model'].queryset.filter(type=self.instance.type)
        self.fields['source'].queryset.filter(type=self.instance.type)
        self.fields.pop('created', None)
        if user and user.is_authenticated and not user.is_superuser:
            self.fields['selected_model'].queryset = self.fields['selected_model'].queryset.filter(
                Q(owner=user) | Q(public=True))
            self.fields['source'].queryset = self.fields['source'].queryset.filter(Q(owner=user) | Q(public=True))

        elif user and user.is_anonymous:
            self.fields['selected_model'].queryset = self.fields['selected_model'].queryset.filter(public=True)
            self.fields['source'].queryset = self.fields['source'].queryset.filter(public=True)

    def clean(self, convert_type=FileType.IMAGE):
        super().clean()
        try:
            if self.data.get('conversion_properties'):
                for key, value in json.loads(self.data['conversion_properties']).items():
                    if key in self.data:
                        self.cleaned_data['conversion_properties'][key] = self.data[key]
            else:
                self.cleaned_data['conversion_properties'] = {}

            post_data = self.request.POST
            if post_data.get('selected_model'):
                # obj.selected_model_id = post_data.get('selected_model')
                self.cleaned_data['selected_model'] = Model.objects.get(id=post_data.get('selected_model'))
            else:
                self.add_error('selected_model', 'Please provide model.')

            if post_data.get('target_file_1', '0') is not '0':
                self.cleaned_data['target'] = File.objects.get(id=post_data.get('target_file_1'))

            if post_data.get('source_file_1', '0') is not '0':
                self.cleaned_data['source'] = File.objects.get(id=post_data.get('source_file_1'))

            if self.data.get('target_file_0'):
                if self.cleaned_data.get('target'):
                    self.add_error('target_file', 'Please provide only one file for target.')

                self.cleaned_data['target'] = File(title=self.data.get('target_file_0').name)
                self.cleaned_data['target'].file_object.save(
                    self.data.get('target_file_0').name,
                    ContentFile(self.data.get('target_file_0').file.read())
                )
                self.cleaned_data['target'].save()

            if self.data.get('source_file_0'):
                if self.cleaned_data.get('source'):
                    self.add_error('source_file', 'Please provide only one file for source.')

                self.cleaned_data['source'] = File(title=self.data.get('source_file_0').name)
                self.cleaned_data['source'].file_object.save(
                    self.data.get('source_file_0').name,
                    ContentFile(self.data.get('source_file_0').file.read())
                )
                self.cleaned_data['source'].save()

            if not self.cleaned_data.get('source') or not self.cleaned_data.get('target'):
                self.add_error(None, "Both source and target need to be provided.")
            print(self.cleaned_data.get('selected_model').type == FileType.VIDEO.value,self.cleaned_data.get('source').type == FileType.IMAGE.value, self.cleaned_data.get('target').type == FileType.VIDEO.value)
            print(self.cleaned_data.get('selected_model').type,self.cleaned_data.get('source').type, self.cleaned_data.get('target').type)
            if not self.cleaned_data.get('source').type == self.cleaned_data.get('target').type == self.cleaned_data.get('selected_model').type \
                and not (self.cleaned_data.get('selected_model').type == FileType.VIDEO.value
                    and self.cleaned_data.get('source').type == FileType.IMAGE.value
                    and self.cleaned_data.get('target').type == FileType.VIDEO.value):
                self.add_error(None, "Files and model's 'types suppose to match")


        except MultiValueDictKeyError as ex:
            self.add_error(str(ex)[1:-1], "This field is required.")
        except ValueError as ex:
            self.add_error(None, ex)


    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    "created" if self.instance._state.adding else "changed",
                )
            )
        if self.cleaned_data.get('target'):
            self.instance.target_id = self.cleaned_data['target'].id
        if self.cleaned_data.get('source'):
            self.instance.source_id = self.cleaned_data['source'].id
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
