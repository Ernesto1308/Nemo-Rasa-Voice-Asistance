from datetime import datetime
from typing import List, Tuple, Any, Sequence

from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from acces_data_layer.models.models import RelOldPersonMedicine, Medicine, OldPerson
from acces_data_layer.services import engine


def insert(op_med_data: Any) -> None:
    """
    Inserts a new relation between an old person and a medicine into the database.

    Args:
      op_med_data: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_med = RelOldPersonMedicine(**op_med_data)
        session.add(op_med)
        session.commit()


def select_all() -> List[dict]:
    """
    Returns all the relations between old persons and medicines from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.execute(
           select(
               OldPerson.id_old_person, OldPerson.old_person_name,
               Medicine.id_medicine, Medicine.medicine_name,
               RelOldPersonMedicine.medicine_hour
           ).join(
               RelOldPersonMedicine, OldPerson.id_old_person == RelOldPersonMedicine.id_old_person
           ).join(
              Medicine, RelOldPersonMedicine.id_medicine == Medicine.id_medicine
           )
        )
        rows = []

        for row in relations:
            rows.append(
                {
                    "id_old_person": row.id_old_person,
                    "old_person_name": row.old_person_name,
                    "id_medicine": row.id_medicine,
                    "medicine_name": row.medicine_name,
                    "medicine_hour": row.medicine_hour,
                }
            )

        return rows


def select_by_ids_hour(id_op: int, id_med: int, hour: datetime) -> List:
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
        ).all()

        return list(result)


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
        op_med_current_state = RelOldPersonMedicine(**op_med.get('current_state'))
        op_med_next_state = RelOldPersonMedicine(**op_med.get('next_state'))
        current_relation = session.get(
            RelOldPersonMedicine, (
                op_med_current_state.id_old_person,
                op_med_current_state.id_medicine,
                op_med_current_state.medicine_hour
            )
        )
        current_relation.id_old_person = op_med_next_state.id_old_person
        current_relation.id_medicine = op_med_next_state.id_medicine
        current_relation.medicine_hour = op_med_next_state.medicine_hour
        session.commit()


def delete(id_op: int, id_med: int, medicine_hour: datetime) -> None:
    """
    Deletes the relation between an old person and a medicine with the given IDs from the database.

    Args:
      id_op: The ID of the old person.
      id_med: The ID of the medicine.
      medicine_hour: The hour of the medicine.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonMedicine, (id_op, id_med, medicine_hour))
        session.delete(relation)
        session.commit()
