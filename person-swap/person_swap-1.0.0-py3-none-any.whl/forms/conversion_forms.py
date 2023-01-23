from django import forms
from django.forms import ModelForm

from dash.models import FileType
from dash.models.file import ConvertedFile

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


class ModelSelectionForm(ModelForm):
    class Meta:
        model = ConvertedFile
        fields = ('selected_model',)

    def __init__(self, file_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_model'].required = True
        self.fields['selected_model'].queryset = self.fields['selected_model'].queryset.filter(type=file_type)

        if file_type:
            CHOICES = [('source', 'as source'), ('target', 'as target')]
            self.fields['selected_file_as'] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
        else:
            CHOICES = [(FileType.IMAGE.value, FileType.IMAGE.value), (FileType.MP3.value, 'Audio'),
                       (FileType.VIDEO.value, FileType.VIDEO.value)]
            self.fields['from'] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
            self.fields['to'] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
