"""
Configuration Model
"""

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from database.models.base import Base


class Configuration(Base):

    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True)

    experiment_id = Column(
        Integer,
        ForeignKey("experiments.id"),
        nullable=False
    )

    protocol = Column(String(20), default="ipv6")

    ip_mode = Column(String(20), default="automatic")

    topology_type = Column(String(50))

    controller = Column(String(50))

    duration = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    experiment = relationship(
        "Experiment",
        back_populates="configuration"
    )
