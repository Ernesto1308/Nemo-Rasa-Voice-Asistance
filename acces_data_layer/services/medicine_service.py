from typing import Optional, List, Any
from sqlalchemy.orm import Session
from acces_data_layer.models.models import Medicine
from acces_data_layer.services import engine


def insert(medicine_data: Any) -> None:
    """
    Inserts a new medicine into the database.

    Args:
        medicine_data: The Medicine object to insert

    Returns:
        None

    Description:
        Opens a SQLAlchemy session. Adds the Medicine object.
        Commits change to persist in the database.
    """
    with Session(engine) as session:
        medicine = Medicine(**medicine_data)
        session.add(medicine)
        session.commit()


def select_all() -> List[dict]:
    """
    Gets all medicines from the database.

    Args:
        None

    Returns:
        medicines: List of Medicine objects

    Description:
        Opens a SQLAlchemy session. Queries for all Medicine rows.
        Returns them in a list.
    """
    with Session(engine) as session:
        medicines = session.query(Medicine).all()
        medicines_dict = [medicine.to_dict() for medicine in medicines]
        return medicines_dict


def select_by_id(id_medicine: int) -> dict:
    """
    Gets a medicine by ID.

    Args:
        id_medicine: The ID of the medicine

    Returns:
        medicine: The Medicine object with the given ID, or None if not found

    Description:
        Opens a SQLAlchemy session. Queries for Medicine with matching ID.
        Returns Medicine if found, otherwise returns None.
    """
    with Session(engine) as session:
        medicine = session.get(Medicine, id_medicine).to_dict()
        return medicine


def select_by_name(medicine: str) -> int:
    """
    Gets a medicine by name.

    Args:
        medicine: The medicine name

    Returns:
        medicine: The Medicine object with the given name, or None if not found

    Description:
        Opens a SQLAlchemy session. Queries for Medicine with matching name.
        Returns Medicine if found, otherwise returns None.
    """
    with Session(engine) as session:
        query = session.query(Medicine).filter_by(medicine_name=medicine)
        result = query.first()
        return result.id_medicine if result else None


def update(medicine_data: Any):
    """
    Updates an existing medicine.

    Args:
        medicine_data: The Medicine object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Medicine by ID.
        Sets its fields to the passed Medicine object. Commits changes.
    """
    with Session(engine) as session:
        medicine = Medicine(**medicine_data)
        current_medicine = session.get(Medicine, medicine.id_medicine)
        current_medicine.medicine_name = medicine.medicine_name
        session.commit()


def delete(id_medicine: int):
    """
    Deletes a medicine by ID.

    Args:
        id_medicine: The ID of the medicine to delete

    Returns:
        None

    Description:
        Opens SQLAlchemy session. Gets existing Medicine by ID.
        Deletes from session. Commits changes.
    """
    with Session(engine) as session:
        medicine = session.get(Medicine, id_medicine)
        session.delete(medicine)
        session.commit()
