#!/usr/bin/python
# coding=utf-8


import yaml

class ValidationError(Exception):
    pass

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

    def _wrap(self, obj, name):
        return wrap(obj)

    def _validate_get(self, param):
        pass
    def _validate_set(self, param, value):
        pass


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
        self._validate_get(nth)
        return self._wrap(self._objects[nth], nth)

    def __setitem__(self, nth, value):
        self._validate_set(nth, value)
        self._objects[nth] = value

    def __iter__(self):
        for n in self._objects:
            yield n
    def __len__(self):
        return len(self._objects)

    def append(self, x):
        self._validate_set(-1, x)
        self._objects.append(x)

    def __repr__(self):
        if len(self) > 5:
            return "ListMixin instance with %d items"%(len(self._objects),)

        s = ','.join([repr(self._wrap(obj, i)) for i, obj in enumerate(self._objects)])
        return '[' +  s + ']'

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
        self._validate_get(name)
        return self._wrap(self._objects.get(name), name)

    def __getitem__(self, name):
        self._validate_get(name)
        return self._wrap(self.__dict__["_objects"][name], name)

    def __setattr__(self, name, value):
        self._validate_set(name, value)
        self.__dict__["_objects"][name] = value

    def __setitem__(self, name, value):
        self._validate_set(name, value)
        self.__dict__["_objects"][name] = value

    def __repr__(self):
        assert isinstance(self._objects, dict)
        n = getattr(self._objects, "name", None)
        if n is None:
            return "%s"%(self.__keys__(),)
        return n


class YamlDict(DictMixin, YamlProxy):
    pass


class YSchemaProxy(YamlProxy):
    def __init__(self, obj):
        YamlProxy.__init__(self, obj)

class YSchemaList(ListMixin, YSchemaProxy):
    hometype = None
    #FIXME should have wrapper/wrappee pair
    def _wrap(self, obj, nth):
        k = self.schema.get_class(self.hometype)
        return k(obj)

    def _validate_set(self, param, value):
        k = self.schema.get_class(self.hometype)
        assert isinstance(value, k)

class YSchemaDict(DictMixin, YSchemaProxy):
    field = ()
    def _wrap(self, obj, name):
        kname = self.field.get(name, None)
        if kname is None:
            kname = self.field.get("*", None)
            if kname is None:
                raise ValidationError 

        k = self.schema.get_class(kname)
        return k(obj)

    def _validate_get(self, param):
        if param not in self.__class__.field:
            print param
            print self.__class__.field
            raise ValidationError, "%s got %s, %s"%(self, param, self.__class__.field)

    def _validate_set(self, param, value):
        if param not in self.__class__.field:
            raise ValidationError, "%s got %s, for %s, in  %s"%(self, param, value, self.__class__.field)


class YSchema(object):
    def __init__(self, f):
        self.kls = {}
        YSchemaProxy.schema = self #FIXME
        """
        Dynamic gen. of classes?
        """

    def get_class(self, name, default=None):
        if default is None:
            return self.kls[name]
        else:
            return self.kls.get(name, default)

    def wrap_as_root(self, x):
        k = self.get_class("Root")
        return k(x)

    def bind(self, as_name=None):
        def foo(kls):
            if as_name is None:
                name = kls.__name__
            else:
                name = as_name
            #print "binding", name, kls
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

