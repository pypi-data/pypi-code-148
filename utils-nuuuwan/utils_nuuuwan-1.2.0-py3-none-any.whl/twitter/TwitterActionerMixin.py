"""Implements twitter."""


from utils.Log import Log
from utils.time.Time import Time
from utils.time.TimeFormat import TimeFormat
from utils.time.TIMEZONE_OFFSET import TIMEZONE_OFFSET
from utils.twitter.Tweet import Tweet

log = Log('Twitter')


def _update_status(api, tweet_text, media_ids, in_reply_to_status_id):
    if len(media_ids) > 0:
        if in_reply_to_status_id:
            response = api.update_status(
                tweet_text,
                media_ids=media_ids,
                in_reply_to_status_id=in_reply_to_status_id,
            )
        else:
            response = api.update_status(
                tweet_text,
                media_ids=media_ids,
            )
    else:
        if in_reply_to_status_id:
            response = api.update_status(
                tweet_text, in_reply_to_status_id=in_reply_to_status_id
            )
        else:
            response = api.update_status(tweet_text)
    return response


def _upload_media(api, image_files):
    media_ids = []
    for image_file in image_files:
        media_id = api.media_upload(image_file).media_id
        media_ids.append(media_id)
        log.info(
            f'Uploaded status image {image_file} to twitter as {media_id}',
        )
    return media_ids


def _update_profile_description(api):
    date_with_timezone = TimeFormat(
        '%Y-%m-%d %H:%M:%S', TIMEZONE_OFFSET.LK
    ).stringify(Time.now())
    description = (
        f'Automatically updated at {date_with_timezone} (#SriLanka Time)'
    )
    api.update_profile(description=description)
    log.info(f'Updated profile description to: {description}')


class TwitterActionerMixin:
    def send(self, tweet: Tweet):
        media_ids = _upload_media(
            self.api,
            tweet.image_file_path_list,
        )
        return _update_status(
            self.api, tweet.text, media_ids, tweet.in_reply_to_status_id
        )

    def update_profile_description(self):
        _update_profile_description(self.api)

    def update_profile_image(self, profile_image_file):
        log.debug(f'update_profile_image: {profile_image_file}')
        self.api.update_profile_image(profile_image_file)

    def update_banner_image(self, banner_image_file):
        log.debug(f'update_banner_image: {banner_image_file}')
        self.api.update_profile_banner(banner_image_file)
