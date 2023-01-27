"""IndieAuth server."""

import easyuri
import indieauth
import web
from web import tx

__all__ = ["app"]

app = web.application(
    __name__,
    prefix="auth",
    args={
        "client_id": r"[\w/.]+",
    },
    model={
        "auths": {
            "auth_id": "TEXT",
            "initiated": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "revoked": "DATETIME",
            "code": "TEXT",
            "client_id": "TEXT",
            "client_name": "TEXT",
            "code_challenge": "TEXT",
            "code_challenge_method": "TEXT",
            "redirect_uri": "TEXT",
            "response": "JSON",
            "token": "TEXT",
        },
    },
)

supported_scopes = (
    "create",
    "draft",
    "update",
    "delete",
    "media",
    "profile",
    "email",
)


@app.wrap
def linkify_head(handler, main_app):
    """Ensure server links are reference from homepage."""
    yield
    if tx.request.uri.path == "":
        web.add_rel_links(
            authorization_endpoint="/auth",
            token_endpoint="/auth/tokens",
            **{"indieauth-metadata": "/auth/metadata"},
        )


def redeem_authorization_code(flow: str) -> dict:
    request = web.form(
        "code",
        "client_id",
        "redirect_uri",
        grant_type="authorization_code",
        code_verifier=None,
        code_challenge=None,
    )
    # TODO verify authenticity
    # TODO grant_type=refresh_token
    auth = app.model.get_auth_from_code(request.code)
    owner = {
        "url": tx.origin,
        "name": tx.host.owner["name"][0],
        "email": tx.host.owner.get("email", [None])[0],
        "photo": tx.host.owner.get("photo", [None])[0],
    }
    try:
        response = indieauth.validate_redemption(request, auth, owner, flow)
    except indieauth.AuthorizationError as err:
        raise web.Forbidden(err)
    app.model.update_auth(response, auth["code"])
    web.header("Content-Type", "application/json")
    return response


@app.control("")
class AuthorizationEndpoint:
    """Identity and resource authorization."""

    owner_only = ["get"]

    def get(self):
        """Return a consent screen for a third-party site sign-in."""
        try:
            form = web.form(
                "client_id", "redirect_uri", "state", response_type="code", scope=""
            )
        except web.BadRequest:
            return app.view.authorizations(
                app.model.get_clients(),
                app.model.get_active(),
                app.model.get_revoked(),
            )
        if form.response_type not in ("code", "id"):  # NOTE `id` for backcompat
            raise web.BadRequest('`response_type` must be "code".')
        client = indieauth.discover_client(form.client_id)
        tx.user.session.update(
            client_id=form.client_id,
            client_name=client["name"],
            redirect_uri=form.redirect_uri,
            state=form.state,
        )
        if "code_challenge" in form and "code_challenge_method" in form:
            tx.user.session.update(
                code_challenge=form.code_challenge,
                code_challenge_method=form.code_challenge_method,
            )
        return app.view.consent(client, form.scope.split(), supported_scopes)

    def post(self):
        """Handle "Profile URL" flow response."""
        return redeem_authorization_code("profile")


@app.control("consent")
class AuthorizationConsent:
    """The authorization consent screen."""

    owner_only = ["post"]

    def post(self):
        """
        Handle consent screen action.

        Complete the authorization and redirect to client's `redirect_uri`.

        """
        form = web.form("action", scopes=[])
        if form.action == "cancel":
            raise web.SeeOther(tx.user.session["redirect_uri"])
        code = app.model.create_auth(form.scopes, **tx.user.session)
        redirect_uri = indieauth.complete_signin(
            tx.user.session["redirect_uri"], tx.user.session["state"], code, tx.origin
        )
        raise web.Found(redirect_uri)


@app.control("tokens")
class TokenEndpoint:
    """Your token endpoint."""

    owner_only = ["get"]

    def get(self):
        """Return a list of tokens to owner otherwise a form to submit a code."""
        # TODO move to library?
        try:
            auth = app.model.get_auth_from_token(
                str(tx.request.headers["authorization"])
            )
        except IndexError:
            raise web.Forbidden("token could not be found")
        web.header("Content-Type", "application/json")
        return {
            "me": auth["response"]["me"],
            "client_id": auth["client_id"],
            "scope": " ".join(auth["response"]["scope"]),
        }

    def post(self):
        """Handle "Access Token" flow response or revoke an existing access token."""
        # TODO token introspection
        # TODO token verification
        try:
            form = web.form("action", "token")
        except web.BadRequest:
            form = web.form("grant_type")
            if form.grant_type == "personal_access":
                token = app.model.generate_local_token("/auth", "webint_auth", "create")
                return {"access_token": token}
            elif form.grant_type == "device_code":
                return {"access_token": "secret-token:wlkerjwlekrj"}
            elif form.grant_type == "authorization_code":
                return redeem_authorization_code("token")
        if form.action == "revoke":  # TODO XXX
            app.model.revoke_token(form.token)
            raise web.OK("revoked")


