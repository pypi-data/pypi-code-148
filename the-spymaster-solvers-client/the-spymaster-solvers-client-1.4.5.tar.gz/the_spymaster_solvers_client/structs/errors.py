from the_spymaster_util.http.errors import ApiError


class SpymasterSolversError(ApiError):
    pass


SERVICE_ERRORS = frozenset({SpymasterSolversError})
