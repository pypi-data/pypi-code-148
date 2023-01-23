from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def security_txt(request):
    """
    securit.tyt

    ---

    add to the path
    path(".well-known/security.txt", core_views.security_txt),
    """
    lines = [
        "Contact: mailto:security@talk-point.de",
        "Expires: 2023-04-25T22:00:00.000Z",
        "Preferred-Languages: de, en"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
