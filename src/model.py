class AbstractModel:
    """Abstract models class: defines a 3d model."""

    def __init__(self, path="", size=1, origin=(0, 0)):
        """* path : path to the 3d file of the model
        * size : resize factor of the model
        * origin : new origin (related to the original one, in the 3d file)"""
        self.path = path
        self.size = size
        self.origin = origin

        
class Model:
    """A model with (x,y) coordinates in the plane of the world."""

    def __init__(self, position=(0, 0), model=AbstractModel()):
        """* position : (x,y) coordinates in the world
        * model : AbstractModel, general model for this specific instance"""
        self.pos = position
        self.model = model
