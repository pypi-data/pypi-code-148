from datetime import datetime
from uuid import uuid4
from caronte_common.data.entities.owner import Owner
from caronte_common.data.entities.project import Project
from caronte_common.data.entities.claim import Claim
from caronte_common.data.entities.config import Config
from caronte_common.data.entities.role import Role
from caronte_common.data.entities.user import User


if __name__ == "__main__":
    owner = Owner(
        email="giovanilzanini@hotmail.com",
        cellphone="+55 47 99292-0419",
        user_name="giovanilzanini",
        full_name="Giovani Liskoski Zanini",
        projects=Project(
            name="Driver Manager",
            description="Gerencie seus gastos diarios durante suas corridas de Uber e 99Taxi",
            config=Config(
                max_users=15, use_email_notification=True, use_sms_notification=True
            ),
            claims=[
                Claim(
                    name="stats",
                    value="dayly",
                    created_at=datetime.now(),
                    external_id=uuid4(),
                ),
                Claim(
                    name="stats",
                    value="monthly",
                    created_at=datetime.now(),
                    external_id=uuid4(),
                ),
            ],
            roles=Role(
                name="stats",
                claims=[uuid4(), uuid4()],
                created_at=datetime.now(),
            ),
            users=[
                User(
                    email="user01@gmail.com",
                    cellphone="+55 47 99292-0418",
                    user_name="user-01",
                    full_name="user 0 1",
                    created_at=datetime.now(),
                    password="abc123",
                    external_id=uuid4(),
                ),
                User(
                    email="user02@gmail.com",
                    cellphone="+55 47 99292-0418",
                    user_name="user-02",
                    full_name="user 0 2",
                    created_at=datetime.now(),
                    password="123abc",
                    external_id=uuid4(),
                ),
            ],
            created_at=datetime.now(),
            external_id=uuid4(),
        ),
        created_at=datetime.now(),
        password="xxxx",
        external_id=uuid4(),
    )
