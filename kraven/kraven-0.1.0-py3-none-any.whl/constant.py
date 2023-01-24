PRODUCT_HUNT = "https://www.producthunt.com"

PRODUCT_HUNT_API = "https://api.producthunt.com/v2/api/graphql"

USAGE = ()

ENDPOINTS = ( "streaks", "trending", "user", "post", "collection" )

SCHEMAS = {
    "streaks": {
        "key": "visitStreaks", "Streak": "duration", "Username": "user.username"
        },
    "trending": {
        "key": "homefeed",
        "Name": "name",
        "Tagline": "tagline",
        "Votes": "votesCount",
        },
    "user":
        {
            "Name": "name",
            "Posts": "madePosts.totalCount",
            "Followers": "followers.totalCount",
            "Following": "following.totalCount",
            }
    }
