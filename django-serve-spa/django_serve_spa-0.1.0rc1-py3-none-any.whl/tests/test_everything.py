import pytest
from django.http import Http404
from django.urls import resolve

from example import settings
from serve_spa import views, utils


@pytest.fixture  # (params=['', 'app/'])
def spa_path(request):
    # settings.SPA_URL = request.param
    # django.setup()
    return settings.SPA_URL


def test_serve_file_view(rf, spa_path):
    from serve_spa import settings as app_settings

    request = rf.get(f'/{spa_path}home')
    response = views.serve_file(request, filename='index.html')
    assert response.status_code == 200
    assert list(response.streaming_content)[0] == (app_settings.SPA_ROOT / 'index.html').read_bytes()


def test_redirect_static_view(rf, spa_path):
    request = rf.get(f'/{spa_path}static/js/main.f9d654a7.js')
    response = views.redirect_static(request, resource='main.f9d654a7.js')
    assert response.status_code == 302
    assert response.url == f'/static/main.f9d654a7.js'


def test_urls(rf, spa_path):
    assert resolve(f'/{spa_path}static/main.f9d654a7.js').func == views.redirect_static
    assert resolve(f'/{spa_path}favicon.ico').func == views.serve_file
    assert resolve(f'/{spa_path}').func == views.serve_file
    assert resolve(f'/{spa_path}path/').func == views.serve_file
    with pytest.raises(Http404):
        request = rf.get(f'/{spa_path}not-found.ico')
        resolver = resolve(f'/{spa_path}not-found.ico')
        resolver.func(request, **resolver.kwargs)


def test_get_dont_match_prefix_regex():
    assert utils.get_dont_match_prefix_regex(['abc', 'def'], 'ghi') == '^(?!abc|def)^ghi'
    assert utils.get_dont_match_prefix_regex(['abc', 'def']) == '^(?!abc|def)'
