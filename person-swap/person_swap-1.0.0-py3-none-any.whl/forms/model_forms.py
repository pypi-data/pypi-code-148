from django import forms

from dash.models.model import TorchModel, VideoSwapModel, Model, VoiceSwapModel, ModelFile


class ModelAdminForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = "__all__"


class ModelFileAdminForm(forms.ModelForm):
    class Meta:
        model = ModelFile
        fields = "__all__"


class VoiceSwapModelAdminForm(ModelAdminForm):
    class Meta:
        model = VoiceSwapModel
        fields = "__all__"


class VideoSwapModelAdminForm(ModelAdminForm):
    class Meta:
        model = VideoSwapModel
        fields = "__all__"


class TorchModelAdminForm(ModelAdminForm):
    class Meta:
        model = TorchModel
        fields = '__all__'
