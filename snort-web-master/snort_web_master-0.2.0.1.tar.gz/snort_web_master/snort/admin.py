import copy
import os
import csv
import time
from io import StringIO
from django.contrib import messages
from functools import partial
from import_export.admin import ImportExportModelAdmin
from django import forms
from .models import SnortRule, SnortRuleViewArray, save_rule_to_s3, delete_rule_from_s3
from .snort_templates import types_list
from .parser import Parser
from django.utils.encoding import smart_str
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.html import mark_safe
from django.db import transaction
import suricataparser
from snort.views import build_keyword_dict
# Register your models here.
from django.contrib import admin
from django_object_actions import DjangoObjectActions
import subprocess
from settings.models import Setting, keywords, attackGroup
from django.shortcuts import render
from pcaps.admin import verify_legal_pcap
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime


class StoreAdminForm(forms.ModelForm):
    ## add an extra field:
    upfile = forms.FileField()

    class Meta:
        model = SnortRule
        fields = "__all__"

    def clean(self):
        cleaned_data = super(StoreAdminForm, self).clean()

        if "upfile" in self.changed_data:
            ### file validation on file type etc here ..
            ## file is valid:
            ## next lines deal with the InMemoryUploadedFile Type
            path = settings.MEDIA_ROOT.joinpath("___tmp___")
            tmp = default_storage.save(path, ContentFile(cleaned_data["upfile"].read()))

            ## ...

BASE_FIELDS = [
    "id", "active", "is_template", "deleted", "admin_locked", 'name', "request_ref", "main_ref", "description",
    "extra", "location", "user"]
FILTER_FIELDS = ("active", "is_template", "deleted", "admin_locked")
ADVANCE_FILTER_FIELDS = tuple(i for i in BASE_FIELDS + ["content", ("pcap_sanity_check__name", "pcap_sanity_check_name"), ("pcap_legal_check__name", "pcap_legal_check_name"),("group_name", "group_name")])
FIELDS = [
    "id", "content", "active", "is_template", "deleted", "admin_locked", 'name', "request_ref", "main_ref", "snort_builder", "description",
    "group", "extra", "location", "user", 'pcap_sanity_check', "pcap_legal_check", ]
SEARCH_FIELDS = tuple(i for i in BASE_FIELDS + ["content", "pcap_sanity_check__name", "pcap_legal_check__name", "group__name"])
BASE_BUILDER_KEY = ("action", "protocol", "srcipallow", "srcip", "srcportallow", "srcport", "direction", "dstipallow",
                    "dstportallow", "dstport")

INPUT_TYPE = ("srcip" , "srcport", "dstip", "dstport")
from django.core.cache import cache
# todo: upload unmanaged rule file

