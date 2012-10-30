#!/usr/bin/python
# coding=utf-8


import isbn as libisbn

"""
(path,id,key, <value type>, value)

path - class or type
id - unique numbering on each instance
key - property name (or "reference" to other object)
value - property value (or id, if key starts with '/')

value type must be one of:
    bool (python native)
    int (python native)
    string (python native)
    ref (entry of reference set)

special id
<special> "Book", <id-0>
<special> "Book", <id-1>
<special> "Tag", <id-0>
... => constructor to omit 'path'
id-0 is 'init' object, meta thing, world, root, class manager, whatever..
(<id-0>, "Book", ref, <id-1>)
(<id-0>, "Book", ref, <id-2>)
(<id-0>, "Book", ref, <id-3>)
(<id-0>, "Book", ref, <id-4>)
(<id-0>, "Tag", ref, <id-5>)
(<id-0>, "Tag", ref, <id-6>)
(<id-0>, "Tag", ref, <id-7>)
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
("Tag", <id-3>, "name", "meat") 
("Tag", <id-3>, "/Tag", <id-4>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-4>, "parent", <id-3>) #ugh!


another idea for nested tag
("Tag", <id-3>, "name", "meat") 
("Tag", <id-4>, "name", "meat/chicken") #wrong. giving special meaning to value 


yet another idea for nested tag 
("Tag", <id-3>, "name", "meat")
("Tag", <id-3>, "subtag", <id-4>)
("Tag", <id-3>, "subtag", <id-5>)
("Tag", <id-3>, "subtag", <id-6>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-5>, "name", "pork")
("Tag", <id-6>, "name", "beaf")

issue:
    How to get parent
    value types. How to distinguish between int value and <id>




or we can go more "relational" on book-tag feature.

("Book", <id-0>, "title", "this is title")
("Book", <id-0>, "isbn", "00000000")
("Tag", <id-3>, "name", "geek") 
("Tag", <id-4>, "name", "cooking")

("Relation", <id-5>, "Left", <id-0>) #relation "object" MxN
("Relation", <id-5>, "Right", <id-3>) 

("Relation", <id-6>, "Left", <id-0>)
("Relation", <id-6>, "Right", <id-4>)

"""

class Book:
    fields = set(["isbn", "title", "props"]) #fixme 

    @classmethod
    def from_tuple(klass, t):
        assert t[0] == "Book"
        return Book(t[1], t[2])

    def tuplify(self):
        return ("Book", self.isbn, self.title)

    def validateISBN(self, isbn):
        xs = libisbn.isbn_strip(isbn)
        assert xs

        if len(xs) == 10:
            if not libisbn.validateISBN10(xs):
                raise libisbn.BadISBNException
            xs = libisbn.isbn10to13(xs)

        elif len(xs) == 13:
            if not libisbn.validateISBN13(xs):
                raise libisbn.BadISBNException
        else:
            print "bad length %s"%(isbn,)
            raise

        assert xs
        assert len(xs) == 13
        return ''.join(map(str, xs))

    def __init__(self, isbn, title): #fixme I wanna use "new", not "init" 
        '''has to be unicode, not utf-8'''
        if False:
            isbn = self.validateISBN(isbn)

        self.isbn = isbn  # has to validate isbn here.
        self.title = title  #check encode !
        self.props = {}

    #def __str__(self):
    #    raise UnicodeEncodeError

    def __unicode__(self):
        sp = "".join(["(%s: %s)"%(k, v) for k, v in self.props.iteritems()])
        return u'ISBN: %s, title: "%s" props: %s'%(self.isbn, self.title, sp)


    def iterprops(self):
        return self.props.iteritems()

    def __getattr__(self, name):
        return self.props[name]

    def __nonzero__(self):
        return True

    def __setattr__(self, name, value):
        if name in self.fields:
            self.__dict__[name] = value
        else:
            self.__dict__["props"][name] = value




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
