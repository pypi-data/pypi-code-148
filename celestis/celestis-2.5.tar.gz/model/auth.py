import jwt
import datetime

def gen_token(secret, email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return token

