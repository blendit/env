import numpy


class FeatureTree:
    '''Tree structure for features'''
    def __init__(self, features):
        self.features = list(features)
        self.tree = None
        self.init_tree()

    def init_tree(self):
        '''Initialize the tree from the list of features'''
        # TODO
        pass


def Node:
    '''Abstract class for nodes in the feature tree'''

    def z(self, pos):
        '''Height at a given position'''
        pass

    def influence(self, pos):
        '''Influence of at a given position'''
        pass


class BlendNode:
    '''Node that blends its children'''

    def __init__(self, children):
        self.children = list(children)

    def z(self, pos):
        return numpy.average((c.z(pos) for c in self.children),
                             weight=(c.influence(pos) for c in self.children))

    def influence(self, pos):
        return numpy.sum(c.influence(pos) for self.children)


class ReplaceNode:
    '''Node that replaces an underlying feature with an other one'''

    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground

    def z(self, pos):
        alpha = self.foreground.influence(pos)
        return (1 - alpha) * self.background.z(pos) + alpha * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)


class AdditionNode:
    '''Node that adds a feature on top of another one'''

    def __init__(self, background, foreground):
        self.background = background
        self.foreground = foreground

    def z(self, pos):
        return self.background.z(pos) + self.foreground.influence(pos) * self.foreground.z(pos)

    def influence(self, pos):
        return self.background.influence(pos)
