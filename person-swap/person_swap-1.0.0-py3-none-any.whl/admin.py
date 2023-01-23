import logging

from django import forms
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import re_path as url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .forms.conversion_forms import ModelSelectionForm
from .forms.forms import FileConvertForm
from .forms.model_forms import TorchModelAdminForm, VoiceSwapModelAdminForm, ModelFileAdminForm
from .models import File, Model, VoiceSwapModel, FileType
from .models.file import ConvertedFile
from .models.model import TorchModel, ModelFile, VideoSwapModel

logger = logging.getLogger(__name__)

from django.contrib import admin


class MyAdminSite(admin.AdminSite):

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff


class ModelFileInline(admin.TabularInline):
    model = Model.model_files.through
    extra = 2

    class Meta:
        auto_created = True
        fields = ('title', 'file_object', 'public')


class AbstractAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # if request.path == '/dash/dash/convertedfile/add/' and request.user.username == "anonymous":
        #     return True
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        if obj:
            return (obj and obj.owner and obj.owner.id is request.user.id) or (
                    obj and not obj.owner and request.user.is_superuser)
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        # if request.path.startswith("/dash/dash/convertedfile/") and request.user.username == "anonymous":
        #     return True
        if obj:
            return request.user.is_superuser or (obj and ((obj.owner is request.user) or obj.public))
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or (obj and obj.owner is request.user)
        return request.user.is_staff

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_staff


@admin.register(ModelFile)
class ModelFileAdmin(AbstractAdmin):
    form = ModelFileAdminForm


@admin.register(Model)
class ModelAdmin(AbstractAdmin):
    inlines = (ModelFileInline,)

    list_display = ('title', 'owner', 'files_link')
    list_filter = ("type",)
    search_fields = ("title__startswith",)
    fields = ('type', 'owner', 'title', 'public')
    readonly_fields = ()

    def files_link(self, obj):
        count = obj.convertedfile_set.count()
        url = (
                reverse("admin:dash_file_changelist")
                + "?"
                + urlencode({"selected_model__pk": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Files</a>', url, count)

    files_link.short_description = "Files"


@admin.register(TorchModel)
class TorchModelAdmin(ModelAdmin):
    form = TorchModelAdminForm
    fields = ('type', 'owner', 'title', 'public', 'conversion_properties')  # , 'display_files')


@admin.register(VoiceSwapModel)
class VoiceSwapModelAdmin(ModelAdmin):
    form = VoiceSwapModelAdminForm
    list_display = ('title', 'owner', 'files_link')
    list_filter = ("type",)
    search_fields = ("title__startswith",)
    fields = ('type', 'owner', 'title', 'public', 'vocoder', 'acoustic_model')  # , 'display_files')
    readonly_fields = ()


@admin.register(VideoSwapModel)
class VideoSwapModelAdmin(ModelAdmin):
    form = VoiceSwapModelAdminForm
    list_display = ('title', 'owner', 'files_link')
    list_filter = ("type",)
    search_fields = ("title__startswith",)
    fields = ('type', 'owner', 'title', 'public', 'face_model', 'voice_model')  # , 'display_files')
    readonly_fields = ()


@admin.register(File)
class FileAdmin(AbstractAdmin):
    list_display = ('type', 'title', 'owner', 'file_actions', 'display_file')
    list_filter = ("type",)
    search_fields = ("title__startswith",)
    fields = ('type', 'owner', 'title', 'public', 'file_object')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<file_id>.+)/convert/$',
                self.admin_site.admin_view(self.call_file_conversion),
                name='file-convert',
            )
        ]
        return custom_urls + urls

    def file_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Convert</a>',
            reverse('admin:file-convert', args=[obj.pk]),
        )

    file_actions.short_description = 'Actions'
    file_actions.allow_tags = True

    def call_file_conversion(self, request, file_id, *args, **kwargs):
        # return ConvertedFileAdmin(ConvertedFile, self.admin_site).add_view(request, file_id, *args, **kwargs)
        return ConvertedFileAdmin(ConvertedFile, self.admin_site).process_conversion(request, file_id, *args, **kwargs)

    file_actions.short_description = 'Actions'
    file_actions.allow_tags = True

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_convert': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


class ModelInline(admin.TabularInline):
    model = Model
    fields = ('title', 'conversion_properties')
    extra = 2


