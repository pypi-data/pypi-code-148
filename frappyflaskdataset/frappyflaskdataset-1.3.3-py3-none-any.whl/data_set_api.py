import os
import json
from flask import jsonify, abort, request, send_file
from pbu import list_to_json, default_options


class DataTypes:
    TIME_SERIES = "TIME_SERIES"
    IMAGE = "IMAGE"
    JSON = "JSON"
    BINARY = "BINARY"


class _DummyUser:
    def __init__(self, permissions):
        self.email = "anonymous"
        self.permissions = permissions


def _upload_single_file(uploaded_file, target_directory):
    # save file temporarily
    file_path = os.path.join(target_directory, uploaded_file.filename)
    uploaded_file.save(file_path)
    # return path, mime type and dimension
    return file_path, uploaded_file.mimetype


_DEFAULT_OPTIONS = {
    "api_prefix": "/api/data-sets",
    "manage_permission": None,
    "get_permission": None,
    "data_folder": "_data",
    "login_check_function": None,
    "allow_public_binary_access": False,
}


def register_endpoints(app, data_store, options={}):
    effective_options = default_options(_DEFAULT_OPTIONS, options)

    login_check_function = effective_options["login_check_function"]
    data_folder = effective_options["data_folder"]
    manage_permission = effective_options["manage_permission"]
    get_permission = effective_options["get_permission"]
    api_prefix = effective_options["api_prefix"]
    allow_public_binary_access = effective_options["allow_public_binary_access"]

    # init data folder
    if not os.path.isdir(data_folder):
        os.mkdir(data_folder)

    # login check for each endpoint
    def _check_login_state(permission=None):
        if login_check_function is not None:
            return login_check_function(permission)
        return _DummyUser([manage_permission])

    # check / retrieval function for data set meta data
    def _get_data_meta(data_id):
        data = data_store.get_meta(data_id)
        if data is None:
            abort(404)
        return data

    def _get_data(data_id):
        data = data_store.get(data_id)
        if data is None:
            abort(404)
        return data

    # public endpoints

    @app.route(api_prefix, methods=["GET"])
    def get_data_meta_list():
        _check_login_state(get_permission)
        assignment = request.args.get("assignment")
        assignment_type = request.args.get("assignmentType")
        data_type = request.args.get("dataType")

        if assignment is not None and data_type is not None:
            return jsonify(list_to_json(data_store.get_by_assignment_and_type(assignment, data_type)))
        elif assignment is not None and assignment_type is not None:
            return jsonify(list_to_json(data_store.get_by_assignment_type(assignment, assignment_type)))
        elif assignment is not None:
            return jsonify(list_to_json(data_store.get_by_assignment(assignment)))
        elif data_type is not None:
            return jsonify(list_to_json(data_store.get_by_type(data_type)))

        return jsonify(list_to_json(data_store.get_all()))

    @app.route("{}/<data_id>/meta".format(api_prefix), methods=["GET"])
    def get_data_set_meta(data_id):
        _check_login_state(get_permission)
        data = _get_data_meta(data_id)
        return jsonify(data.to_json())

    @app.route("{}/<data_id>".format(api_prefix), methods=["GET"])
    def get_full_data_set(data_id):
        _check_login_state(get_permission)
        data = _get_data(data_id)
        return jsonify(data.to_json())

    @app.route("{}/<data_id>/relations".format(api_prefix), methods=["GET"])
    def get_related_data_sets(data_id):
        _check_login_state(get_permission)
        _ = _get_data(data_id)
        return jsonify(list_to_json(data_store.get_by_relations(data_id)))

    @app.route("{}/<data_id>/binary".format(api_prefix), methods=["GET"])
    def get_data_set_binary(data_id):
        data = _get_data(data_id)
        if allow_public_binary_access is False:
            if data.type not in [DataTypes.BINARY, DataTypes.IMAGE]:
                abort(400)  # wrong data type
            if data.payload.public_flag is False:
                # run regular authentication
                _check_login_state(get_permission)

        return send_file(data.payload.target_file)

    # @DEPRECATED
    @app.route("{}/<data_id>/image".format(api_prefix), methods=["GET"])
    def get_data_set_image_binary(data_id):
        return get_data_set_binary(data_id)

    # manage endpoints

    @app.route(api_prefix, methods=["POST"])
    def create_data_set():
        user = _check_login_state(manage_permission)
        json_body = json.loads(request.form["meta"])
        if "payload" not in json_body:
            json_body["payload"] = {}
        form_data = data_store.object_class.from_json(json_body)
        if user.email is not None:
            form_data.user_id = user.email
        else:
            form_data.user_id = user.username  # local user

        file = request.files["file"]

        if form_data.type == DataTypes.TIME_SERIES:
            # parse CSV
            content = file.read().decode("utf-8")
            lines = content.replace("/\r/g", "\n").split("\n")
            for line in lines[1:]:
                if line == "":
                    # skip empty lines
                    continue

                cols = line.split(",")
                # attempt to parse floats and ints
                parsed_cols = []
                for col_content in cols:
                    try:
                        if "." in col_content:
                            parsed_value = float(col_content)
                        else:
                            parsed_value = int(col_content)
                        parsed_cols.append(parsed_value)
                    except ValueError:
                        # not a number
                        parsed_cols.append(col_content)
                # add the parsed columns
                form_data.payload.data.append(parsed_cols)
        elif form_data.type in [DataTypes.IMAGE, DataTypes.BINARY]:
            # handle uploaded image
            final_path, mime_type = _upload_single_file(file, data_folder)
            form_data.payload.target_file = final_path
            form_data.payload.mime_type = mime_type
        elif form_data.type == DataTypes.JSON:
            # handle JSON file
            content = json.loads(file.read().decode("utf-8"))
            form_data.payload.data = content

        data_id = data_store.create(form_data.to_json())

        # post handling for images and binary
        if form_data.type in [DataTypes.IMAGE, DataTypes.BINARY]:
            ds = data_store.get(data_id)
            final_path = os.path.join(data_folder, "{}.{}".format(ds.id,
                                                                  ds.payload.target_file.split(".")[-1].lower()))
            # move file to final destination
            os.rename(ds.payload.target_file, final_path)
            # update data set
            ds.payload.target_file = final_path
            data_store.update_full(ds)

        data = data_store.get_meta(data_id)
        return jsonify(data.to_json())

    @app.route("{}/<data_id>".format(api_prefix), methods=["POST"])
    def update_data_meta(data_id):
        _check_login_state(manage_permission)
        body = request.get_json()
        _ = _get_data_meta(data_id)
        data_store.update_meta(data_id, body)
        return jsonify(data_store.get_meta(data_id).to_json())

    @app.route("{}/<data_id>".format(api_prefix), methods=["DELETE"])
    def delete_data_set(data_id):
        _check_login_state(manage_permission)
        data = _get_data(data_id)

        if data.type in [DataTypes.IMAGE, DataTypes.BINARY]:
            # first delete local file
            if data.payload.target_file is not None and os.path.exists(data.payload.target_file):
                os.unlink(data.payload.target_file)

        data_store.delete(data_id)
        return jsonify({"status": True})
