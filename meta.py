#!/usr/bin/python
# coding=utf-8


import yaml

"""
f = "fooo"
g = "gooo"
zm = [f, g]

print yaml.dump([zm, zm])

with file("sample.yaml") as f:
    x = yaml.load(f)

#print x
print x["Tags"]["Category"]["Cooking"][0]["title"]
"""

u"""
>>> f = file("sample.yaml")
>>> y = yaml.load(f)
>>> p = wrap(y)
>>> p.Tags.Category.Cooking[0].isbn
'4873115094'
>>> p.Tags.Category.Cooking[0].title.decode("utf8")
u'Cooking for Geeks: 料理の科学と実践レシピ'

another sample
>>> p = wrap(yaml.load("isbn: 'this is isbn'"))
>>> p.isbn
'this is isbn'
"""

def wrap(x):
    """
    Todo: Schema support
    """
    if isinstance(x, list):
        return YamlProxyList(x)
    if isinstance(x, dict):
        return YamlProxyDict(x)
    return x 


class YamlProxy(object):
    def __init__(self, obj):
        assert obj is not None
        self.__dict__["_objects"] = obj

    def __repr__(self):
        return "YamlProxy instance with %s"%(self._objects,)

class YamlProxyList(YamlProxy):
    def __getitem__(self, nth):
        return wrap(self._objects[nth])

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
        return "YamlProxyList instance with %d items"%(len(self._objects),)


class YamlProxyDict(YamlProxy):
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
        return wrap(self._objects.get(name))

    def __getitem__(self, name):
        return wrap(self.__dict__["_objects"][name])

    def __setattr__(self, name, value):
        self.__dict__["_objects"][name] = value

    def __setitem__(self, name, value):
        self.__dict__["_objects"][name] = value

    def __repr__(self):
        assert isinstance(self._objects, dict)
        return "%s"%(self.__keys__(),)

def bind(kls):
    print kls
    return kls

