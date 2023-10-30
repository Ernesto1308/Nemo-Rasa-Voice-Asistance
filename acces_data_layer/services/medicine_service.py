from typing import List, Any

from sqlalchemy import select

from acces_data_layer.models.models import Medicine
from acces_data_layer.services import Session


def insert(medicine_data: Any) -> None:
    """
    Inserts a new medicine into the database.

    Args:
        medicine_data: The Medicine object to insert

    Returns:
        None

    Description:
        Opens a SQLAlchemy Session. Adds the Medicine object.
        Commits change to persist in the database.
    """
    medicine = Medicine(**medicine_data)
    Session.add(medicine)
    Session.commit()


def select_all() -> List[dict]:
    """
    Gets all medicines from the database.

    Args:
        None

    Returns:
        medicines: List of Medicine objects

    Description:
        Opens a SQLAlchemy Session. Queries for all Medicine rows.
        Returns them in a list.
    """
    medicines = Session.scalars(select(Medicine)).all()
    medicines_dict = [medicine.to_dict() for medicine in medicines]

    return medicines_dict


def select_by_id(id_medicine: int) -> dict:
    """
    Gets a medicine by ID.

    Args:
        id_medicine: The ID of the medicine

    Returns:
        medicine: The Medicine object found
    Description:
    Opens a SQLAlchemy Session. Queries for Medicines Medicine if found, otherwise returns None.
"""
    medicine = Session.get(Medicine, id_medicine).to_dict()
    return medicine


def select_by_name(medicine_name: str) -> int:
    """
    Gets a medicine by name.

    Args:
        medicine_name: The medicine name

    Returns:
        medicine: The Medicine object not found
    Description:
    Opens a SQLAlchemy Session. Queries for Medicines if found, otherwise returns None.
"""
    result = Session.scalars(
         select(Medicine).filter_by(medicine_name=medicine_name).limit(1)
    ).first()

    return result.id_medicine if result else None


def update(medicine_data: Any):
    """
    Updates an existing medicine.

    Args:
        medicine_data: The Medicine object to update

    Returns:
        None

    Description:
        Opens SQLAlchemy Session. Gets existing Medicine by ID.
        Sets its fields to the passed Medicine object. Commits changes.
    """
    medicine = Medicine(**medicine_data)
    current_medicine = Session.get(Medicine, medicine.id_medicine)
    current_medicine.medicine_name = medicine.medicine_name
    Session.commit()


def delete(id_medicine: int):
    """
    Deletes a medicine by ID.

    Args:
        id_medicine: The ID of the medicine to delete

    Returns:
        None

    Description:
        Opens SQLAlchemy Session. Gets existing Medicine by ID.
        Deletes from Session. Commits changes.
    """
    medicine = Session.get(Medicine, id_medicine)
    Session.delete(medicine)
    Session.commit()
