"""
Experiment Model
"""

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from database.models.base import Base


class Experiment(Base):

    __tablename__ = "experiments"

    id = Column(
        Integer,
        primary_key=True
    )

    experiment_uid = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(Text)

    status = Column(
        String(20),
        default="CREATED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    ####################################################################
    # Relationships
    ####################################################################

    configuration = relationship(
        "Configuration",
        uselist=False,
        back_populates="experiment",
        cascade="all, delete-orphan"
    )

    ####################################################################

    def __repr__(self):

        return (
            f"<Experiment("
            f"{self.experiment_uid}, "
            f"{self.name})>"
        )
