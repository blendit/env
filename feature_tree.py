import numpy
from shapely.ops import cascaded_union
from feature import Feature
from exception import EnvironmentException


class IntersectError(EnvironmentException):
    """Error intersecting two incompatible features."""
    def __init__(self, msg="Intersecting two incompatible features"):
        self.msg = msg


class FeatureTree:
    '''Tree structure for features'''
    def __init__(self, features):
        self.features = set(features)
        self.trees = []
        self.init_tree()

    def init_tree(self):
        '''Initialize the tree from the list of features'''
        # Initialize features as nodes
        # Feature which merge as 'blend' do not need any special node
        for feat in self.features:
            if feat.interaction() != "blend":
                background = intersecting(feat, self.features)
                node = None

                if feat.ineraction() == "replace":
                    node = ReplaceNode(background, feat)
                elif feat.interaction() == "addition":
                    node = AdditionNode(background, feat)
                
                self.features.remove(background)
                self.features.remove(feat)
                self.features.append(node)
        
        # Construct the tree
        while len(self.features) > 1:
            a = self.features.pop()
            b = intersecting(a, self.features)

            if a == b:
                trees.append(a)
            else:  # There is a different feature intersecting
                self.features |= {fusion_tree(a, b)}

        # Finally, set the disjoint trees as one unique tree
        self.tree = BlendNode(self.trees)
            
    def intersecting(self, node, node_list):
        """Returuns one node in the list that is intersecting the *node*. If none exists, returns the node."""
        for n in node_list:
            if node.intersect(n):
                return n
                
        return node

    def fusion_tree(a, b):
        if isinstance(a, ReplaceNode) or isinstance(a, AdditionNode):
            a.add_child(b)
        else:
            b.add_child(a)
        

class Node(Feature):
    '''Abstract class for nodes in the feature tree.
    Leaves of the tree are Feature and internal nodes must be specific nodes (Blend, Replace or Add).'''

    def __init__(self, children=[]):
        super(Node, self).__init__()
        
        self.children = []
        for child in children:
            self.add_child(child)

    def add_child(self, child):
        self.children.append(child)
        self.shape = self.shape.union(child.shape)

    def z(self, pos):
        '''Height at a given position'''
        pass

    def influence(self, pos):
        '''Influence of at a given position'''
        pass


class BlendNode(Node):
    '''Node that blends its children'''

    def z(self, pos):
        return numpy.average([c.z(pos) for c in self.children],
                             weights=[c.influence(pos) for c in self.children])

    def influence(self, pos):
        return numpy.sum(c.influence(pos) for c in self.children)


class ReplaceNode(Node):
    '''Node that replaces an underlying feature with an other one'''

    def __init__(self, background, foreground):
        super(ReplaceNode, self).__init__()
        
        self.background = background
        self.foreground = foreground
        self.shape = background.shape
        self.shape = self.shape.union(foreground.shape)

    def z(self, pos):
        alpha = self.foreground.influence(pos)
        return (1 - alpha) * self.background.z(pos) + alpha * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)

    def add_child(self, node):
        self.background.add_child(node)


class AdditionNode(Node):
    '''Node that adds a feature on top of another one'''

    def __init__(self, background, foreground):
        super(AdditionNode, self).__init__()
        
        self.background = background
        self.foreground = foreground
        self.shape = background.shape
        self.shape = self.shape.union(foreground.shape)

    def z(self, pos):
        return self.background.z(pos) + self.foreground.influence(pos) * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)
