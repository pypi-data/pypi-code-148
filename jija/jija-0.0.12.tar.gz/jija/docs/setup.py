import os
from jija import config
from aiohttp_swagger import setup_swagger, _swagger_home, _swagger_def
import aiohttp_swagger
from . import views
from aiohttp import web


class DocsSetup:
    def __init__(self, aiohttp_app):
        self.__aiohttp_app = aiohttp_app

    def setup(self):


        # setup_swagger(aiohttp_app, swagger_url=cls.URL, ui_version=3)

        STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(aiohttp_swagger.__file__), "swagger_ui3"))

        # self.__aiohttp_app.router.
        # self.__aiohttp_app.router.add_route('GET', "/ping", ping)

        self.__aiohttp_app.router.add_route('GET', f'{config.DocsConfig.URL}/', _swagger_home)
        # aiohttp_app.router.add_route('GET', "{}/".format(_base_swagger_url), _swagger_home_func)
        # def aa(re):
        #     return web.json_response({})
        self.__aiohttp_app.router.add_route(
            'GET', f"{config.DocsConfig.URL.rstrip('/')}/swagger.json", views.swagger_view)
        # self.__aiohttp_app.router.add_route('GET', _swagger_def_url, _swagger_def_func)

        static_route = f'{config.DocsConfig.URL}/swagger_static'

        self.__aiohttp_app.router.add_static(static_route, STATIC_PATH)


        self.__aiohttp_app["SWAGGER_DEF_CONTENT"] = 'asdasd'
        self.__set_template()
        return self.__aiohttp_app

    def __set_template(self):
        STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(aiohttp_swagger.__file__), "swagger_ui3"))
        static_route = f'{config.DocsConfig.URL}/swagger_static'

        with open(os.path.join(STATIC_PATH, "index.html"), "r") as file:
            index_html = file.read()

        self.__aiohttp_app["SWAGGER_TEMPLATE_CONTENT"] = (
            index_html
            .replace("##SWAGGER_CONFIG##", f"{config.DocsConfig.URL.rstrip('/')}/swagger.json")
            .replace("##STATIC_PATH##", f"{static_route}")
            .replace("##SWAGGER_VALIDATOR_URL##", "")
        )

    def setup_swagger(self):
    # , app: web.Application,
    #                   *,
    #                   swagger_from_file: str = None,
    #                   swagger_url: str = "/api/doc",
    #                   api_base_url: str = "/",
    #                   swagger_validator_url: str = "",
    #                   description: str = "Swagger API definition",
    #                   api_version: str = "1.0.0",
    #                   ui_version: int = None,
    #                   title: str = "Swagger API",
    #                   contact: str = "",
    #                   swagger_home_decor: FunctionType = None,
    #                   swagger_def_decor: FunctionType = None,
    #                   swagger_info: dict = None,
    #                   swagger_template_path: str = None,
    #                   definitions: dict = None,
    #                   security_definitions: dict = None):
    #     _swagger_url = ("/{}".format(swagger_url)
    #                     if not swagger_url.startswith("/")
    #                     else swagger_url)
    #     _base_swagger_url = _swagger_url.rstrip('/')
    #     _swagger_def_url = '{}/swagger.json'.format(_base_swagger_url)
    #
    #     if ui_version == 3:
    #         STATIC_PATH = abspath(join(dirname(__file__), "swagger_ui3"))
    #     else:
    #         STATIC_PATH = abspath(join(dirname(__file__), "swagger_ui"))
    #
    #     # Build Swagget Info
    #     if swagger_info is None:
    #         if swagger_from_file:
    #             swagger_info = load_doc_from_yaml_file(swagger_from_file)
    #         else:
    #             swagger_info = generate_doc_from_each_end_point(
    #                 app, ui_version=ui_version,
    #                 api_base_url=api_base_url, description=description,
    #                 api_version=api_version, title=title, contact=contact,
    #                 template_path=swagger_template_path,
    #                 definitions=definitions,
    #                 security_definitions=security_definitions
    #             )
    #     else:
    #         swagger_info = json.dumps(swagger_info)
    #
    #     _swagger_home_func = _swagger_home
    #     _swagger_def_func = _swagger_def
    #
    #     if swagger_home_decor is not None:
    #         _swagger_home_func = swagger_home_decor(_swagger_home)
    #
    #     if swagger_def_decor is not None:
    #         _swagger_def_func = swagger_def_decor(_swagger_def)
    #
    #     # Add API routes
    #     app.router.add_route('GET', _swagger_url, _swagger_home_func)
    #     app.router.add_route('GET', "{}/".format(_base_swagger_url),
    #                          _swagger_home_func)
    #     app.router.add_route('GET', _swagger_def_url, _swagger_def_func)
    #
    #     # Set statics
    #     statics_path = '{}/swagger_static'.format(_base_swagger_url)
    #     app.router.add_static(statics_path, STATIC_PATH)
    #
    #     # --------------------------------------------------------------------------
    #     # Build templates
    #     # --------------------------------------------------------------------------

        self.__aiohttp_app["SWAGGER_DEF_CONTENT"] = swagger_info
    #     with open(join(STATIC_PATH, "index.html"), "r") as f:
    #         app["SWAGGER_TEMPLATE_CONTENT"] = (
    #             f.read()
    #             .replace("##SWAGGER_CONFIG##", '{}{}'.
    #                      format(api_base_url.rstrip('/'), _swagger_def_url))
    #             .replace("##STATIC_PATH##", '{}{}'.
    #                      format(api_base_url.rstrip('/'), statics_path))
    #             .replace("##SWAGGER_VALIDATOR_URL##", swagger_validator_url)
    #         )
    #
