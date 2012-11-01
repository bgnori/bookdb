#!/usr/bin/python
# coding=utf-8

"""
(id, key, <value type>, value)

id - unique numbering on each instance
key - property name 
<value type> - value type( see below)
value - property value 

value type must be one of:
    bool (python native)
    int (python native)
    string (python native)
    ref (referenc to other instance)
    mref (entry of reference set)

special id
<special> "Book", <id-0>
<special> "Book", <id-1>
<special> "Tag", <id-0>
... => constructor to omit 'path'
id-0 is 'init' object, meta thing, world, root, class manager, whatever..
(<id-0>, "Book", mref, <id-1>)
(<id-0>, "Book", mref, <id-2>)
(<id-0>, "Book", mref, <id-3>)
(<id-0>, "Book", mref, <id-4>)
(<id-0>, "Tag", mref, <id-5>)
(<id-0>, "Tag", mref, <id-6>)
(<id-0>, "Tag", mref, <id-7>)
....


concrete example for book db

!! we may have very same two books, so using isbn as id is a WRONG idea.

("Book", <id-0>, "title", "this is title")
("Book", <id-0>, "isbn", "00000000")
("Book", <id-0>, "tags", <id-3>) # it is "dangling". reference it, but not begin referenced.
("Book", <id-0>, "tags", <id-4>)
("Tag", <id-3>, "name", "geek") 
("Tag", <id-4>, "name", "cooking")
("Tag", <id-4>, "books", <id-0>) #is this right idea? => y. need tough maintenamce

issue:
    How to find "dangling"/orphan entry?
    nested tag.

nested tag 

an idea... not good
("Tag", <id-3>, "name", "meat") 
("Tag", <id-3>, "/Tag", <id-4>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-4>, "parent", <id-3>) #ugh!

another idea for nested tag
("Tag", <id-3>, "name", "meat") 
("Tag", <id-4>, "name", "meat/chicken") #wrong. giving special meaning to value 

yet another idea for nested tag 
("Tag", <id-3>, "name", "meat")
("Tag", <id-3>, "subtag", <id-4>) #mref
("Tag", <id-3>, "subtag", <id-5>)
("Tag", <id-3>, "subtag", <id-6>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-5>, "name", "pork")
("Tag", <id-6>, "name", "beaf")

issue:
    How to get parent => have a "parent", need ref/mref(multiple ref)
    value types. How to distinguish between int value and <id> => we type value


or we can go more "relational" on book-tag feature.
This forces us to "join".... which I do not want.

("Book", <id-0>, "title", "this is title")
("Book", <id-0>, "isbn", "00000000")
("Tag", <id-3>, "name", "geek") 
("Tag", <id-4>, "name", "cooking")

("Relation", <id-5>, "Left", <id-0>) #relation "object" MxN
("Relation", <id-5>, "Right", <id-3>) 

("Relation", <id-6>, "Left", <id-0>)
("Relation", <id-6>, "Right", <id-4>)


discussion:
 * trade off against ORM+SQLdb
  * human readable datafile
   * There is sql with csv? should be checked out.
   * can export/import. not csv as storage
 * why not pickle?
  * not readable from non-python
 * why not xml?
  * ref, flexibility
 * why not yaml?
  * not sure.
  * & and * are useful.
   * Yes! PyYaml supports it!
    * the point is, how to generate name for &/*
     * they do automatically.
'''python
f = "fooo"
zm = [f, f]

print yaml.dump([zm, zm])
'''
would give
'''
 - &id001 [fooo, fooo]
 - *id001
'''
   * tag (typing) is also supported
    * we need validator?
 * Is worth for sweat and bugs?
  * not sure.
 * Is this fun?
  * yes

We use yaml.
questions are:
    How to map regular objects into list+str+int combination? => Proxy

Should write sample yamls first.
"""



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


class YamlProxy(object):
    u"""
    >>> f = file("sample.yaml")
    >>> y = yaml.load(f)
    >>> p = YamlProxy(y)
    >>> p.Tags.Category.Cooking[0].isbn
    '4873115094'
    >>> p.Tags.Category.Cooking[0].title
    u'Cooking for Geeks: 料理の科学と実践レシピ'

    another sample
    >>> p = YamlProxy(yaml.load("isbn: 'this is isbn'"))
    >>> p.isbn
    'this is isbn'
    """
    def __init__(self, obj):
        self._objects = obj

    def __getitem__(self, nth):
        return self.__getx__(self._objects[nth])

    def __getattr__(self, name):
        return self.__getx__(self._objects.get(name))

    def __getx__(self, found):
        if isinstance(found, (list, dict)):
            return YamlProxy(found)
        return found


