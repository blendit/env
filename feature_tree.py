import numpy
from exception import EnvironmentException


class IntersectError(EnvironmentException):
    """Error intersecting two incompatible features."""
    def __init__(self, msg="Intersecting two incompatible features"):
        self.msg = msg


class FeatureTree:
    '''Tree structure for features'''
    def __init__(self, features):
        self.features = list(features)
        self.tree = None
        self.init_tree()

    def init_tree(self):
        '''Initialize the tree from the list of features'''
        for feature in self.features:
            if feature.interaction() == "blend":
                continue  # We don't care about blend nodes, they will be at the top of the tree anyway

            intersect = []
            intersect_type = "blend"
            for feature2 in self.features:  # Search for intersections
                if feature.intersect(feature2):
                    intersect.append(feature2)
                    if feature2.interaction() != "blend":
                        if intersect_type != blend:
                            raise IntersectError()
                        else:
                            intersect_type = feature2.interaction()
        pass


class Node(Feature):
    '''Abstract class for nodes in the feature tree.
    Leaves of the tree are Feature and internal nodes must be specific nodes (Blend, Replace or Add).'''

    def z(self, pos):
        '''Height at a given position'''
        pass

    def influence(self, pos):
        '''Influence of at a given position'''
        pass


class BlendNode(Node):
    '''Node that blends its children'''

    def __init__(self, children):
        self.children = list(children)

    def z(self, pos):
        return numpy.average((c.z(pos) for c in self.children),
                             weight=(c.influence(pos) for c in self.children))

    def influence(self, pos):
        return numpy.sum(c.influence(pos) for c in self.children)


class ReplaceNode(Node):
    '''Node that replaces an underlying feature with an other one'''

    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground

    def z(self, pos):
        alpha = self.foreground.influence(pos)
        return (1 - alpha) * self.background.z(pos) + alpha * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)


class AdditionNode(Node):
    '''Node that adds a feature on top of another one'''

    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground

    def z(self, pos):
        return self.background.z(pos) + self.foreground.influence(pos) * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)
