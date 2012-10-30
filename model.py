#!/usr/bin/python
# coding=utf-8


import isbn as libisbn

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


class TupleSteamer:
    """
    >>> ts = TupleSteamer(...)
    >>> for t in ts:
            print t
    ('Book', 1234567890123, 'title')
    (1234567890123, 'tag', tag0)
    (1234567890123, 'tag', tag1)
    ('tag', tag0, 'first tag')
    ('tag', tag1, 'second tag')
    """

    def __init__(self, seq):
        pass

    def __next__(self):
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
