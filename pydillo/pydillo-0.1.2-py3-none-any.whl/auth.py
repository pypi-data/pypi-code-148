from ctypes import c_void_p, c_char_p
from ctypes import c_int, c_uint, c_int64, c_bool

from .lib import lib

DILLO_AUTH_TYPE_NONE = 0
DILLO_AUTH_TYPE_TOKEN = 1
DILLO_AUTH_TYPE_ACTION = 2
DILLO_AUTH_TYPE_ROLE = 3
DILLO_AUTH_TYPE_SERVICE = 4
DILLO_AUTH_TYPE_PERMISSIONS = 5
DILLO_AUTH_TYPE_MULTIPLE = 6
DILLO_AUTH_TYPE_COMPLETE = 7

DILLO_AUTH_SCOPE_NONE = 0
DILLO_AUTH_SCOPE_SINGLE = 1
DILLO_AUTH_SCOPE_MANAGEMENT = 2

dillo_auth_type_to_string = lib.dillo_auth_type_to_string
dillo_auth_type_to_string.argtypes = [c_int]
dillo_auth_type_to_string.restype = c_char_p

dillo_auth_scope_to_string = lib.dillo_auth_scope_to_string
dillo_auth_scope_to_string.argtypes = [c_int]
dillo_auth_scope_to_string.restype = c_char_p

dillo_auth_delete = lib.dillo_auth_delete
dillo_auth_delete.argtypes = [c_void_p]

dillo_auth_get_type = lib.dillo_auth_get_type
dillo_auth_get_type.argtypes = [c_void_p]
dillo_auth_get_type.restype = c_int

dillo_auth_get_scope = lib.dillo_auth_get_scope
dillo_auth_get_scope.argtypes = [c_void_p]
dillo_auth_get_scope.restype = c_int

dillo_auth_get_admin = lib.dillo_auth_get_admin
dillo_auth_get_admin.argtypes = [c_void_p]
dillo_auth_get_admin.restype = c_bool

dillo_auth_get_token_id = lib.dillo_auth_get_token_id
dillo_auth_get_token_id.argtypes = [c_void_p]
dillo_auth_get_token_id.restype = c_char_p

dillo_auth_get_token_type = lib.dillo_auth_get_token_type
dillo_auth_get_token_type.argtypes = [c_void_p]
dillo_auth_get_token_type.restype = c_int

dillo_auth_get_token_organization = lib.dillo_auth_get_token_organization
dillo_auth_get_token_organization.argtypes = [c_void_p]
dillo_auth_get_token_organization.restype = c_char_p

dillo_auth_get_token_permissions = lib.dillo_auth_get_token_permissions
dillo_auth_get_token_permissions.argtypes = [c_void_p]
dillo_auth_get_token_permissions.restype = c_char_p

dillo_auth_get_token_role = lib.dillo_auth_get_token_role
dillo_auth_get_token_role.argtypes = [c_void_p]
dillo_auth_get_token_role.restype = c_char_p

dillo_auth_get_token_user = lib.dillo_auth_get_token_user
dillo_auth_get_token_user.argtypes = [c_void_p]
dillo_auth_get_token_user.restype = c_char_p

dillo_auth_get_token_username = lib.dillo_auth_get_token_username
dillo_auth_get_token_username.argtypes = [c_void_p]
dillo_auth_get_token_username.restype = c_char_p

dillo_auth_get_mask = lib.dillo_auth_get_mask
dillo_auth_get_mask.argtypes = [c_void_p]
dillo_auth_get_mask.restype = c_int64

dillo_auth_create = lib.dillo_auth_create
dillo_auth_create.argtypes = [c_int]
dillo_auth_create.restype = c_void_p

dillo_auth_print_token = lib.dillo_auth_print_token
dillo_auth_print_token.argtypes = [c_void_p]

dillo_custom_authentication_handler = lib.dillo_custom_authentication_handler
dillo_custom_authentication_handler.argtypes = [c_void_p, c_void_p]
dillo_custom_authentication_handler.restype = c_uint
