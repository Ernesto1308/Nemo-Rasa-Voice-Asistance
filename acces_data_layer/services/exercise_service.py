from typing import Optional, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import Exercise
from acces_data_layer.services import engine


def insert(exercise: Exercise):
    """
    Inserts a new exercise into the database.

    Args:
        exercise: The Exercise object to insert

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Adds exercise object.
        Commits to persist in database.
    """
    with Session(engine) as session:
        session.add(exercise)
        session.commit()


def select() -> List[Exercise]:
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
        return exercises


def select_by_id(id_exercise: int) -> Optional[Exercise]:
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
        exercise = session.get(Exercise, id_exercise)
        return exercise


def update(exercise: Exercise):
    """
    Updates an existing exercise.

    Args:
        exercise: The Exercise object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Exercise by ID.
        Sets field to passed Exercise object. Commits changes.
    """
    with Session(engine) as session:
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
