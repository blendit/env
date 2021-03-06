import numpy
from shapely.ops import cascaded_union
from src.exception import EnvironmentException
from src.feature import Feature


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
        self.models = self.tree.models

    def init_tree(self):
        '''Initialize the tree from the list of features'''
        # Initialize features as nodes
        # Feature which merge as 'blend' do not need any special node
        # First pass over "blend" objects, that will be backgrounds
        for feat in self.features[:]:
            if feat.interaction() == "blend":
                node = BlendNode([feat])
                self.features.remove(feat)
                self.features.append(node)

        # Second pass for others (Replace and Addition)
        for feat in self.features[:]:
            if not isinstance(feat, Node) and feat.interaction() != "blend":
                background = self.intersecting(feat, self.features)
                node = None
                
                if feat.interaction() == "replace":
                    node = ReplaceNode(background, feat)
                elif feat.interaction() == "addition":
                    node = AdditionNode(background, feat)
                    
                self.features.remove(background)
                if(feat != background):
                    self.features.remove(feat)
                self.features.append(node)

        # Construct the tree
        trees = []
        while len(self.features) > 1:
            a = self.features.pop()
            b = self.intersecting(a, self.features)

            if a == b:
                trees.append(a)
            else:  # There is a different feature intersecting
                self.features.remove(b)
                self.features.append(self.fusion_tree(a, b))

        if len(self.features) == 1:
            trees.append(self.features.pop())

        # Finally, set the disjoint trees as one unique tree
        self.tree = BlendNode(trees)
        self.models = self.tree.models
            
    def intersecting(self, node, node_list):
        """Returuns one node in the list that is intersecting the *node*. If none exists, returns the node."""
        for n in node_list:
            if n == node:
                continue
            if isinstance(n, Node) and node.intersect(n):
                return n
                
        return node

    def fusion_tree(self, a, b):
        if isinstance(a, ReplaceNode):
            a.add_child(b)
            return a
        elif isinstance(b, ReplaceNode):
            b.add_child(a)
            return b
        elif isinstance(a, AdditionNode):
            a.add_child(b)
            return a
        else:
            b.add_child(a)
            return b

    def z(self, pos):
        if self.tree is None:
            raise ValueError("Tree not initializated")
        else:
            return self.tree.z(pos)
        

class Node(Feature):
    '''Abstract class for nodes in the feature tree.
    Leaves of the tree are Feature and internal nodes must be specific nodes (Blend, Replace or Add).'''

    def __init__(self, children=[]):
        super(Node, self).__init__()
        
        self.children = []
        self.models = []
        for child in children:
            self.add_child(child)

    def add_child(self, child):
        self.children.append(child)
        self.shape = self.shape.union(child.shape)
        self.models += child.models

    def z(self, pos):
        '''Height at a given position'''
        return 0

    def influence(self, pos):
        '''Influence of at a given position'''
        return 0


class BlendNode(Node):
    '''Node that blends its children'''
    def z(self, pos):
        w = [c.influence(pos) for c in self.children if c.influence(pos) > 0]
        
        if len(pos) == 0 or len(w) == 0:
            return 0
        else:
            return numpy.average([c.z(pos) for c in self.children if c.influence(pos) > 0],
                                 weights=w)

    def influence(self, pos):
        if len(self.children) == 0:
            return 0
        else:
            return numpy.sum(c.influence(pos) for c in self.children)


class ReplaceNode(Node):
    '''Node that replaces an underlying feature with an other one'''

    def __init__(self, background, foreground):
        super(ReplaceNode, self).__init__()
        
        self.background = background
        self.foreground = foreground
        self.shape = background.shape
        self.shape = self.shape.union(foreground.shape)
        self.models = self.foreground.models
        # For models in background: keep only those which are not in the foreground
        for model in self.background.models:
            pos = model.pos
            if self.foreground.influence(pos) == 0:
                self.models.append(model)

    def z(self, pos):
        alpha = self.foreground.influence(pos)
        if alpha == 0:
            return self.background.z(pos)
        else:
            return (1 - alpha) * self.background.z(pos) + alpha * self.foreground.z(pos)

    def influence(self, pos):
        bg = self.background.influence(pos)
        if bg != 0:
            return bg
        else:
            return self.foreground.influence(pos)

    def add_child(self, node):
        self.background.add_child(node)
        self.shape = self.background.shape
        self.shape = self.shape.union(self.foreground.shape)
        self.models = []
        self.models += self.foreground.models
        # For models in background: keep only those which are not in the foreground
        for model in self.background.models:
            pos = model.pos
            if self.foreground.influence(pos) == 0:
                self.models.append(model)


class AdditionNode(Node):
    '''Node that adds a feature on top of another one'''

    def __init__(self, background, foreground):
        super(AdditionNode, self).__init__()
        
        self.background = background
        self.foreground = foreground
        self.shape = background.shape
        self.shape = self.shape.union(foreground.shape)
        self.models = self.background.models
        self.models += self.foreground.models

    def z(self, pos):
        alpha = self.foreground.influence(pos)
        if alpha == 0:
            return self.background.z(pos)
        else:
            return self.background.z(pos) + alpha * self.foreground.z(pos)

    def influence(self, pos):
        bg = self.background.influence(pos)
        if bg != 0:
            return bg
        else:
            return self.foreground.influence(pos)

    def add_child(self, node):
        self.background.add_child(node)
        self.shape = self.background.shape
        self.shape = self.shape.union(self.foreground.shape)
        self.models = []
        self.models += self.background.models
        self.models += self.foreground.models
