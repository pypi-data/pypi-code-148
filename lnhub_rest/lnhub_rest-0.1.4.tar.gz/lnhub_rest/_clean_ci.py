from datetime import datetime, timedelta

from lamin_logger import logger
from sqlalchemy import text

from lnhub_rest import engine
from lnhub_rest._sbclient import connect_hub_with_auth


def delete_ci_instances() -> None:
    try:
        hub = connect_hub_with_auth()
        # Delete instances created by the CI more than one hour ago
        data = (
            hub.table("instance")
            .delete()
            .like("name", "lamin.ci.instance.%")
            .lt("created_at", datetime.now() - timedelta(hours=1))
            .execute()
            .data
        )
        instance_count = len(data)
        logger.info(f"{instance_count} instances deleted")
    finally:
        hub.auth.sign_out()


def delete_ci_auth_users():
    # Delete users in auth.user table created by the CI more than one hour ago
    query = f"""
    delete
    from auth.users
    where email like 'lamin.ci.user.%'
    and created_at < '{str(datetime.now() - timedelta(hours=1))}';
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()


def delete_ci_accounts() -> None:
    # Delete accounts created by the CI more than one hour ago
    query = f"""
    delete
    from account
    where handle like 'lamin.ci.user.%'
    and created_at < '{str(datetime.now() - timedelta(hours=1))}';
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
