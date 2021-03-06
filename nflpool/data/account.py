import datetime
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer

from nflpool.data.modelbase import SqlAlchemyBase


class Account(SqlAlchemyBase):
    __tablename__ = "Account"

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()).replace("-", "")
    )

    email = Column(String, index=True, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
    email_confirmed = Column(Boolean, nullable=False, default=False)
    is_super_user = Column(Boolean, nullable=False, default=False)
    twitter = Column(String, nullable=True)
    paid = Column(Integer, default=0)
