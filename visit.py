#!/usr/bin/python
# coding=utf-8

import yaml

class Visitor(object):
    def __init__(self, loader):
        self.loader = loader

    def handleScalarNode(self, sn):
        """
        >>> yaml.load('1')
        1
        >>> yaml.load("'a'")
        'a'
        >>> yaml.load('') is None
        True
        """
        prefix = u'tag:yaml.org,2002:'
        mapping = {
            'null':lambda x : None,
            'int': int,
            'str': str,
            }
        rest, tail = sn.tag.rsplit(':', 1)
        return mapping[tail](sn.value)

    def handleSequenceNode(self, sn):
        """
        >>> _foo
        1
        >>> yaml.load('[]')
        []
        >>> isinstance(yaml.load('[]'), list)
        True
        >>> yaml.load('[0]')
        [0]
        >>> isinstance(yaml.load('[0]'), list)
        True
        >>> yaml.load('[0, "a"]')
        [0, 'a']
        """
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


def from_yaml(loader, node):
    print "from_yaml"
    v = Visitor(node)
    return v.dispatch(node)


yaml.add_constructor(u"Root", from_yaml)
yaml.add_path_resolver(u"Root", [], dict)
yaml.add_path_resolver(u"Root", [], list)

_foo = 1

if False:
    with file("sample.yaml") as f:
        y = yaml.load(f.read())

if False:
    y = yaml.load('''
        key-foo: 'value-foo'
        key-bar: 'value-bar'
        array: [1, 2, 3]''')
    print y

if True:
    y = yaml.load('''&A [*A] ''')
    print y

