from datetime import datetime, timezone

from sqlalchemy import Column, BigInteger, DateTime, Integer, Boolean, func

from bot.db.base import Base


class User(Base):
    """
        Класс пользователя
    """
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    login_attempts = Column(Integer, unique=False)
    login = Column(Boolean, unique=False)
    login_time = Column(Integer, unique=False)
    creation_date = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))
    update_date = Column(DateTime(timezone=True), onupdate=func.now(tz=timezone.utc))

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
