

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect

def rate_limit(num_requests: int, time_minutes: int, redirect_url: str=None):
    """
        Decorator to limit the number of requests a user can make to a specific view within a given time frame.
            When the limit is reached, the user will be redirected to the specified redirect_url.

        :param num_requests: The number of requests allowed within the time frame.
        :type num_requests: int
        :param time_frame: The time frame, in seconds, in which the number of requests is limited.
        :type time_frame: int
        :param redirect_url: The URL to redirect the user to when the limit is reached.
        :type redirect_url: str
        :return: The decorated view function.
        :rtype: function
    """
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            ip_address = request.META['REMOTE_ADDR']
            requests = cache.get(ip_address)
            if requests:
                if requests >= num_requests:
                    if redirect_url:
                        return redirect(redirect_url)
                    else:

                        return HttpResponse("You have been rate limited.")
                else:
                    cache.set(ip_address, requests+1, time_minutes*60)
            else:
                cache.set(ip_address, 1, time_minutes*60)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
