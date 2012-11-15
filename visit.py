#!/usr/bin/python
# coding=utf-8

import yaml

class Visitor(object):
    prefix = u'tag:yaml.org,2002:'
    mapping = {
        'null':lambda x : None,
        'int': int,
        'str': str,
        }

    def __init__(self, loader):
        self.loader = loader
        self.history = {}


    def handleScalarNode(self, sn):
        rest, tail = sn.tag.rsplit(':', 1)
        n = self.mapping[tail](sn.value)
        self.history[sn] = n
        return n

    def handleSequenceNode(self, sn):
        n = []
        self.history[sn] = n
        n.extend([self.visit(v) for v in sn.value])
        return n
    
    def handleMappingNode(self, sn):
        n = {}
        self.history[sn] = n
        vs = getattr(sn, "value", None)
        n.update([
            (self.visit(k), self.visit(v))
            for k, v in vs])
        return n

    def visit(self, node):
        try:
            return self.history[node]
        except:
            pass

        if isinstance(node, yaml.nodes.ScalarNode):
            return self.handleScalarNode(node)
        elif isinstance(node, yaml.nodes.MappingNode):
            return self.handleMappingNode(node)
        elif isinstance(node, yaml.nodes.SequenceNode):
            return self.handleSequenceNode(node)
        else:
            print "Unknown node", node.__class__
        assert False


def inject(vclass):
    def from_yaml(loader, node):
        #print "from_yaml"
        v = vclass(node)
        return v.visit(node)
    """
      visit every thing!
    """
    yaml.add_constructor(u"Root", from_yaml)
    yaml.add_path_resolver(u"Root", [], dict)
    yaml.add_path_resolver(u"Root", [], list)

    # These are not, since we "override" only dict/list
    # yaml.add_path_resolver(u"Root", [], str)
    # yaml.add_path_resolver(u"Root", [], None)


