from typing import Optional, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import RelOldPersonActivity
from acces_data_layer.services import engine


def insert(op_act: RelOldPersonActivity):
    """
    Inserts a new relation between an old person and an activity into the database.

    Args:
      op_act: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        session.add(op_act)
        session.commit()


def select() -> List[RelOldPersonActivity]:
    """
    Returns all the relations between old persons and activities from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonActivity).all()
        return relations


def select_by_id(op_id: int, act_id: int) -> Optional[RelOldPersonActivity]:
    """
    Returns the relation between an old person and an activity with the given IDs.

    Args:
      op_id: The ID of the old person.
      act_id: The ID of the activity.

    Returns:
      The relation with the given IDs, or `None` if no relation with those IDs is found.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonActivity, (op_id, act_id))
        return relation


def update(op_act: RelOldPersonActivity):
    """
    Updates a relation between an old person and an activity in the database.

    Args:
      op_act: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        current_relation = session.get(RelOldPersonActivity, (op_act.id_old_person, op_act.id_activity))
        current_relation.activity_hour = op_act.activity_hour
        session.commit()


def delete(op_id: int, act_id: int):
    """
    Deletes the relation between an old person and an activity with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      act_id: The ID of the activity.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonActivity, (op_id, act_id))
        session.delete(relation)
        session.commit()
