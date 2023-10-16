from datetime import datetime
from typing import List, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from acces_data_layer.models.models import RelOldPersonFeeding, OldPerson, Feeding
from acces_data_layer.services import engine


def insert(op_feed_data: Any) -> None:
    """
    Inserts a new relation between an old person and a feeding into the database.

    Args:
      op_feed_data: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_feed = RelOldPersonFeeding(**op_feed_data)
        session.add(op_feed)
        session.commit()


def select_all() -> List[dict]:
    """
    Returns all the relations between old persons and feedings from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.execute(
            select(
                OldPerson.id_old_person, OldPerson.old_person_name,
                Feeding.id_feeding, Feeding.feeding_name,
                RelOldPersonFeeding.feeding_hour
            ).join(
                RelOldPersonFeeding, OldPerson.id_old_person == RelOldPersonFeeding.id_old_person
            ).join(
                Feeding, RelOldPersonFeeding.id_feeding == Feeding.id_feeding
            )
        )
        rows = []

        for row in relations:
            rows.append(
                {
                    "id_old_person": row.id_old_person,
                    "old_person_name": row.old_person_name,
                    "id_feeding": row.id_feeding,
                    "feeding_name": row.feeding_name,
                    "feeding_hour": row.feeding_hour,
                }
            )

        return rows


def update(op_feed_data: Any) -> None:
    """
    Updates a relation between an old person and a feeding in the database.

    Args:
      op_feed_data: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_feed_current_state = RelOldPersonFeeding(**op_feed_data.get('current_state'))
        op_feed_next_state = RelOldPersonFeeding(**op_feed_data.get('next_state'))
        current_relation = session.get(
            RelOldPersonFeeding, (
                op_feed_current_state.id_old_person,
                op_feed_current_state.id_feeding,
                op_feed_current_state.feeding_hour
            )
        )
        current_relation.id_old_person = op_feed_next_state.id_old_person
        current_relation.id_feeding = op_feed_next_state.id_feeding
        current_relation.feeding_hour = op_feed_next_state.feeding_hour
        session.commit()


def delete(op_id: int, feed_id: int, feeding_hour: datetime) -> None:
    """
    Deletes the relation between an old person and a feeding with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      feed_id: The ID of the feeding.
      feeding_hour: The hour of the feeding.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonFeeding, (op_id, feed_id, feeding_hour))
        session.delete(relation)
        session.commit()
