from typing import List, Any

from sqlalchemy.orm import Session

from acces_data_layer.models.models import Exercise
from acces_data_layer.services import engine


def insert(exercise_data: Any):
    """
    Inserts a new exercise into the database.

    Args:
        exercise_data: The Exercise object to insert

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Adds exercise object.
        Commits to persist in database.
    """
    with Session(engine) as session:
        exercise = Exercise(**exercise_data)
        session.add(exercise)
        session.commit()


def select_all() -> List[dict]:
    """
    Gets all exercises from the database.

    Args:
        None

    Returns:
        exercises: List of Exercise objects

    Description:
        Opens SQLAlchemy session. Queries for all Exercise rows.
        Returns them in a list.
    """
    with Session(engine) as session:
        exercises = session.query(Exercise).all()
        exercises_dict = [exercise.to_dict() for exercise in exercises]
        return exercises_dict


def select_by_id(id_exercise: int) -> dict:
    """
    Gets an exercise by ID.

    Args:
        id_exercise: The ID of the exercise

    Returns:
        exercise: The Exercise object with the given ID, or None if not found

    Description:
        Opens SQLAlchemy session. Queries for Exercise with matching ID.
        Returns Exercise if found, otherwise returns None.
    """
    with Session(engine) as session:
        exercise = session.get(Exercise, id_exercise).to_dict()
        return exercise


def update(exercise_data: Any):
    """
    Updates an existing exercise.

    Args:
        exercise_data: The Exercise object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Exercise by ID.
        Sets field to passed Exercise object. Commits changes.
    """
    with Session(engine) as session:
        exercise = Exercise(**exercise_data)
        current_exercise = session.get(Exercise, exercise.id_exercise)
        current_exercise.exercise_name = exercise.exercise_name
        session.commit()


def delete(id_exercise: int):
    """
    Deletes an exercise by ID.

    Args:
        id_exercise: The ID of the exercise to delete

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Exercise by ID.
        Deletes from session. Commits changes.
    """
    with Session(engine) as session:
        exercise = session.get(Exercise, id_exercise)
        session.delete(exercise)
        session.commit()
