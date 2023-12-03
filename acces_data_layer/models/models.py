from datetime import datetime
from typing import Dict, List

from sqlalchemy import String, ForeignKey, LargeBinary, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from acces_data_layer import Base
from utils import serialize_bytes


class OlderPerson(Base):
    __tablename__ = "older_person"

    id_older_person: Mapped[int] = mapped_column(primary_key=True)
    older_person_name: Mapped[str] = mapped_column(String)
    audio: Mapped[bytes] = mapped_column(LargeBinary)
    """responsible_persons: Mapped[List["ResponsiblePerson"]] = relationship(
        secondary="r_older_person_responsible", back_populates="older_persons", viewonly=True
    )
    medicines: Mapped[List["Medicine"]] = relationship(
        secondary="r_older_person_medicine", back_populates="older_persons", viewonly=True
    )"""

    def __repr__(self) -> str:
        return f"Id Older Person(id={self.id_old_person!r}, Older Person Name={self.old_person_name!r})"

    def to_dict(self) -> Dict:
        """'responsible_persons': [responsible_person.to_dict() for responsible_person in self.responsible_persons],
                    'medicines': [medicine.to_dict() for medicine in self.medicines],"""
        return {
            'id_older_person': self.id_older_person,
            'older_person_name': self.older_person_name,
            'audio': serialize_bytes(data=self.audio)
        }


class ResponsiblePerson(Base):
    __tablename__ = "responsible_person"

    id_responsible_person: Mapped[int] = mapped_column(primary_key=True)
    responsible_person_name: Mapped[str] = mapped_column(String)
    """older_persons: Mapped[List["OlderPerson"]] = relationship(
        secondary="r_older_person_responsible", back_populates="responsible_persons", viewonly=True
    )"""

    def __repr__(self) -> str:
        return f"Responsible Person(id={self.id_responsible_person!r}, " \
               f"Responsible Person name={self.responsible_person_name!r}) "

    def to_dict(self) -> Dict:
        return {
            'id_responsible_person': self.id_responsible_person,
            'responsible_person_name': self.responsible_person_name,
        }


class RelOlderPersonResponsible(Base):
    __tablename__ = "r_older_person_responsible"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_older_person: Mapped[int] = mapped_column(ForeignKey("older_person.id_older_person"))
    id_responsible_person: Mapped[int] = mapped_column(ForeignKey("responsible_person.id_responsible_person"))

    def __repr__(self) -> str:
        return (f"Relation(id={self.id!r}), "
                f"Older Person(id={self.id_old_person!r}), "
                f"Responsible Person(id={self.id_responsible_person!r})")

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'id_older_person': self.id_older_person,
            'id_responsible_person': self.id_responsible_person
        }


class Medicine(Base):
    __tablename__ = "medicine"

    id_medicine: Mapped[int] = mapped_column(primary_key=True)
    medicine_name: Mapped[str] = mapped_column(String)
    """older_persons: Mapped[List["OlderPerson"]] = relationship(
        secondary="r_older_person_medicine", back_populates="medicines", viewonly=True
    )"""

    def __repr__(self) -> str:
        return f"Id Medicine(id={self.id_medicine!r}, Medicine name={self.medicine_name!r})"

    def to_dict(self) -> Dict:
        return {
            'id_medicine': self.id_medicine,
            'medicine_name': self.medicine_name,
        }


class RelOlderPersonMedicine(Base):
    __tablename__ = "r_older_person_medicine"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_older_person: Mapped[int] = mapped_column(ForeignKey("older_person.id_older_person"))
    id_medicine: Mapped[int] = mapped_column(ForeignKey("medicine.id_medicine"))
    medicine_hour: Mapped[datetime] = mapped_column(TIMESTAMP)
    status: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Relation(id={self.id!r}), Older Person(id={self.id_old_person!r}), Medicine(id={self.id_medicine!r})" \
               f"Medicine Hour(hour={self.medicine_hour!r}, Status(status={self.status!r})"

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'id_older_person': self.id_older_person,
            'id_medicine': self.id_medicine,
            'medicine_hour': self.medicine_hour,
            'status': self.status
        }
