#!/usr/bin/python
# coding=utf-8


import yaml

def wrap(x):
    u"""
    Todo: Schema support
    >>> f = file("sample.yaml")
    >>> y = yaml.load(f)
    >>> p = wrap(y)
    >>> p.Tags.Category.Cooking[0].isbn
    '4873115094'
    >>> p.Tags.Category.Cooking[0].title
    u'Cooking for Geeks: 料理の科学と実践レシピ'

    #print x["Tags"]["Category"]["Cooking"][0]["title"]
    """
    if isinstance(x, list):
        return YamlList(x)
    if isinstance(x, dict):
        return YamlDict(x)
    return x 


class YamlProxy(object):
    def __init__(self, obj):
        assert obj is not None
        self.__dict__["_objects"] = obj

    def __repr__(self):
        return "YamlProxy instance with %s"%(self._objects,)

    def wrap(self, obj):
        return wrap(obj)

class ListMixin(object):
    """
    >>> p = wrap(yaml.load("[0, 100, 2]"))
    >>> p[0]
    0
    >>> p[1]
    100
    >>> p[-1]
    2
    """
    def __getitem__(self, nth):
        return self.wrap(self._objects[nth])

    def __setitem__(self, nth, value):
        self._objects[nth] = value

    def __iter__(self):
        for n in self._objects:
            yield n
    def __len__(self):
        return len(self._objects)

    def append(self, x):
        self._objects.append(x)

    def __repr__(self):
        return "ListMixin instance with %d items"%(len(self._objects),)

class YamlList(ListMixin, YamlProxy):
    pass

class DictMixin(object):
    """
    >>> p = wrap(yaml.load("isbn: 'this is isbn'"))
    >>> p.isbn
    'this is isbn'
    >>> p.title = "this is title"
    >>> p.title
    'this is title'
    """
    def __keys__(self):
        assert isinstance(self._objects, dict)
        return self._objects.keys()

    def __getattr__(self, name):
        return self.wrap(self._objects.get(name))

    def __getitem__(self, name):
        return self.wrap(self.__dict__["_objects"][name])

    def __setattr__(self, name, value):
        self.__dict__["_objects"][name] = value

    def __setitem__(self, name, value):
        self.__dict__["_objects"][name] = value

    def __repr__(self):
        assert isinstance(self._objects, dict)
        return "%s"%(self.__keys__(),)

class YamlDict(DictMixin, YamlProxy):
    pass

class YSchemaProxy(YamlProxy):
    schema = None
    def wrap(self, obj):
        return self.schema.wrap(obj)
    def path(self):
        return self.path

class YSchemaList(ListMixin, YSchemaProxy):
    pass

class YSchemaDict(DictMixin, YSchemaProxy):
    pass

class YSchema(object):
    def __init__(self, f):
        self.kls = {}
        YSchemaProxy.schema = self #FIXME
        """
        Dynamic gen. of classes?
        """

    def wrap(self, x, path=None):
        #print "YSchema", x
        if path is None:
            p = "/"
        else:
            p = path
        if isinstance(x, list):
            return YSchemaList(x)
        if isinstance(x, dict):
            return YSchemaDict(x)
        return x 

    def bind(self, as_name=None):
        def foo(kls):
            if as_name is None:
                name = kls.__name__
            else:
                name = as_name
            print "binding", name, kls
            self.kls[name] = kls
            return kls
        return foo

class Validator(object):
    """
    Kwailify
    http://jp.rubyist.net/magazine/?0012-YAML

     make Kwalipy??

    http://pyyaml.org/wiki/YAMLSchemaDiscussion

    """
    pass

