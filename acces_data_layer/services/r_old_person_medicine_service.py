from datetime import datetime
from typing import Optional, List, Type, Tuple, Any, Sequence, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, Row, ScalarResult, RowMapping, Result, MappingResult
from acces_data_layer.models.models import RelOldPersonMedicine, Medicine, OldPerson
from acces_data_layer.services import engine


def insert(op_med: RelOldPersonMedicine):
    """
    Inserts a new relation between an old person and a medicine into the database.

    Args:
      op_med: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        session.add(op_med)
        session.commit()


def select_all() -> List[Type[RelOldPersonMedicine]]:
    """
    Returns all the relations between old persons and medicines from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonMedicine).all()
        return relations


def select_by_id(id_op: int, id_med: int) -> Optional[RelOldPersonMedicine]:
    """
    Returns the relation between an old person and a medicine with the given IDs.

    Args:
      id_op: The ID of the old person.
      id_med: The ID of the medicine.

    Returns:
      The relation with the given IDs, or `None` if no relation with those IDs is found.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonMedicine, (id_op, id_med))
        return relation


def select_by_ids_hour(id_op: int, id_med: int, hour: datetime) -> Optional[datetime]:
    """
    Returns the medicine hour for the relation between an old person
    and a medicine after the specified hour.

    Args:
        id_op: The ID of the old person.
        id_med: The ID of the medicine.
        hour: The hour to filter relations after.

    Returns:
        A datetime containing the medicine_hour if a matching relation is found
        after the specified hour, otherwise None.
    """

    with Session(engine) as session:
        result = session.scalars(
            select(RelOldPersonMedicine.medicine_hour)
            .where(RelOldPersonMedicine.id_old_person == id_op)
            .where(RelOldPersonMedicine.id_medicine == id_med)
            .where(RelOldPersonMedicine.medicine_hour >= hour)
        ).first()

        return result


def select_by_op_id(
    id_op: int,
    start_hour: datetime,
    end_hour: datetime
) -> Sequence[Row[Tuple[Any, Any]]]:

    """
    Get medicine info for a patient between specified hours.

    Args:
        id_op: The id of the old person (patient)
        start_hour: The start of the datetime range
        end_hour: The end of the datetime range

    Returns:
        A ScalarResult containing medicine name and hour info
        for the given patient id and date range.
    """

    with Session(engine) as session:
        result = session.execute(
            select(Medicine.medicine_name, RelOldPersonMedicine.medicine_hour)
            .join(RelOldPersonMedicine, Medicine.id_medicine == RelOldPersonMedicine.id_medicine)
            .where(RelOldPersonMedicine.id_old_person == id_op)
            .filter(RelOldPersonMedicine.medicine_hour >= start_hour)
            .filter(RelOldPersonMedicine.medicine_hour <= end_hour)
        ).all()

        return result


def update(op_med: RelOldPersonMedicine):
    """
    Updates a relation between an old person and a medicine in the database.

    Args:
      op_med: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        current_relation = session.get(RelOldPersonMedicine, (op_med.id_old_person, op_med.id_medicine))
        current_relation.medicine_hour = op_med.medicine_hour
        session.commit()


def delete(id_op: int, id_med: int):
    """
    Deletes the relation between an old person and a medicine with the given IDs from the database.

    Args:
      id_op: The ID of the old person.
      id_med: The ID of the medicine.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonMedicine, (id_op, id_med))
        session.delete(relation)
        session.commit()
