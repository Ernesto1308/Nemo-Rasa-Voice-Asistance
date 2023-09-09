from typing import Optional, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import Feeding
from acces_data_layer.services import engine


def insert(feeding: Feeding):
    """
    Inserts a new feeding into the database.

    Args:
        feeding: The Feeding object to insert

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Adds feeding object.
        Commits to persist in database.
    """
    with Session(engine) as session:
        session.add(feeding)
        session.commit()


def select() -> List[Feeding]:
    """
    Gets all feedings from the database.

    Args:
        None

    Returns:
        feedings: List of Feeding objects

    Description:
        Opens SQLAlchemy session. Queries for all Feeding rows.
        Returns them in a list.
    """
    with Session(engine) as session:
        feedings = session.query(Feeding).all()
        return feedings


def select_by_id(id_feeding: int) -> Optional[Feeding]:
    """
    Gets a feeding by ID.

    Args:
        id_feeding: The ID of the feeding

    Returns:
        feeding: The Feeding object with the given ID, or None if not found

    Description:
        Opens SQLAlchemy session. Queries for Feeding with matching ID.
        Returns Feeding if found, otherwise returns None.
    """
    with Session(engine) as session:
        feeding = session.get(Feeding, id_feeding)
        return feeding


def update(feeding: Feeding):
    """
    Updates an existing feeding.

    Args:
        feeding: The Feeding object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Feeding by ID.
        Sets field to passed Feeding object. Commits changes.
    """
    with Session(engine) as session:
        current_feeding = session.get(Feeding, feeding.id_feeding)
        current_feeding.feeding_name = feeding.feeding_name
        session.commit()


def delete(id_feeding: int):
    """
    Deletes a feeding by ID.

    Args:
        id_feeding: The ID of the feeding to delete

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Feeding by ID.
        Deletes from session. Commits changes.
    """
    with Session(engine) as session:
        feeding = session.get(Feeding, id_feeding)
        session.delete(feeding)
        session.commit()
