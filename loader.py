#!/usr/bin/python
# coding=utf-8

import lxml.etree as et
import utf8csv

import model

def write_csv(bs, csvf):
    """
    bs: sequence of Book instance
    unittest is needed, doctests become too complex

    usage:
    >>> from StringIO import StringIO
    >>> f = StringIO()
    >>> b0 = model.Book("00000000000", "How to use books")
    >>> b1 = model.Book("00000000000", "How ")
    >>> write_csv([b1], f)
    >>> f.getvalue() # doctest:+ELLIPSIS
    ...
    ...
    """
    w = utf8csv.UnicodeWriter(csvf)
    for b in bs:
        w.writerow(b.tuplify())
        for k, v in b.iterprops():
            w.writerow((b.isbn, k, v))

def read_csv(csvf):
    """
    """
    reader = utf8csv.UnicodeReader(csvf)
    books = {}

    for r in reader:
        if len(r) == 2:
            isbn = r[0]
            title = r[1]
            b = model.Book(isbn, title)
            books[isbn] = b
        elif len(r) == 3:
            isbn = r[0]
            key = r[1]
            value = r[2]
            b = books[isbn]
            setattr(b, key, value)
        else:
            raise "Bad data row", r

    return books.values()



googlexmlpath = {
    'id':"""/library/books/book/id""",
    'url':"""/library/books/book/url""",
    'title':"""/library/books/book/title""",
    'contributor':"""/library/books/book/contributor""",
    'type':"""/library/books/book/identifier/type""",  # = ISBN
    'value':"""/library/books/book/identifier/value"""
}


def read_xml(xmlf):
    """
    Load books from google books xml.
    usage: #fix this to use doctest
    with file("GoogleBooks/2012.xml") as f:
        bs = Book.load(f)
    for b in bs:
        print b.title #prints titles

    todo:
        tag as "google books" + shelf name in google books
    """
    r = []
    t = et.parse(xmlf)
    for found in t.xpath("/library/books/book"):
        title = found.xpath("title")[0].text#.decode('utf-8')
        isbn = found.xpath("identifier/value")[0].text#.decode('utf-8')
        b = model.Book(isbn, title)

        b.google_id = found.xpath("id")[0].text
        b.google_url = found.xpath("url")[0].text
        r.append(b)
    return r



if __name__ == "__main__":

    def dump(bs):
        for b in bs:
            print b.isbn
            print b.title
            print b.props
            print unicode(b)
            #print b

    import codecs
    import sys
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    with file("GoogleBooks/2012.xml") as f:
        bs = read_xml(f)
        print 'loaded', len(bs)
    if 0:
        dump(xs)

    with file("test.csv", 'w') as f:
        write_csv(bs, f)

    if 0:
        dump(bs)

    if 1:
        with file("test.csv") as f:
            cs = read_csv(f)
    if 1:
        #dump(cs)
        print 'loaded', len(cs)


