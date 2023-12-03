from datetime import datetime
from typing import List, Tuple, Sequence, Any, Dict

from sqlalchemy import select, Row

from acces_data_layer import db_session
from acces_data_layer.models.models import RelOlderPersonMedicine, Medicine, OlderPerson


def insert(op_med: RelOlderPersonMedicine) -> None:
    """
    Inserts a new relation between an old person and a medicine into the database.

    Args:
      op_med: The relation to insert.

    Returns:
      None.
    """
    op_med.status = 'Pendiente'
    db_session.add(op_med)
    db_session.commit()


def select_all() -> List[dict]:
    """
    Returns all the relations between old persons and medicines from the database.

    Returns:
      A list of relations.
    """
    relations = db_session.execute(
        select(
            RelOlderPersonMedicine.id,
            OlderPerson.id_older_person, OlderPerson.older_person_name,
            Medicine.id_medicine, Medicine.medicine_name,
            RelOlderPersonMedicine.medicine_hour,
            RelOlderPersonMedicine.status
        ).join(
            RelOlderPersonMedicine, OlderPerson.id_older_person == RelOlderPersonMedicine.id_older_person
        ).join(
            Medicine, RelOlderPersonMedicine.id_medicine == Medicine.id_medicine
        )
    )
    rows = []

    for row in relations:
        rows.append(
            {
                "id": row.id,
                "id_older_person": row.id_older_person,
                "older_person_name": row.older_person_name,
                "id_medicine": row.id_medicine,
                "medicine_name": row.medicine_name,
                "medicine_hour": row.medicine_hour,
                "status": row.status
            }
        )

    return rows


def select_by_id(id_relation: int) -> RelOlderPersonMedicine:
    """
    Returns the relation between an old person and a medicine with the given ID.

    Args:
        id_relation: The ID of the relation.

    Returns:
        The relation with the given id
    """
    relation = db_session.get(RelOlderPersonMedicine, id_relation)
    return relation


def select_by_ids_major_hour(id_op: int, id_med: int, hour: datetime) -> List[datetime]:
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
    result = db_session.scalars(
        select(RelOlderPersonMedicine.medicine_hour)
        .where(RelOlderPersonMedicine.id_older_person == id_op)
        .where(RelOlderPersonMedicine.id_medicine == id_med)
        .where(RelOlderPersonMedicine.medicine_hour >= hour)
    ).all()

    return result


def select_by_ids_hour(id_op: int, id_med: int, hour: datetime) -> RelOlderPersonMedicine:
    """
    Returns the medicine hour for the relation between an old person
    and a medicine with the specified hour.

    Args:
        id_op: The ID of the old person.
        id_med: The ID of the medicine.
        hour: The hour of the medicine.

    Returns:
        The relation selected.
    """
    result = db_session.scalar(
        select(RelOlderPersonMedicine)
        .where(RelOlderPersonMedicine.id_older_person == id_op)
        .where(RelOlderPersonMedicine.id_medicine == id_med)
        .where(RelOlderPersonMedicine.medicine_hour == hour)
    )

    return result


def get_medicine_schedule(id_op: int, start_hour: datetime, end_hour: datetime) -> Dict[str, List[datetime]]:
    """
    Get medicine schedule for a patient between specified hours.

    Args:
        id_op: The id of the old person (patient)
        start_hour: The start of the datetime range
        end_hour: The end of the datetime range

    Returns:
        A dictionary where keys are medicine names and values are lists of datetime with the hours.
    """
    result = db_session.execute(
        select(Medicine.medicine_name, RelOlderPersonMedicine.medicine_hour)
        .join(RelOlderPersonMedicine, Medicine.id_medicine == RelOlderPersonMedicine.id_medicine)
        .where(RelOlderPersonMedicine.id_older_person == id_op and RelOlderPersonMedicine.status == "Pendiente")
        .filter(RelOlderPersonMedicine.medicine_hour >= start_hour)
        .filter(RelOlderPersonMedicine.medicine_hour <= end_hour)
    ).all()

    medicine_schedule = {}

    for medicine_name, medicine_hour in result:
        if medicine_name not in medicine_schedule:
            medicine_schedule[medicine_name] = []
        medicine_schedule[medicine_name].append(medicine_hour)

    return medicine_schedule


def update(op_med: RelOlderPersonMedicine):
    """
    Updates a relation between an old person and a medicine in the database.

    Args:
      op_med: The relation to update.

    Returns:
      None.
    """
    db_session.merge(op_med)
    db_session.commit()


def delete(id_relation: int) -> None:
    """
    Deletes the relation between an old person and a medicine with the given IDs from the database.

    Args:
      id_relation: The ID of relation.

    Returns:
      None.
    """
    relation = db_session.get(RelOlderPersonMedicine, id_relation)
    db_session.delete(relation)
    db_session.commit()
