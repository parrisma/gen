from python.id.EntityId import EntityId


class GeneId(EntityId):
    """
    The globally unique Id of a Gene
    """

    def __init__(self):
        super().__init__()
        return

    def __eq__(self,
               other):
        return super().__eq__(other)
