from typing import Optional, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import RelOldPersonExercise
from acces_data_layer.services import engine


def insert(op_ex: RelOldPersonExercise):
    """
    Inserts a new relation between an old person and an exercise into the database.

    Args:
      op_ex: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        session.add(op_ex)
        session.commit()


def select() -> List[RelOldPersonExercise]:
    """
    Returns all the relations between old persons and exercises from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonExercise).all()
        return relations


def select_by_id(op_id: int, ex_id: int) -> Optional[RelOldPersonExercise]:
    """
    Returns the relation between an old person and an exercise with the given IDs.

    Args:
      op_id: The ID of the old person.
      ex_id: The ID of the exercise.

    Returns:
      The relation with the given IDs, or `None` if no relation with those IDs is found.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonExercise, (op_id, ex_id))
        return relation


def update(op_ex: RelOldPersonExercise):
    """
    Updates a relation between an old person and an exercise in the database.

    Args:
      op_ex: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        current_relation = session.get(RelOldPersonExercise, (op_ex.id_old_person, op_ex.id_exercise))
        current_relation.exercise_hour = op_ex.exercise_hour
        session.commit()


def delete(op_id: int, ex_id: int):
    """
    Deletes the relation between an old person and an exercise with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      ex_id: The ID of the exercise.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonExercise, (op_id, ex_id))
        session.delete(relation)
        session.commit()
