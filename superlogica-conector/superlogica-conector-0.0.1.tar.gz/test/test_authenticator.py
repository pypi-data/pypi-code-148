from superlogica.auth.authenticator import Authenticator


class TestAuth:
    def test_authenticator_parameters(self):
        apk = "api.test"
        token = "teste"
        expiration = 999

        resultado = Authenticator(apk, token, expiration)

        assert apk == resultado.api_key
