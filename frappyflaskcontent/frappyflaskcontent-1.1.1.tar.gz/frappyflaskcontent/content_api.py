from flask import abort, jsonify, request
from pbu import list_to_json, default_options, JSON


class _DummyUser:
    def __init__(self, permissions):
        self.email = "anonymous"
        self.permissions = permissions


_DEFAULT_OPTIONS = {
    "api_prefix": "/api/content",
    "manage_permission": None,
    "get_permission": None,
    "login_check_function": None,
    "allow_get_without_auth": True
}


def register_endpoints(app, content_store, options={}):
    final_options = default_options(_DEFAULT_OPTIONS, options)

    api_prefix = final_options["api_prefix"]
    get_permission = final_options["get_permission"]
    manage_permission = final_options["manage_permission"]
    login_check_function = final_options["login_check_function"]
    allow_get = final_options["allow_get_without_auth"]

    # login check for each endpoint
    def _check_login_state(permission=None):
        if login_check_function is not None:
            return login_check_function(permission)
        return _DummyUser([manage_permission])

    # check / retrieval function for data set meta data
    def _get_content(content_id):
        content = content_store.get(content_id)
        if content is None:
            abort(404)
        return content

    # get endpoints

    @app.route(api_prefix, methods=["GET"])
    def get_content_list():
        if not allow_get:
            _check_login_state(get_permission)
        references = request.args.get("references")
        content_type = request.args.get("contentType")
        if references is not None:
            if content_type is not None:
                return jsonify(list_to_json(content_store.find_by_reference_and_content_type(references, content_type)))
            else:
                return jsonify(list_to_json(content_store.find_by_reference(references)))
        elif content_type is not None:
            return jsonify(list_to_json(content_store.find_by_content_type(content_type)))
        # no filter, return all
        return jsonify(list_to_json(content_store.get_all()))

    @app.route("{}/<content_id>".format(api_prefix), methods=["GET"])
    def get_content(content_id):
        if not allow_get:
            _check_login_state(get_permission)
        content = _get_content(content_id)
        return jsonify(content.to_json())

    # manage endpoints

    @app.route(api_prefix, methods=["POST"])
    def create_content():
        _check_login_state(manage_permission)
        body = request.get_json()
        new_content = content_store.object_class.from_json(body)
        content_id = content_store.create(new_content)
        return jsonify(content_store.get(content_id).to_json())

    @app.route("{}/<content_id>".format(api_prefix), methods=["POST"])
    def update_content(content_id):
        _check_login_state(manage_permission)
        _ = _get_content(content_id)
        body = JSON(request.get_json())
        content_store.update_content(content_id, body.label, body.references, body.content)
        return jsonify(content_store.get(content_id).to_json())

    @app.route("{}/<content_id>".format(api_prefix), methods=["DELETE"])
    def delete_content(content_id):
        _check_login_state(manage_permission)
        _ = _get_content(content_id)
        content_store.delete(content_id)
        return jsonify({
            "contentId": content_id,
            "deleted": True,
        })
