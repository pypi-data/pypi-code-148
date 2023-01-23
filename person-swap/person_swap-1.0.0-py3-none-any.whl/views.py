import logging
import os

import django
from django.http import HttpResponseRedirect

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms.forms import RegisterForm

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.is_staff = True
            form.instance.is_active = False  # TODO remove after demonstration if that is going to be deployed
            form.instance.save()
            Group.objects.get(id=1).user_set.add(form.instance)
            return redirect("/dash", permanent=True)
        else:
            logger.warning(f"Registration failed. Data: {request.POST}")
            logger.warning(f"Registration failed: {form.errors}")
    else:
        form = RegisterForm()

    return render(request, "admin/register.html", {"form": form})


def handle404(request, exception):
    return HttpResponseRedirect("/dash")


def handle500(request):
    return render(request, '500.html', status=500)
