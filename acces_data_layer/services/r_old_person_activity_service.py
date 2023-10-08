from datetime import datetime
from typing import List, Any

from sqlalchemy.orm import Session

from acces_data_layer.models.models import RelOldPersonActivity
from acces_data_layer.services import engine


def insert(op_act_data: Any) -> None:
    """
    Inserts a new relation between an old person and an activity into the database.

    Args:
      op_act_data: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_act_current_state = RelOldPersonActivity(**op_act_data)
        session.add(op_act_current_state)
        session.commit()


def select_all() -> List[dict]:
    """
    Returns all the relations between old persons and activities from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonActivity).all()
        relations_dict = [relation.to_dict() for relation in relations]
        return relations_dict


def update(op_act_data: Any) -> None:
    """
    Updates a relation between an old person and an activity in the database.

    Args:
      op_act_data: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_act_current_state = RelOldPersonActivity(**op_act_data.get('current_state'))
        op_act_next_state = RelOldPersonActivity(**op_act_data.get('next_state'))
        current_relation = session.get(
            RelOldPersonActivity, (
                op_act_current_state.id_old_person,
                op_act_current_state.id_activity,
                op_act_current_state.activity_hour
            )
        )
        current_relation.id_old_person = op_act_next_state.id_old_person
        current_relation.id_activity = op_act_next_state.id_activity
        current_relation.activity_hour = op_act_next_state.activity_hour
        session.commit()


def delete(op_id: int, act_id: int, act_hour: datetime) -> None:
    """
    Deletes the relation between an old person and an activity with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      act_id: The ID of the activity.
      act_hour: The hour of the activity.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonActivity, (op_id, act_id, act_hour))
        session.delete(relation)
        session.commit()
