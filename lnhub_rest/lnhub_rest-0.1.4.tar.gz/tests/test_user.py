from lnhub_rest.main import client
from lnhub_rest.routers.user import get_profile


def test_get_profile():
    user_profile_expected = {
        "id": "29cff183-c34d-445f-b6cf-31fb3b566158",
        "lnid": "DzTjkKse",
        "handle": "testuser1",
        "name": "Test User1",
        "bio": "Test user at Lamin",
        "website": None,
        "github_handle": None,
        "twitter_handle": None,
        "linkedin_handle": None,
        "created_at": "2022-10-07T16:39:58.68071",
        "updated_at": None,
        "user_id": "29cff183-c34d-445f-b6cf-31fb3b566158",
        "profile_picture_url": None,
    }

    user_profile_from_function = get_profile("29cff183-c34d-445f-b6cf-31fb3b566158")
    assert str(user_profile_from_function) == str(user_profile_expected)

    response = client.get("/user/profile/29cff183-c34d-445f-b6cf-31fb3b566158")
    assert str(response.json()) == str(user_profile_expected)
