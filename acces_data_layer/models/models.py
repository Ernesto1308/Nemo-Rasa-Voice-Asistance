from datetime import datetime
from typing import List, Dict

from sqlalchemy import String, ForeignKey, LargeBinary, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from acces_data_layer.models import Base


class OldPerson(Base):
    __tablename__ = "old_person"

    id_old_person: Mapped[int] = mapped_column(primary_key=True)
    old_person_name: Mapped[str] = mapped_column(String)
    audio: Mapped[bytes] = mapped_column(LargeBinary)
    responsible_persons: Mapped[List["ResponsiblePerson"]] = relationship(secondary="r_old_person_responsible",
                                                                          back_populates="old_persons", viewonly=True)
    exercises: Mapped[List["Exercise"]] = relationship(secondary="r_old_person_exercise",
                                                       back_populates="old_persons", viewonly=True)
    feedings: Mapped[List["Feeding"]] = relationship(secondary="r_old_person_feeding",
                                                     back_populates="old_persons", viewonly=True)
    medicines: Mapped[List["Medicine"]] = relationship(secondary="r_old_person_medicine",
                                                       back_populates="old_persons", viewonly=True)

    def __repr__(self) -> str:
        return f"Id Old Person(id={self.id_old_person!r}, Old Person Name={self.old_person_name!r})"

    def to_dict(self) -> Dict:
        return {
            'id_old_person': self.id_old_person,
            'old_person_name': self.old_person_name,
            # 'audio': serialize_bytes(data=self.audio),
        }


class ResponsiblePerson(Base):
    __tablename__ = "responsible_person"

    id_responsible_person: Mapped[int] = mapped_column(primary_key=True)
    responsible_person_name: Mapped[str] = mapped_column(String)
    old_persons: Mapped[List[OldPerson]] = relationship(secondary="r_old_person_responsible",
                                                        back_populates="responsible_persons", viewonly=True)

    def __repr__(self) -> str:
        return f"Responsible Person(id={self.id_responsible_person!r}, " \
               f"Responsible Person name={self.responsible_person_name!r}) "

    def to_dict(self) -> Dict:
        return {
            'id_responsible_person': self.id_responsible_person,
            'responsible_person_name': self.responsible_person_name,
        }


class RelOldPersonResponsible(Base):
    __tablename__ = "r_old_person_responsible"

    id_old_person: Mapped[int] = mapped_column(ForeignKey("old_person.id_old_person"), primary_key=True)
    id_responsible_person: Mapped[int] = mapped_column(ForeignKey("responsible_person.id_responsible_person"),
                                                       primary_key=True)

    def __repr__(self) -> str:
        return f"Old Person(id={self.id_old_person!r}), Responsible Person(id={self.id_responsible_person!r})"

    def to_dict(self) -> Dict:
        return {
            'id_old_person': self.id_old_person,
            'id_responsible_person': self.id_responsible_person
        }


class Exercise(Base):
    __tablename__ = "exercise"

    id_exercise: Mapped[int] = mapped_column(primary_key=True)
    exercise_name: Mapped[str] = mapped_column(String)
    old_persons: Mapped[List[OldPerson]] = relationship(secondary="r_old_person_exercise",
                                                        back_populates="exercises", viewonly=True)

    def __repr__(self) -> str:
        return f"Id Exercise(id={self.id_exercise!r}, Exercise name={self.exercise_name!r})"

    def to_dict(self) -> Dict:
        return {
            'id_exercise': self.id_exercise,
            'exercise_name': self.exercise_name,
        }


class RelOldPersonExercise(Base):
    __tablename__ = "r_old_person_exercise"

    id_old_person: Mapped[int] = mapped_column(ForeignKey("old_person.id_old_person"), primary_key=True)
    id_exercise: Mapped[int] = mapped_column(ForeignKey("exercise.id_exercise"),
                                             primary_key=True)
    exercise_hour: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)

    def __repr__(self) -> str:
        return f"Id Person(id={self.id_old_person!r}), Exercise(id={self.id_exercise!r}) " \
               f"Exercise Hour(hour={self.exercise_hour!r}"

    def to_dict(self) -> Dict:
        return {
            'id_old_person': self.id_old_person,
            'id_exercise': self.id_exercise,
            'exercise_hour': self.exercise_hour
        }


class Feeding(Base):
    __tablename__ = "feeding"

    id_feeding: Mapped[int] = mapped_column(primary_key=True)
    feeding_name: Mapped[str] = mapped_column(String)
    old_persons: Mapped[List[OldPerson]] = relationship(secondary="r_old_person_feeding",
                                                        back_populates="feedings", viewonly=True)

    def __repr__(self) -> str:
        return f"Id Feeding(id={self.id_feeding!r}, Feeding name={self.feeding_name!r})"

    def to_dict(self) -> Dict:
        return {
            'id_feeding': self.id_feeding,
            'feeding_name': self.feeding_name,
        }


class RelOldPersonFeeding(Base):
    __tablename__ = "r_old_person_feeding"

    id_old_person: Mapped[int] = mapped_column(ForeignKey("old_person.id_old_person"), primary_key=True)
    id_feeding: Mapped[int] = mapped_column(ForeignKey("feeding.id_feeding"),
                                            primary_key=True)
    feeding_hour: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)

    def __repr__(self) -> str:
        return f"Old Person(id={self.id_old_person!r}), Feeding(id={self.id_feeding!r})" \
               f"Feeding Hour(hour={self.feeding_hour!r}"

    def to_dict(self) -> Dict:
        return {
            'id_old_person': self.id_old_person,
            'id_feeding': self.id_feeding,
            'feeding_hour': self.feeding_hour
        }


class Medicine(Base):
    __tablename__ = "medicine"

    id_medicine: Mapped[int] = mapped_column(primary_key=True)
    medicine_name: Mapped[str] = mapped_column(String)
    old_persons: Mapped[List[OldPerson]] = relationship(secondary="r_old_person_medicine",
                                                        back_populates="medicines", viewonly=True)

    def __repr__(self) -> str:
        return f"Id Medicine(id={self.id_medicine!r}, Medicine name={self.medicine_name!r})"

    def to_dict(self) -> Dict:
        return {
            'id_medicine': self.id_medicine,
            'medicine_name': self.medicine_name,
        }


class RelOldPersonMedicine(Base):
    __tablename__ = "r_old_person_medicine"

    id_old_person: Mapped[int] = mapped_column(ForeignKey("old_person.id_old_person"), primary_key=True)
    id_medicine: Mapped[int] = mapped_column(ForeignKey("medicine.id_medicine"),
                                             primary_key=True)
    medicine_hour: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    status: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Old Person(id={self.id_old_person!r}), Medicine(id={self.id_medicine!r})" \
               f"Medicine Hour(hour={self.medicine_hour!r}, Status(status={self.status!r})"

    def to_dict(self) -> Dict:
        return {
            'id_old_person': self.id_old_person,
            'id_medicine': self.id_medicine,
            'medicine_hour': self.medicine_hour,
            'status': self.status
        }