class SnortRuleAdminForm(forms.ModelForm):
    def clean_user(self):
        return getattr(self.current_user, self.current_user.USERNAME_FIELD)

    def clean_date(self):
        return self.cleaned_data["date"]

    def clean_type(self):
        if not dict(types_list).get(self.cleaned_data.get("type")):
            raise forms.ValidationError("cant find type, did you forgot it? or forgot to add type to db", code=404)
        return self.cleaned_data.get("type")

    def clean_content(self):
        try:
            parser = Parser(self.data["content"])
            parser.parse_header()
            parser.parse_options()
        except Exception as e:
            raise forms.ValidationError(e)

        return self.data["content"]

    def clean_location(self):
        try:
            if os.path.dirname(self.cleaned_data["location"]) != "":
                os.makedirs(os.path.dirname(self.cleaned_data["location"]), exist_ok=True)
            os.makedirs(os.path.dirname(self.cleaned_data["location"]), exist_ok=True)
            with open(self.cleaned_data["location"], "w") as rule_file:
                rule_file.write(self.cleaned_data["content"])
        except Exception as e:
            forms.ValidationError(e)
        return self.cleaned_data["location"]

    def clean_is_template(self):
        if not self.cleaned_data.get("is_template"):
            self.cleaned_data["active"] = False
        return self.cleaned_data.get("is_template")

    def clean_pcap_sanity_check(self):
        # return self.cleaned_data.get("pcap_validation")
        if not self.cleaned_data.get("pcap_sanity_check"):
            if Setting.objects.get(**{"name": "FORCE_SANITY_CHECK"}).value == "False":
                return self.cleaned_data["pcap_sanity_check"]
            elif Setting.objects.get(**{"name": "FORCE_SANITY_CHECK"}).value == "True":
                raise forms.ValidationError(
                    f"no pcap provided fof sanity check, plase add pcap or edit setting(FORCE_SANITY_CHECK)")
            else:
                raise forms.ValidationError(
                    f"bad configuration setting (FORCE_SANITY_CHECK), pleas edit setting(FORCE_SANITY_CHECK) must be True or False")
        cur_rule = SnortRule()
        cur_rule.content = self.data.get("content")
        cur_rule.location = self.data.get("location")
        cur_rule.group = self.instance.group
        cur_rule.id = self.data.get("id")
        cur_rule.main_ref = self.data.get("main_ref")
        cur_rule.name = self.data.get("name")
        cur_rule.type = self.data.get("type")
        cur_rule.user = self.data.get("user")
        cur_rule.request_ref = self.data.get("request_ref")

        validate_pcap_snort(self.cleaned_data.get("pcap_sanity_check"), cur_rule)
        return self.cleaned_data["pcap_sanity_check"]

    # only admin can activate admin locked rule
    def clean_pcap_legal_check(self):
        # return self.cleaned_data.get("pcap_validation")

        if not self.cleaned_data.get("pcap_legal_check"):
            if Setting.objects.get(**{"name": "FORCE_LEGAL_CHECK"}).value == "False":
                return self.cleaned_data["pcap_legal_check"]
            elif Setting.objects.get(**{"name": "FORCE_LEGAL_CHECK"}).value == "True":
                raise forms.ValidationError(
                    f"no pcap provided fof sanity check, plase add pcap or edit setting(FORCE_LEGAL_CHECK)")
            else:
                raise forms.ValidationError(
                    f"bad configuration setting (FORCE_LEGAL_CHECK), pleas edit setting(FORCE_LEGAL_CHECK) must be True or False")

        cur_rule = SnortRule()
        cur_rule.content = self.data.get("content")
        cur_rule.location = self.data.get("location")
        cur_rule.group = self.data.get("group")
        cur_rule.id = self.data.get("id")
        cur_rule.main_ref = self.data.get("main_ref")
        cur_rule.name = self.data.get("name")
        cur_rule.type = self.data.get("type")
        cur_rule.user = self.data.get("user")
        cur_rule.request_ref = self.data.get("request_ref")

        count = validate_pcap_snort(self.cleaned_data.get("pcap_legal_check"), cur_rule)
        max_allowd = self.cleaned_data["MAX_MATCH_ALLOWD"]
        if int(count) > max_allowd:
            self.cleaned_data["admin_locked"] = True
            self.instance.admin_locked = True
            self.instance.save()
            if self.cleaned_data["active"] == True:
                if not self.current_user.is_staff and not self.current_user.is_superuser:
                    raise forms.ValidationError(
                        f"rule is admin locked due to hige number of validations {count}, please contact admin or fix rule\n all changed of an admin locked rull must be approved by admin")
        else:
            self.cleaned_data["admin_locked"] = False
            self.instance.admin_locked = False
            self.instance.save()

        return self.cleaned_data["pcap_legal_check"]

    def clean_active(self):
        if self.instance.active:
            return self.cleaned_data["active"]
        locked = False
        if self.cleaned_data.get("admin_locked") is None:
            locked = self.instance.admin_locked
        else:
            locked = self.cleaned_data.get("admin_locked")
        if self.cleaned_data["active"] and locked:
            if not self.current_user.is_staff and not self.current_user.is_superuser:
                raise forms.ValidationError(
                    f"rule is admin locked, please contact admin", code=403)
        return self.cleaned_data["active"]

    @transaction.atomic
    def clean(self):
        try:
            self.instance.user = self.clean_user()
            self.instance.content = self.clean_content()
        except Exception as e:
            self.add_error(None, e)
        rule_keys = []
        self.instance.deleted = False
        if not self.instance.pk and not self.errors:
            self.instance.save()
        # SnortRuleViewArray.objects.filter(snortId=None).delete()
        if not self.errors:
            SnortRuleViewArray.objects.filter(snortId=self.instance.id).delete()
        for key, value in self.data.items():
            if key in FIELDS + ['csrfmiddlewaretoken', "_save"]:
                continue
            item_type = "select"
            location_x = 0
            location_y = 0
            if "keyword_selection" in key:
                location_x = 0
                try:
                    index = key.index("-")
                except:
                    index = len(key)
                location_y = int(key[len("keyword_selection"):index])
            elif "keyword" in key:
                try:
                    index = key.index("-", key.index("-") + 1)
                except:
                    index = len(key)
                if key[key.index("-") + 1:index] == "not":
                    location_x = 0
                    location_y = 0
                else:
                    location_x = int(key[key.index("-") + 1:index])
                    location_y = int(key[len("keyword"):key.index("-")])
            if "-data" in key or key in INPUT_TYPE:
                item_type = "input"
            rule_keys.append(SnortRuleViewArray(snortId=self.instance,
                               typeOfItem=item_type,
                               locationX=location_x,
                               locationY=location_y,
                               value=value,
                               htmlId=key))
        if not self.errors:
            cache.set(self.instance.id, rule_keys)
            for key in rule_keys:
                key.save()
        else:
            cache.set(self.instance.id, rule_keys)
            return
        if self.cleaned_data.get("active"):
            save_rule_to_s3(self.instance.id, self.instance.content)
            pass
            # todo: save to s3
        else:
            delete_rule_from_s3(self.instance.id)
            # todo: make sure it is not on prod


