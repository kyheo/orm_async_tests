from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, declarative_base, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class DateTimeModel(Base):
    __abstract__ = True
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.utcnow)


class User(DateTimeModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"


class TrackPoint(DateTimeModel):
    __tablename__ = "track_points"
    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    lat: float = Column(Float, nullable=False)
    lon: float = Column(Float, nullable=False)
    date: Mapped[datetime] = Column(DateTime, nullable=False)

    user: "User" = relationship("User", uselist=False)

    def __repr__(self) -> str:
        return (
            f"TrackPoint(id={self.id}, user_id={self.user_id}, lat={self.lat}, "
            f"lon={self.lon}, date={self.date.isoformat()}, user={self.user})"
        )
