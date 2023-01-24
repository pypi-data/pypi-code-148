"""
Old GUI HTTP views.
"""

import functools
from urllib.parse import urlencode

import aiohttp_jinja2
from aiohttp_session import STORAGE_KEY
from aiohttp import web

from .services import HTTPLoginService, HTTPSessionService

__all__ = ('auth_required', 'LoginView', 'LogoutView')


def auth_required(method):
    """Auth decorator for custom views."""

    @functools.wraps(method)
    async def wrapper(view, *args, **kwargs):

        storage = view.request.get(STORAGE_KEY)
        redirect = view.request.path
        q = urlencode({'redirect': redirect})
        login_path = f'/login?{q}'

        if storage is None:
            return web.HTTPFound(login_path)
        else:
            session = await storage.load_session(view.request)
            if not session or session['user_id'] is None:
                return web.HTTPFound(login_path)

            view.request.session = session

        return await method(view, *args, **kwargs)

    return wrapper


class LoginView(web.View):

    login_service_name = HTTPLoginService.service_name
    session_service_name = HTTPSessionService.service_name
    form_template = 'auth/login.html'
    route_name = 'login'

    @aiohttp_jinja2.template(form_template)
    async def get(self):

        session_service = self.request.app.services[self.session_service_name]
        session = await session_service.load_session(self.request)

        if session and session['user_id']:
            home_page = self.request.app.router['index'].url_for()
            return web.HTTPFound(home_page)

        return {
            "header_settings": {
                "current_page": "login"
            },
            "login": "",
            "password": "",
            "form_errors": {}
        }

    @aiohttp_jinja2.template(form_template)
    async def post(self):
        form_data = await self.request.post()
        password = form_data.get("password")
        username = form_data.get("login")
        login_service = self.request.app.services[self.login_service_name]
        await login_service.login(self.request, username=username, password=password)
        redirect = self.request.query.get("redirect", "")
        q = urlencode({'redirect': redirect}) if redirect else ""
        location = self.request.app.router['index'].url_for()
        return web.HTTPFound(f'{location}?{q}')


class LogoutView(web.View):

    login_service_name = HTTPLoginService.service_name
    form_template = 'auth/logout.html'
    route_name = 'logout'

    @aiohttp_jinja2.template(form_template)
    async def get(self):
        login_service = self.request.app.services[self.login_service_name]
        await login_service.logout(self.request)
        login = self.request.app.router[LoginView.route_name].url_for()
        return web.HTTPFound(login)
