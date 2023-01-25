from django.urls import path, register_converter

from . import views

app_name = 'spa'


class SPAFilenameConverter:
    regex = r'[-\w.]+\.(?:json|jpe?g|png|txt|ico|js|map)'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(SPAFilenameConverter, 'spa_filename')

urlpatterns = [
    path('static/<path:resource>', views.redirect_static),  # Serve SPA static files using django staticfiles
    path('<spa_filename:filename>', views.serve_file),  # Serve other SPA file like manifest.json
    # Serve SPA paths from the index.html entrypoint.
    path('<path:path>/', views.serve_file, {'filename': 'index.html'}, name='path'),
    # Serve SPA home from the index.html entrypoint.
    path('', views.serve_file, {'filename': 'index.html'}, name='home'),
]
