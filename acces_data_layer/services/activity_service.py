from typing import Optional, List, Any
from sqlalchemy.orm import Session
from acces_data_layer.models.models import Activity
from acces_data_layer.services import engine


def insert(activity_data: Any):
    """
    Inserts a new activity into the database.

    Args:
        activity_data: The Activity object to insert

    Returns:
        None

    Description:
        Opens a SQLAlchemy session. Adds the Activity object to the session.
        Commits the changes to persist the new activity in the database.
    """
    with Session(engine) as session:
        activity = Activity(**activity_data)
        session.add(activity)
        session.commit()


def select_all() -> List[dict]:
    """
    Gets all activities from the database.

    Args:
        None

    Returns:
        activities: List of Activity objects

    Description:
        Opens a SQLAlchemy session. Performs a query for all Activity objects.
        Returns them in a list.
    """
    with Session(engine) as session:
        activities = session.query(Activity).all()
        activities_dict = [activity.to_dict() for activity in activities]
        return activities_dict


def select_by_id(id_activity: int) -> dict:
    """
    Gets an activity by ID.

    Args:
        id_activity: The ID of the activity

    Returns:
        activity: The Activity object with the matching ID, or None if not found

    Description:
        Opens a SQLAlchemy session. Queries for an Activity with the given ID.
        Returns the Activity if found, otherwise returns None.
    """
    with Session(engine) as session:
        activity = session.get(Activity, id_activity).to_dict()
        return activity


def update(activity_data: Any):
    """
    Updates an existing activity.

    Args:
        activity_data: The Activity object to update

    Returns:
        None

    Description:
        Opens a SQLAlchemy session. Gets the existing Activity by ID.
        Sets its fields to the passed Activity object. Commits changes.
    """
    with Session(engine) as session:
        activity = Activity(**activity_data)
        current_activity = session.get(Activity, activity.id_activity)
        current_activity.activity_name = activity.activity_name
        session.commit()


def delete(id_activity: int):
    """
    Deletes an activity by ID.

    Args:
        id_activity: The ID of the activity to delete

    Returns:
        None

    Description:
        Opens a SQLAlchemy session. Gets the existing Activity by ID.
        Deletes the Activity from the session. Commits changes.
    """
    with Session(engine) as session:
        activity = session.get(Activity, id_activity)
        session.delete(activity)
        session.commit()
