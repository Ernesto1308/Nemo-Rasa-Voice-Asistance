from datetime import datetime
from typing import List, Any

from sqlalchemy.orm import Session

from acces_data_layer.models.models import RelOldPersonExercise
from acces_data_layer.services import engine


def insert(op_ex_data: Any) -> None:
    """
    Inserts a new relation between an old person and an exercise into the database.

    Args:
      op_ex_data: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_ex_current_state = RelOldPersonExercise(**op_ex_data)
        session.add(op_ex_current_state)
        session.commit()


def select_all() -> List[dict]:
    """
    Returns all the relations between old persons and exercises from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonExercise).all()
        relations_dict = [relation.to_dict() for relation in relations]
        return relations_dict


def update(op_ex_data: Any) -> None:
    """
    Updates a relation between an old person and an exercise in the database.

    Args:
      op_ex_data: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        op_ex_current_state = RelOldPersonExercise(**op_ex_data.get('current_state'))
        op_ex_next_state = RelOldPersonExercise(**op_ex_data.get('next_state'))
        current_relation = session.get(
            RelOldPersonExercise, (
                op_ex_current_state.id_old_person,
                op_ex_current_state.id_exercise,
                op_ex_current_state.exercise_hour
            )
        )
        current_relation.id_old_person = op_ex_next_state.id_old_person
        current_relation.id_exercise = op_ex_next_state.id_exercise
        current_relation.exercise_hour = op_ex_next_state.exercise_hour
        session.commit()


def delete(op_id: int, ex_id: int, ex_hour: datetime) -> None:
    """
    Deletes the relation between an old person and an exercise with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      ex_id: The ID of the exercise.
      ex_hour: The hour of the exercise.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonExercise, (op_id, ex_id, ex_hour))
        session.delete(relation)
        session.commit()