# @app.control("introspection")
# class IntrospectionEndpoint:
#     """Your introspection endpoint."""
#
#     def get(self):
#         """Return a list of tickets to owner otherwise a form to submit a ticket."""
#         return "y"


@app.control("devices")
class DeviceEndpoint:
    """Your device endpoint."""

    owner_only = ["get"]

    def get(self):
        """Return a list of tickets to owner otherwise a form to submit a ticket."""

    def post(self):
        web.form("client_id")
        return {
            "device_code": "NGU5OWFiNjQ5YmQwNGY3YTdmZTEyNzQ3YzQ1YSA",
            "user_code": "BDWP-HQPK",
            "verification_uri": f"{tx.origin}/auth/devices",
            "interval": 2,
            "expires_in": 1800,
        }


@app.control("tickets")
class TicketEndpoint:
    """Your ticket endpoint."""

    owner_only = ["get"]

    def get(self):
        """Return a list of tickets to owner otherwise a form to submit a ticket."""


@app.control("clients")
class Clients:
    """Third-party clients you've used."""

    owner_only = ["get"]

    def get(self):
        """Return a list of clients."""
        return app.view.clients(app.model.get_clients())


@app.control("clients/{client_id}")
class Client:
    """A third-party client."""

    owner_only = ["get"]

    def get(self, client_id):
        """Return given client's authorizations."""
        return app.view.client(app.model.get_client_auths(client_id))


@app.control("metadata")
class MetadataEndpoint:
    """Identity and resource authorization."""

    def get(self):
        """Return a consent screen for a third-party site sign-in."""
        return {
            "issuer": web.tx.origin,
            "authorization_endpoint": f"{web.tx.origin}/auth",
            "token_endpoint": f"{web.tx.origin}/auth/tokens",
            "device_endpoint": f"{web.tx.origin}/auth/devices",
            "ticket_endpoint": f"{web.tx.origin}/auth/tickets",
            "code_challenge_methods_supported": ["S256"],
        }


@app.query
def get_clients(db):
    """Return a unique list of clients."""
    return db.select(
        "auths", order="client_name ASC", what="DISTINCT client_id, client_name"
    )


@app.query
def create_auth(
    db,
    scopes: list,
    code_challenge: str = None,
    code_challenge_method: str = None,
    client_id: str = None,
    client_name: str = None,
    redirect_uri: str = None,
    **_,
):
    """Create an authorization."""
    code = web.nbrandom(32)
    while True:
        try:
            db.insert(
                "auths",
                auth_id=web.nbrandom(4),
                code=code,
                code_challenge=code_challenge,
                code_challenge_method=code_challenge_method,
                client_id=client_id,
                client_name=client_name,
                redirect_uri=redirect_uri,
                response={"scope": scopes},
            )
        except db.IntegrityError:
            continue
        break
    return code


@app.query
def generate_local_token(db, client_id: str, client_name: str, scope: str):
    """"""
    code = app.model.create_auth(scope, client_id=client_id, client_name=client_name)
    response = indieauth._generate_token(app.model.get_auth_from_code(code)["response"])
    app.model.update_auth(response, code)
    return response["access_token"]


@app.query
def get_auth_from_code(db, code: str):
    """Return authorization with given `code`."""
    return db.select("auths", where="code = ?", vals=[code])[0]


@app.query
def get_auth_from_token(db, token: str):
    """Return authorization with given `token`."""
    return db.select(
        "auths",
        where="json_extract(auths.response, '$.access_token') = ?",
        vals=[token],
    )[0]


@app.query
def update_auth(db, response: dict, code: str):
    """Update `response` of authorization with given `code`."""
    db.update("auths", response=response, where="code = ?", vals=[code])


@app.query
def get_client_auths(db, client_id: easyuri.URI):
    """Return all authorizations for given `client_id`."""
    return db.select(
        "auths",
        where="client_id = ?",
        vals=[f"https://{client_id}"],
        order="redirect_uri, initiated DESC",
    )


@app.query
def get_active(db):
    """Return all active authorizations."""
    return db.select("auths", where="revoked is null")


@app.query
def get_revoked(db):
    """Return all revoked authorizations."""
    return db.select("auths", where="revoked not null")


@app.query
def revoke_token(db, token: str):
    """Revoke authorization with given `token`."""
    db.update(
        "auths",
        revoked=web.utcnow(),
        where="json_extract(response, '$.access_token') = ?",
        vals=[token],
    )
