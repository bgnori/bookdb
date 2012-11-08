#!/usr/bin/python
# coding=utf-8


import isbn as libisbn
from meta import YSchemaDict, YSchemaList, YSchema
import yaml


book_schema = YSchema(0)

@book_schema.bind("Root")
class Root(YSchemaDict):
    field = {"Tags":"Tags", "Books":"Books"}


@book_schema.bind("Book")
class Book(YSchemaDict):
    field = {"isbn":str, "title":str}

@book_schema.bind("Books")
class Books(YSchemaList):
    hometype = Book
    def _validate_set(self, param, value):
        assert isinstance(value, Book)


@book_schema.bind("Tags")
class Tags(YSchemaDict):
    field = {"Category":"Categories", "Status":"Status"}


@book_schema.bind("Category")
class Category(YSchemaDict):
    field = {"name":str, "Books":"Books", "SubCategory":"Categories"}


@book_schema.bind("Categories")
class Categories(YSchemaList):
    hometype = Category


@book_schema.bind("Status")
class Status(YSchemaDict):
    field = {"notyet", "working", "read"}


class Library(object):
    """
    >>> lib = Library()
    >>> f = file("sample.yaml")
    >>> lib.load(f)
    >>> lib.Root()
    ['Books', 'Tags']
    >>> lib.Books()
    ListMixin instance with 5 items
    >>> lib.Tags()
    ['Category', 'Status']
    >>> lib.Categories()
    ['Engineering', 'Cooking', 'Business']
    >>> t = lib.Category("Politics")
    >>> t
    []
    >>> lib.Categories()
    ['Politics', 'Engineering', 'Cooking', 'Business']
    >>> b = lib.Book(None, None)
    >>> b
    ['isbn', 'title']
    """
    def __init__(self):
        self.objects = None

    def load(self, f):
        self.objects = book_schema.wrap_as_root(yaml.load(f))

    def save(self, f):
        pass

    def Root(self):
        return self.objects

    def Books(self):
        return self.objects.Books

    def Tags(self):
        return self.objects.Tags

    def Categories(self):
        return self.Tags().Category

    def Book(self, isbn, title):
        b = Book({'isbn':isbn, 'title':title})
        self.objects.Books.append(b)
        return b

    def Category(self, name):
        c = Category({})
        self.Tags().Category.append(c)
        return c

    def path(self, p):
        """
        Check YPath first.
        .>>> lib = Library()
        .>>> f = file("sample.yaml")
        .>>> lib.load(f)
        .>>> lib.path("/Tags/Categories/Cooking[0]")
        'Book, isbn: 4873115094'

        """
        xs = p.split("/")
        print xs
        obj = self.objects
        for x in xs:
            if not x:
                continue
            print x, obj
            if obj:
                obj = getattr(obj, x)
            else:
                return None
        return obj


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
