"""IndieAuth client."""

import indieauth
import web
import webagt
from web import tx

app = web.application(
    __name__,
    prefix="guests",
    model={
        "guests": {
            "url": "TEXT",
            "name": "TEXT",
            "email": "TEXT",
            "access_token": "TEXT",
            "account_created": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        }
    },
)


@app.control("")
class Guests:
    """Site guests."""

    def get(self):
        """Return a list of guests to owner, the current user or a sign-in page."""
        if not tx.user.session:
            return app.view.signin(tx.host.name)
        if tx.user.is_owner:
            return app.view.guests(app.model.get_guests())
        return tx.user.session  # a guest is signed in; show other guests


@app.control("sign-in")
class SignIn:
    """IndieAuth client sign in."""

    def get(self):
        """Initiate a sign-in."""
        if tx.user.session:
            raise web.SeeOther("/guests")
        form = web.form("me", return_to="/")
        tx.user.session["return_to"] = form.return_to
        raise web.SeeOther(
            indieauth.initiate_signin(
                tx.origin,
                "guests/authorize",
                form.me,
                ["profile", "email"],
                tx.user.session,
            )
        )


@app.control("authorize")
class Authorize:
    """IndieAuth client authorization redirect URL."""

    def get(self):
        """Complete the authorization using a 'profile' flow."""
        # TODO Complete a sign-in by requesting a token.
        # XXX TODO if tx.user.session:
        # XXX TODO     raise web.SeeOther("/guests")
        form = web.form("state", "code")
        response = indieauth.redeem_code(form.state, form.code, tx.user.session)
        app.model.create_guest(response)
        raise web.SeeOther(tx.user.session["return_to"])


@app.control("sign-out")
class SignOut:
    """IndieAuth client sign out."""

    def get(self):
        """Return a sign-out form."""
        if not tx.user.session:
            raise web.SeeOther("/sign-in")
        return app.view.signout()

    def post(self):
        """Sign the guest out. Revoke any tokens."""
        if not tx.user.session:
            raise web.SeeOther("/sign-in")
        form = web.form(return_to="")
        try:
            guest_url = tx.user.session["uid"][0]
        except KeyError:
            pass
        else:
            access_token = app.model.get_guest(guest_url)["access_token"]
            web.post(
                tx.user.session["token_endpoint"],
                data={"action": "revoke", "token": access_token},
            )
        tx.user.session = None
        raise web.SeeOther(f"/{form.return_to}")


@app.query
def create_guest(db, response):
    """Add a user based upon given response."""
    profile = response.get("profile", {})
    db.insert(
        "guests",
        url=response["me"],
        name=profile.get("name"),
        email=profile.get("email"),
        access_token=response.get("access_token"),
    )


@app.query
def get_guests(db):
    """Return a list of guests."""
    return db.select("guests")


@app.query
def get_guest(db, user: webagt.uri):
    """Return a user."""
    return db.select("guests", where="url = ?", vals=[user])[0]


# @model.migrate(1)
# def change_name(db):
#     """Rename `url` to `me` to reuse language from the spec."""
#     db.rename_column("guests", "url", "me")
