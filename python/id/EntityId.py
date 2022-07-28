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

    def __eq__(self,
               other):
        if isinstance(other, EntityId):
            if self._id == other._id:
                return True
        return False

    def __str__(self) -> str:
        """
        String representation of the entity Id
        :return: The entity id as string
        """
        return self.as_str()

    def __repr__(self) -> str:
        return self.as_str()
