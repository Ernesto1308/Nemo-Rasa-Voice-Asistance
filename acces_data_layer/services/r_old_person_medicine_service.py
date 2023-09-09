from datetime import datetime
from typing import Optional, List, Type, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, Row
from acces_data_layer.models.models import RelOldPersonMedicine
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


def select_by_id(op_id: int, med_id: int) -> Optional[RelOldPersonMedicine]:
    """
    Returns the relation between an old person and a medicine with the given IDs.

    Args:
      op_id: The ID of the old person.
      med_id: The ID of the medicine.

    Returns:
      The relation with the given IDs, or `None` if no relation with those IDs is found.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonMedicine, (op_id, med_id))
        return relation


def select_by_ids_hour(op_id: int, med_id: int, hour: datetime) -> Optional[datetime]:
    """
    Returns the medicine hour for the relation between an old person
    and a medicine after the specified hour.

    Args:
        op_id: The ID of the old person.
        med_id: The ID of the medicine.
        hour: The hour to filter relations after.

    Returns:
        A datetime containing the medicine_hour if a matching relation is found
        after the specified hour, otherwise None.
    """

    with Session(engine) as session:
        result = session.scalars(
            select(RelOldPersonMedicine.medicine_hour)
            .where(RelOldPersonMedicine.id_old_person == op_id)
            .where(RelOldPersonMedicine.id_medicine == med_id)
            .where(RelOldPersonMedicine.medicine_hour >= hour)
        ).first()

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


def delete(op_id: int, med_id: int):
    """
    Deletes the relation between an old person and a medicine with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      med_id: The ID of the medicine.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonMedicine, (op_id, med_id))
        session.delete(relation)
        session.commit()
