from pydantic import BaseModel


class Config(BaseModel):
    max_users: int
    use_email_notification: bool
    use_sms_notification: bool
