from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from sqlalchemy import String
from app.db.base import Base, TimestampMixin

class Userdetails(Base, TimestampMixin):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)