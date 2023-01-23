from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # if request.path == '/dash/dash/convertedfile/add/' and request.user.is_anonymous:
        #     user = User.objects.get(username="anonymous")
        #     if not user:
        #         user = User.objects.create_user("anonymous", is_staff=True)
        #         user.groups.add(2)
        #     request.user = user

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_exception(self, request, exception):
    #     # Get the exception info now, in case another exception is thrown later.
    #     if isinstance(exception, Http404):
    #         return HttpResponseRedirect("/dash")
    #     else:
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dash'))
