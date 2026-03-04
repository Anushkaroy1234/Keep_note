from sqlalchemy import Column,Integer,String,Text
from app.db.base import Base,TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column

class KeepNote(Base,TimestampMixin,):
    __tablename__="keepnotes"

    
    Title:Mapped[str] = mapped_column(String(200), nullable=False)
    Progress:Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    Description:Mapped[str] = mapped_column(Text, nullable=False)
