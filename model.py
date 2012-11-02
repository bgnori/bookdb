#!/usr/bin/python
# coding=utf-8


import isbn as libisbn
import meta
import yaml

class Yamlable(meta.YamlProxyDict):
    def __init__(self, **argv):
        kls = self.__class__
        d = dict([(key, None) for k in kls.fields])
        d.update(argv)
        self.__dict__["_objects"] = d

class Tag(Yamlable):
    fields = ()

class Book(Yamlable):
    fields = ()


class Library(object):
    """
    >>> lib = Library()
    >>> f = file("sample.yaml")
    >>> lib.load(f)
    >>> lib.show(lib.Root())
    set(['Books', 'Tags'])
    >>> len(lib.Books())
    5
    >>> lib.show(lib.Tags())
    set(['Category', 'Status'])
    >>> lib.show(lib.Categories())
    set(['Engineering', 'Cooking', 'Business'])
    >>> t = lib.Category("Politics")
    >>> lib.show(lib.Categories())
    set(['Cooking', 'Business', Engineering', 'Politics'])
    >>> lib.show(lib.path("/Tags/Categories/Cooking"))
    'Book, isbn: 4873115094'

    """
    def __init__(self):
        self.objects = None

    def load(self, f):
        self.objects = meta.wrap(yaml.load(f))

    def save(self, f):
        pass

    def show(self, obj):
        if isinstance(obj, meta.YamlProxyDict):
            print set(obj.__keys__())
        elif isinstance(obj, meta.YamlProxyList):
            print len(obj)
        else:
            print obj

    def Root(self):
        return self.objects

    def Books(self):
        return self.objects.Books

    def Tags(self):
        return self.objects.Tags

    def Categories(self):
        return self.objects.Tags.Category

    def Book(self):
        pass

    def Tag(self, name):
        self.objects.Tags[name] = Tag()

    def Category(self, name):
        self.objects.Tags.Category[name] = Tag()

    def path(self, p):
        pass


class App:
    """
    Application.
    """
    def __init__(self):
        self.bs = []
        self.filename = "test.csv"
        self.marked = set()
        self.focus = 0

    def load(self, bs):
        self.bs = bs

    def save(self):
        return self.bs

    def sync(self):
        self.save()# FIXME incremental write

    def get_list(self, count):
        return self.bs[:count]

    def add(self, isbn, title):
        try:
            b = model.Book(isbn, title)
        except libisbn.BadISBNException:
            pass
        self.bs.append(b)
        self.sync()

    def find(self, s):
        #FIXME
        r = re.compile(s, re.UNICODE)
        with file(self.filename) as f:
            for found in r.findall(f.read()):
                print unicode(found, "utf-8")#fileencoding!

    def isbn(self, isbn):
        for b in self.bs:
            if b.isbn == isbn:
                return b
        return None

    def mark(self):
        self.marked.add(self.focus)

    def unmark(self):
        self.marked.discard(self.focus)

    def mktag(self, name):
        pass

    def rmtag(self):
        pass

    def lstag(self, name):
        r = []
        for b in self.bs:
            s = b.props.get("shelf", None)
            if s and name in s:
                r.append(b)
        return r

    def mark_all_with_tag(self, tag):
        pass


"""
app.load()
#app.listall()
#app.find(u"482.*")
#app.find(u"入門") #FIXME
app.mark(app.book("4582851037"))
app.mark(app.book("4873115094"))
app.showmarked()
"""
