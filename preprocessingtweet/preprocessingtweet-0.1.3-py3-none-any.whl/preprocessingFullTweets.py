import datetime
import logging

import preprocessingText
import pytz

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


def process_tweet(tweet, lang):
    """
    Getting a tweet dictionary and returning a cleaned version of it
    :params:
        tweet dict(): tweet dictionary containing the following keys:
            - [text]
            - [created_at] # Optional
            - [extended_tweet][full_text]
            - [retweet_status][extended_tweet]
            - [entities][urls] # Optional
            - [entities][hashtags] # Optional
            - [entities][user_mentions] # Optional
    """

    tweet_to_return = dict()

    # Transform the date into a datetime format
    try:
        tweet_to_return["created_at"] = datetime.datetime.strptime(
            tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y"
        ).replace(tzinfo=pytz.UTC)
    except KeyError:
        tweet_to_return['created_at'] = None

    # Try to get the full text in either the case of a retweet or a normal tweet
    # Seems to have the key 'truncated': bool() that can be used
    try:
        if (
            tweet["retweeted_status"] is None
        ):  # used in case parse the pandas document after 1.export. In that case the key exists == None. Raise KeyError to ensure compatibility
            raise KeyError
        tweet_to_return["rt_status"] = True
        tweet_to_return["text"] = tweet["retweeted_status"]["extended_tweet"][
            "full_text"
        ]
    except KeyError:
        tweet_to_return["rt_status"] = False
        try:
            tweet_to_return["text"] = tweet["extended_tweet"]["full_text"]
        except KeyError:
            tweet_to_return["text"] = tweet["text"]

    remove_entities = preprocessingText.preprocess_text(
        tweet_to_return["text"],
        remove_mention=False,
        remove_url=False,
        remove_rt=False,
        replace_emoticon=True,
        replace_emoji=True,
    )

    tweet_to_return["txt_wo_entities"] = remove_entities["tweet"]

    tweet_to_return["stemmed_text"] = preprocessingText.stem_text(
        tweet_to_return["txt_wo_entities"], lang=lang
    )

    tweet_to_return["token_txt"] = preprocessingText.return_token(
        tweet_to_return["txt_wo_entities"]
    )

    tweet_to_return["token_stemmed_txt"] = preprocessingText.return_token(
        tweet_to_return["stemmed_text"]
    )

    tweet_to_return["word_count"] = len(tweet_to_return["token_txt"])

    # Check if the rt has not been set up as true earlier
    if tweet_to_return["rt_status"] is False:
        tweet_to_return["rt_status"] = remove_entities["rt_status"]

    try:
        tweet_to_return["user_mentions"] = [x["screen_name"].lower() for x in tweet["entities"]["user_mentions"]
                                            ]
    except KeyError:
        tweet_to_return['user_mentions'] = remove_entities['mentions']

    try:
        tweet_to_return["user_mentions_ids"] = [
            x["id"] for x in tweet["entities"]["user_mentions"]
        ]
    except KeyError:
        tweet_to_return["user_mentions_ids"] = None

    try:
        tweet_to_return["hashtags"] = [
            x["text"].lower() for x in tweet["entities"]["hashtags"]
        ]
    except KeyError:
        tweet_to_return["hashtags"] = remove_entities['hashtags']

    try:
        tweet_to_return["urls"] = [x["expanded_url"]
                                   for x in tweet["entities"]["urls"]]
    except KeyError:
        tweet_to_return["urls"] = remove_entities['urls']

    return tweet_to_return


def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
