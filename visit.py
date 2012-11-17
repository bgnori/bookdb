#!/usr/bin/python
# coding=utf-8

import yaml

class Visitor(object):
    prefix = u'tag:yaml.org,2002:'
    mapping = {
        'null':lambda x : None,
        'int': int,
        'str': str,
        'bool': bool,
        'value': str, #FIXME
        }

    def __init__(self, loader):
        self.loader = loader
        self.history = {}
        self.cwp = [] #current working path


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

    def _visit(self, node):
       if isinstance(node, yaml.nodes.ScalarNode):
           return self.handleScalarNode(node)
       elif isinstance(node, yaml.nodes.MappingNode):
           return self.handleMappingNode(node)
       elif isinstance(node, yaml.nodes.SequenceNode):
           return self.handleSequenceNode(node)
       else:
           print "Unknown node", node.__class__
           assert False

    def push(self, node):
        self.cwp.append(node)

    def pop(self, node):
        p = self.cwp.pop(-1)
        assert node == p

    def getcwp(self):
        return self.cwp

    def visit(self, node):
        self.push(node)
        try:
            n = self.history[node]
        except:
            n = self._visit(node)
        self.pop(node)
        return n


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

def find(path, node):
    '[]'
    xs = path.split("/")
    
    n = node
    for x in xs:
        if not x:
            continue
        try:
            ik = int(x)
        except:
            ik = x
        n = n[ik]
    return n




