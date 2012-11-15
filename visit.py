#!/usr/bin/python
# coding=utf-8

import yaml

class Visitor(object):
    def __init__(self, loader):
        self.loader = loader

    def handleScalarNode(self, sn):
        prefix = u'tag:yaml.org,2002:'
        mapping = {
            'null':lambda x : None,
            'int': int,
            'str': str,
            }
        rest, tail = sn.tag.rsplit(':', 1)
        return mapping[tail](sn.value)

    def handleSequenceNode(self, sn):
        return [self.dispatch(v) for v in sn.value]
    
    def handleMappingNode(self, sn):
        vs = getattr(sn, "value", None)
        return dict([
            (self.dispatch(k), self.dispatch(v))
            for k, v in vs])

    def dispatch(self, node):
        #print "dispatch", node
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
        return v.dispatch(node)
    yaml.add_constructor(u"Root", from_yaml)
    yaml.add_path_resolver(u"Root", [], dict)
    yaml.add_path_resolver(u"Root", [], list)

# Do I need these?
#yaml.add_path_resolver(u"Root", [], str)
#yaml.add_path_resolver(u"Root", [], int)
#yaml.add_path_resolver(u"Root", [], None)


