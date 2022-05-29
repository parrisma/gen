import uuid
from copy import copy


class EntityId(str):
    """
    A globally unique id across all entities.
    """
    _id: str

    def __init__(self):
        self._id = str(uuid.uuid4().hex)
        return

    def as_str(self) -> str:
        """
        The EntityId
        :return: Entity Id as string
        """
        return copy(self._id)  # Ensure immutability of Id
