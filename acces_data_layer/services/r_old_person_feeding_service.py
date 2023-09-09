from typing import Optional, List
from sqlalchemy.orm import Session
from acces_data_layer.models.models import RelOldPersonFeeding
from acces_data_layer.services import engine


def insert(op_feed: RelOldPersonFeeding):
    """
    Inserts a new relation between an old person and a feeding into the database.

    Args:
      op_feed: The relation to insert.

    Returns:
      None.
    """

    with Session(engine) as session:
        session.add(op_feed)
        session.commit()


def select() -> List[RelOldPersonFeeding]:
    """
    Returns all the relations between old persons and feedings from the database.

    Returns:
      A list of relations.
    """

    with Session(engine) as session:
        relations = session.query(RelOldPersonFeeding).all()
        return relations


def select_by_id(op_id: int, feed_id: int) -> Optional[RelOldPersonFeeding]:
    """
    Returns the relation between an old person and a feeding with the given IDs.

    Args:
      op_id: The ID of the old person.
      feed_id: The ID of the feeding.

    Returns:
      The relation with the given IDs, or `None` if no relation with those IDs is found.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonFeeding, (op_id, feed_id))
        return relation


def update(op_feed: RelOldPersonFeeding):
    """
    Updates a relation between an old person and a feeding in the database.

    Args:
      op_feed: The relation to update.

    Returns:
      None.
    """

    with Session(engine) as session:
        current_relation = session.get(RelOldPersonFeeding, (op_feed.id_old_person, op_feed.id_feeding))
        current_relation.feeding_hour = op_feed.feeding_hour
        session.commit()


def delete(op_id: int, feed_id: int):
    """
    Deletes the relation between an old person and a feeding with the given IDs from the database.

    Args:
      op_id: The ID of the old person.
      feed_id: The ID of the feeding.

    Returns:
      None.
    """

    with Session(engine) as session:
        relation = session.get(RelOldPersonFeeding, (op_id, feed_id))
        session.delete(relation)
        session.commit()