@admin.register(ConvertedFile)
class ConvertedFileAdmin(AbstractAdmin):
    list_display = ('type', 'title', 'owner', 'display_file')
    list_filter = ("type",)
    search_fields = ("title__startswith",)
    fields = ('selected_model', 'title', 'files_table', 'image_preview')

    readonly_fields = ('files_table', 'image_preview')

    form = FileConvertForm

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(ConvertedFileAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            return (obj and obj.owner and obj.owner.id is request.user.id) or (
                    obj and not obj.owner and request.user.is_superuser)
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or (obj and ((obj.owner is request.user) or obj.public))
        return request.user.is_staff

    def add_view(self, request, form_url="", extra_context=None):
        if len(request.POST) > 0 and not request.POST.get('selected_file_as'):
            form = FileConvertForm(
                False,
                request.POST,
                request.FILES,
                request=request
            )

            if not form.is_valid():
                logger.warning(f"Model selection failed: {form.errors}")

                self.exclude = ('files_table', 'image_preview', 'source', 'target', 'conversion_properties')
                self.fields = ('title', 'selected_model', 'source_file', 'target_file')

                adminForm = helpers.AdminForm(
                    form,
                    list(self.get_fieldsets(request)),
                    self.prepopulated_fields,
                    self.readonly_fields,
                    model_admin=self
                )

                return super(ConvertedFileAdmin, self).add_view(
                    request,
                    form_url=form_url,
                    extra_context={
                        'adminform': adminForm
                    }
                )


            converted_file_pk, message = self.convert_file(form.instance, request.user)
            if message:
                form.add_error(None, message)
                return self.return_conversion_form(request, form)

            self.message_user(request, 'Success')
            return self.response_add(request, form.instance)

        self.exclude = ('files_table', 'image_preview',)
        self.fields = ('title', 'selected_model', 'source_file', 'target_file')
        self.readonly_fields = ()
        return super(ConvertedFileAdmin, self).add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.exclude = ('source_file', 'target_file')
        self.fields = ('selected_model', 'title', 'files_table', 'image_preview')
        self.readonly_fields = ('selected_model', 'title', 'files_table', 'image_preview')
        return super(ConvertedFileAdmin, self).change_view(request, object_id)

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(f'/dash/dash/convertedfile/{obj.id}/change/')

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.temp = True
        status, message = obj.convert()
        if not status:
            form.add_error(None, message)
            # TODO
            # converted_file.delete()
            # return render(request, 'admin/convert_action.html', {"form": form})

        obj.save()

    def process_conversion(self, request, file_id, *args, **kwargs):
        if request.method != 'POST':
            form = ModelSelectionForm(
                file_type=File.objects.get(id=file_id).type
            )

        elif request.POST.get('title') is None:
            file = File.objects.get(id=file_id)

            model_form = ModelSelectionForm(file.type, request.POST)
            if not model_form.is_valid():
                logger.warning(f"Model selection failed: {model_form.errors}")
                return self.return_conversion_form(request, model_form)

            form = FileConvertForm(
                fill_values=True,
                initial={
                    model_form.data['selected_file_as'] + "_file_1": file,
                    model_form.data['selected_file_as'] + "_file": file,
                    'selected_model': model_form.cleaned_data['selected_model'],
                    'conversion_properties': model_form.cleaned_data['selected_model'].conversion_properties
                },
                request=request,
                file_type=file.type
            )

            self.exclude = ('files_table', 'image_preview', 'source', 'target', 'conversion_properties')
            self.fields = ('title', 'selected_model', 'source_file', 'target_file')

            adminForm = helpers.AdminForm(
                form,
                list(self.get_fieldsets(request)),
                self.prepopulated_fields,
                self.readonly_fields,
                model_admin=self
            )

            request.method = "GET"

            return self.add_view(
                request,
                form_url='/dash/dash/convertedfile/add/',
                extra_context={
                    'adminform': adminForm
                }
            )
        else:
            form = FileConvertForm(
                False,
                request.POST,
                request.FILES,
                request=request
            )

            if not form.is_valid():
                logger.warning(f"Model selection failed: {form.errors}")
                file = File.objects.get(id=file_id)

                model_form = ModelSelectionForm(file.type, request.POST)
                if not model_form.is_valid():
                    logger.warning(f"Model selection failed: {model_form.errors}")
                    return self.return_conversion_form(request, model_form)

                form = FileConvertForm(
                    fill_values=True,
                    initial={
                        model_form.data['selected_file_as'] + "_file_1": file,
                        model_form.data['selected_file_as'] + "_file": file,
                        'selected_model': model_form.cleaned_data['selected_model'],
                        'conversion_properties': model_form.cleaned_data['selected_model'].conversion_properties
                    },
                    request=request,
                    file_type=file.type
                )

                self.exclude = ('files_table', 'image_preview', 'source', 'target', 'conversion_properties')
                self.fields = ('title', 'selected_model', 'source_file', 'target_file')

                adminForm = helpers.AdminForm(
                    form,
                    list(self.get_fieldsets(request)),
                    self.prepopulated_fields,
                    self.readonly_fields,
                    model_admin=self
                )

                request.method = "GET"

                return self.add_view(
                    request,
                    form_url='/dash/dash/convertedfile/add/',
                    extra_context={
                        'adminform': adminForm
                    }
                )

            converted_file_pk, message = self.convert_file(form.instance, request.user)

            if message:
                form.add_error(None, message)
                return self.return_conversion_form(request, form)

            self.message_user(request, 'Success')

            url = reverse(
                'admin:dash_convertedfile_change',
                args=[converted_file_pk],
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(url)

        return self.return_conversion_form(request, form)

    def return_conversion_form(self, request, form):
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form

        return TemplateResponse(
            request,
            'admin/file_convert_action.html',
            context,
        )

    @staticmethod
    def convert_file(converted_file, owner):
        converted_file.owner = owner

        status, message = converted_file.convert()
        if not status:
            logger.warning(f"File conversion failed: {message}")
            if converted_file.pk:
                converted_file.delete()
            return None, message or "Something went wrong"

        converted_file.save()

        return converted_file.pk, None

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
        )

    def files_table(self, obj):
        if obj.created.file_object:
            if obj.type == FileType.IMAGE:
                return format_html("""
                           <table>
                               <tr>
                                   <td> Source </td>
                                   <td> Target </td>
                                   <td> Created </td>
                               </tr>
                               <tr>
                                   <td><img width="200px" height="200px" src="{img1}"></td>
                                   <td><img width="200px" height="200px" src="{img2}"></td>
                                   <td><img width="200px" height="200px" src="{img3}"></td>
                               </tr>
                           </table>
                       """,
                                   img1=obj.source.file_object.url,
                                   img2=obj.target.file_object.url,
                                   img3=obj.created.file_object.url
                                   )
            if obj.type == FileType.VIDEO:
                return format_html("""
                           <table>
                               <tr>
                                   <td> Source </td>
                                   <td> Target </td>
                                   <td> Created </td>
                               </tr>
                               <tr>
                                   <td ><img width="200px" height="200px" src="{img1}"></td>
                                   <td><video width="200px" height="200px" controls> <source src="{vid1}" type="video/mp4"></video></td>
                                   <td><video width="200px" height="200px" controls> <source src="{vid2}" type="video/mp4"></video></td>
                               </tr>
                           </table>
                       """,
                                   img1=obj.source.file_object.url,
                                   vid1=obj.target.file_object.url,
                                   vid2=obj.created.file_object.url
                                   )
            if obj.type == FileType.MP3:
                return format_html("""
                         <table>
                             <tr>
                                 <td> Source </td>
                                 <td> Target </td>
                                 <td> Created </td>
                             </tr>
                             <tr>
                                 <td><audio controls> <source src="{obj1}" type="audio/mp3"></audio></td>
                                 <td><audio controls> <source src="{obj2}" type="audio/mp3"></audio></td>
                                 <td><audio controls> <source src="{obj3}" type="audio/mp3"></audio></td>
                             </tr>
                         </table>
                     """,
                                   obj1=obj.source.file_object.url,
                                   obj2=obj.target.file_object.url,
                                   obj3=obj.created.file_object.url
                                   )
                #
                # return format_html(
                #     f'<audio controls> <source src="{obj.target.file_object.url}" type="audio/mp3"></audio>')
            else:
                # raise Exception
                pass

        return format_html('<strong>There is no image for this entry.<strong>')

    def model_title(self, obj):
        return format_html("<b><i>{}</i></b>", obj.selected_model.title) if obj.selected_model else "None"

    model_title.short_description = "Model"
