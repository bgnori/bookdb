#!/usr/bin/python
# coding=utf-8

"""
 add_constructor(tag, constructor) specifies a constructor for the given tag. A constructor is a function that converts a node of a YAML representation graph to a native Python object. A constructor accepts an instance of Loader and a node and returns a Python object.
"""

"""
add_multi_constructor(tag_prefix, multi_constructor) specifies a multi_constructor for the given tag_prefix. A multi-constructor is a function that converts a node of a YAML representation graph to a native Python object. A multi-constructor accepts an instance of Loader, the suffix of the node tag, and a node and returns a Python object. 
"""


"""
 add_implicit_resolver(tag, regexp, first) adds an implicit tag resolver for plain scalars. If the scalar value is matched the given regexp, it is assigned the tag. first is a list of possible initial characters or None.

"""
"""
add_path_resolver(tag, path, kind) adds a path-based implicit tag resolver. A path is a list of keys that form a path to a node in the representation graph. Paths elements can be string values, integers, or None. The kind of a node can be str, list, dict, or None.
"""
"""
import yaml


def util():
  books  = {}
  def BooksBuilder(loader, node):
    books[0] = []
    return books[0]

  def BookBuilder(loader, node):
    books[0].append("mybook")
    return "BookBuilder"
  return BooksBuilder, BookBuilder

with file("sample.yaml") as f:
  sample = f.read()

p = util()

yaml.add_constructor("Books", p[0])
yaml.add_path_resolver("Books", ["Books"], list)
yaml.add_constructor("Book", p[1])
yaml.add_path_resolver("Book", ["Books", None, ], dict)
y = yaml.load(sample)

print y['Books']
print "done."
"""
from yaml import YAMLObject, Loader, Dumper
import yaml


class Books(YAMLObject):
    yaml_loader = Loader
    yaml_dumper = Dumper
    tag = u'Books'
    @classmethod
    def from_yaml(cls, loader, node):
        #print "Books::from_yaml"
        print type(node.value)
        return [""]

class Book(YAMLObject):
    yaml_loader = Loader
    yaml_dumper = Dumper
    tag = u'Book'

    @classmethod
    def from_yaml(cls, loader, node):
        d = dict([(a.value, b.value) for a, b in node.value])
        print d["isbn"]
        return d #isbn #'mybook'

    @classmethod
    def to_yaml(cls, dumper, data):
        # ...
        return node

#yaml.add_constructor("Books", Books.from_yaml)
#yaml.add_path_resolver(u"Books", [u"Books"], list)
yaml.add_constructor("Book", Book.from_yaml)
yaml.add_path_resolver(u"Book", ["list", None, ], dict)

with file("sample.yaml") as f:
  y = yaml.load(f.read())
print y

