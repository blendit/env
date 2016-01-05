class Resource:
    """Resources class"""

    def __init__(self):
        """Currently, one resource = the path to this model (then, we will import in blender these models)
        Types: object, texture, ...?"""
        self.path = ""
        self.types = "UNKNOWN" 