def validate_pcap_snort(pcaps, rule):
    stdout = b""

    if not rule.location:
        import re
        rule.location = re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '',
                                                      rule.name)
                               .strip()
                               .lower())

    with open(rule.location + ".tmp", "w") as rule_file:
        rule_file.write(rule.content)
    failed = True
    for pcap in pcaps:
        try:
            if not verify_legal_pcap("/app/{pcap.pcap_file}"):
                raise Exception(f"illegal pcap file")
            if not os.path.exists(f"/app/{pcap.pcap_file}"):
                raise Exception(f"cant find file /app/{pcap.pcap_file}")
            stdout, stderr = subprocess.Popen(
                ["/home/snorty/snort3/bin/snort", "-R", rule.location + ".tmp", "-r", f"/app/{pcap.pcap_file}", "-A",
                 "fast"], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).communicate()
            if stdout and not stderr:
                if b"total_alerts: " in stdout:
                    return stdout.split(b"total_alerts: ")[1].split(b"\n")[0]
                else:
                    return 0
        except Exception as e:
            raise forms.ValidationError(f"could not validate rule on {pcap.pcap_file}: {e}", code=405)
    if failed:
        raise Exception("no rules was chosen")
    return stdout


@admin.register(SnortRule)
class SnortRuleAdmin(DjangoObjectActions, AdminAdvancedFiltersMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = FILTER_FIELDS  # simple list filters

    # specify which fields can be selected in the advanced filter
    # creation form
    advanced_filter_fields = ADVANCE_FILTER_FIELDS
    change_actions = ('clone_rule',)
    # changelist_actions = ('load_template',)
    fields = FIELDS
    filter_horizontal = ('pcap_sanity_check', "pcap_legal_check")
    list_display_links = ("name",)
    list_display = ("id", "user", "active", "name", "group", "description", "content", "date", "is_template")
    search_fields = SEARCH_FIELDS
    form = SnortRuleAdminForm
    actions = ['make_published']

    def export_action(self, request):
        return self.export_data(SnortRule.objects.all())

    @transaction.atomic
    def import_action(self, request):
        errors = False
        if request.method == 'POST':
            snort_rules_to_save = []
            snort_rules_options_to_save = {}
            try:
                csv_file = request.FILES['myfile']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'File is not CSV type')
                    return HttpResponseRedirect("/admin/snort/snortrule/import/")
                # if file is too large, return
                if csv_file.multiple_chunks():
                    messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                    return HttpResponseRedirect("/admin/snort/snortrule/import/")

                file_data = csv.DictReader(StringIO(csv_file.read().decode("utf-8")))
                # loop over the lines and save them in db. If error , store as string and then display
                for item in file_data:
                    snort_rule = SnortRule()
                    snort_rule.active = item["Active"]
                    snort_rule.deleted = item["Deleted"]
                    snort_rule.user = getattr(request.user, request.user.USERNAME_FIELD)
                    snort_rule.description = item["Description"]
                    snort_rule.extra = item["Extra"]
                    if item.get("Group"):
                        snort_rule.group = attackGroup.objects.get(name=item["Group"])
                    snort_rule.name = item["Name"]
                    if item.get("Id"):
                        snort_rule.id = item["Id"]
                    else:
                        temp_id = str(time.time())
                        snort_rule.id = "temp " + temp_id
                    snort_rule.content = item["Rule"]

                    try:
                        resppnse = {"data": []}
                        try:
                            rule_parsed = suricataparser.parse_rule(item["Rule"])
                        except:
                            raise Exception("bad rule format")
                        build_keyword_dict(resppnse, rule_parsed)
                        for item_data in resppnse["data"]:
                            temp_id = snort_rule.id
                            snort_rules_options_to_save[temp_id] = []
                            snort_rules_options_to_save[temp_id].append(SnortRuleViewArray(**item_data))
                        for op in rule_parsed.options:
                            if op.name == "msg":
                                if snort_rule.group:
                                    op.value = snort_rule.group.name + " "
                                else:
                                    op.value = ""
                                if snort_rule.name:
                                    op.value += snort_rule.name
                                continue
                            if op.name == "sid":
                                op.value = snort_rule.id
                                continue
                            if op.name == "metadata":
                                new_value = []
                                user_applyed = False
                                for item_metadata in op.value.data:
                                    if item_metadata.strip("'").strip().startswith("group "):
                                        if snort_rule.group:
                                            new_value.append(f"group {snort_rule.group.name}")
                                            continue
                                    if item_metadata.strip("'").strip().startswith("name "):
                                        new_value.append(f"name {snort_rule.name}")
                                        continue
                                    if item_metadata.strip("'").strip().startswith("description "):
                                        new_value.append(f"description {snort_rule.description}")
                                        continue
                                    if item_metadata.strip("'").strip().startswith("employee "):
                                        new_value.append(f"employee {snort_rule.user}")
                                        user_applyed = False
                                        continue
                                    if item_metadata.strip("'").strip().startswith("document "):
                                        snort_rule.main_ref = item_metadata.strip("'").strip().replace("document ", "")
                                    if item_metadata.strip("'").strip().startswith("treatment "):
                                        snort_rule.request_ref = item_metadata.strip("'").strip().replace("document ", "")
                                    new_value.append(item_metadata)
                                if not user_applyed:
                                    new_value.append(f"employee {snort_rule.user}")
                                op.value.data = new_value
                                continue
                        snort_rule.content = rule_parsed
                        snort_rules_to_save.append(snort_rule)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        errors = True
                        messages.error(request, f"Unable to load rule {item['Name']}. {repr(e)}")
                        pass

            except Exception as e:
                errors = True
                messages.error(request, "Unable to upload file. " + repr(e))
            if not errors:
                for rule in snort_rules_to_save:
                    rule_id = rule.id
                    if rule_id.startswith("temp "):
                        rule.id = None
                        rule_parsed = rule.content
                        for op in rule_parsed.options:
                            if op.name == "sid":
                                op.value = 0
                                break
                        rule.content = ""
                        rule.save()
                        for op in rule_parsed.options:
                            if op.name == "sid":
                                op.value = rule.id
                                break
                    rule.content = rule_parsed.build_rule()
                    rule.save()
                    if rule.active:
                        save_rule_to_s3(rule.id, rule.content)
                    else:
                        delete_rule_from_s3(rule.id)
                    SnortRuleViewArray.objects.filter(snortId=rule.id).delete()
                    for attr in snort_rules_options_to_save[rule_id]:
                        attr.snortId = rule
                        attr.save()
                return HttpResponseRedirect("/admin/snort/snortrule/")
            return HttpResponseRedirect("/admin/snort/snortrule/import/")

        return render(request, 'html/import.html')

    @admin.action(description='export selected snort to csv')
    def make_published(self, request, queryset):
        return self.export_data(queryset)

    def export_data(self, queryset):
        response = HttpResponse(
            content_type='application/force-download')  # mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f"SnortRule-{datetime.now()}.csv")
        str_content = "Active,Date,Deleted,Description,Extra,Group,Name,Id,User,Rule\n"
        for snort_item in queryset:
            content = snort_item.content.replace('"', "'")
            my_list = [snort_item.active, snort_item.date, snort_item.deleted, snort_item.description, snort_item.extra,
                       snort_item.group, snort_item.name, snort_item.pk, snort_item.user, content]
            for item in my_list:
                if isinstance(item, bool):
                    str_content += str(item) + ","
                    continue
                if not item:
                    str_content += ','
                    continue
                str_content += '"' + str(item) + '",'
                continue
            str_content = str_content[:-1] + "\n"
        response.content = smart_str(str_content)
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
        return response

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def snort_builder(self, obj):
        set_rule = cache.get(obj.id)
        if not set_rule:
            set_rule = SnortRuleViewArray.objects.filter(snortId=obj.id)
            cache.set(obj.id, set_rule)
        else:
            cache.set(obj.id, [])
        context = copy.deepcopy(self.context)
        context["build_items"] = set_rule
        snort_buider_section = self.snort_buider_section(context).content.decode("utf-8")
        return mark_safe(self.full_rule_js.content.decode("utf-8") + snort_buider_section)

    def get_form(self, request, *args, **kwargs):
        form = super(SnortRuleAdmin, self).get_form(request, **kwargs)
        form.current_user = request.user
        context = {"actions": keywords.objects.filter(stage="action", avalable="True"),
                   "protocols": keywords.objects.filter(stage="protocol", avalable="True")}
        self.snort_buider_section = partial(render, request, "html/snortBuilder.html")
        self.full_rule_js = render(request, "html/full_rule.html")
        self.context = context
        return form

    @transaction.atomic
    def clone_rule(self, request, obj: SnortRule):
        new_snort = SnortRule.objects.get(pk=obj.id)
        new_snort.pk = None
        new_snort.is_template = False
        new_snort.active = False
        new_snort.deleted = False
        new_snort.user = getattr(request.user, request.user.USERNAME_FIELD)
        new_snort.save()
        for keyword in SnortRuleViewArray.objects.filter(snortId=obj.id):
            keyword.pk = None
            keyword.snortId = new_snort
            keyword.save()

        return HttpResponseRedirect(f"/snort/snortrule/{new_snort.pk}/change")

    clone_rule.label = "clone_rule"  # optional

    def get_readonly_fields(self, request, obj=None):
        if obj and (obj.is_template or obj.admin_locked):
            read_only_fields = (
            "id", "active", 'location', "user", "admin_locked", "snort_builder", "deleted")
        else:
            read_only_fields = ("id", 'location', "user", "admin_locked", "snort_builder", "deleted")

        return read_only_fields

    # readonly_fields = ("id", 'location', "user", "admin_locked", "full_rule", "snort_builder", "deleted")
    clone_rule.short_description = "clone rule to a new rule"  # optional
