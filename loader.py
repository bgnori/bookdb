#!/usr/bin/python
# coding=utf-8

import lxml.etree as et
import utf8csv

import model


googlexmlpath = {
    'id':"""/library/books/book/id""",
    'url':"""/library/books/book/url""",
    'title':"""/library/books/book/title""",
    'contributor':"""/library/books/book/contributor""",
    'type':"""/library/books/book/identifier/type""",  # = ISBN
    'value':"""/library/books/book/identifier/value"""
}

def write_csv(bs, csvf):
    """
    seq: sequence of Book instance
    >>> from StringIO import StringIO
    >>> f = StringIO()
    >>> write_csv([model.Book("00000000000", "How to use books")], f)
    >>> f.getvalue()
    "something" #FIXME
    """
    w = utf8csv.UnicodeWriter(csvf)
    for b in bs:
        w.writerow(b.tuplify())

def read_csv(csvf):
    """
    """
    reader = utf8csv.UnicodeReader(csvf)
    return [model.Book(r[0], r[1]) for r in reader]


def read_xml(xmlf):
    """
    Load books from google books xml.
    usage: #fix this to use doctest
    with file("GoogleBooks/2012.xml") as f:
        bs = Book.load(f)
    for b in bs:
        print b.title #prints titles
    """
    r = []
    t = et.parse(xmlf)
    for found in t.xpath("/library/books/book"):
        title = found.xpath("title")[0].text#.decode('utf-8')
        isbn = found.xpath("identifier/value")[0].text#.decode('utf-8')
        b = kls(isbn, title)

        b.google_id = found.xpath("id")[0].text
        b.google_url = found.xpath("url")[0].text
        r.append(b)
    return r



if __name__ == "__main__":

    import codecs
    import sys
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    with file("GoogleBooks/2012.xml") as f:
        bs = model.Book.read_xml(f)
    for b in bs:
        print b.isbn
        print b.title
        print b.props
        print unicode(b)
        print b

if False:
    with file("test.csv", 'w') as f:
        write_csv(bs, f)

    with file("test.csv") as f:
        cs = read_csv(f)
        for c in cs:
            print unicode(c)
            #print u'ISBN: %s, title: "%s"'%(c.isbn, c.title)
            #print c.isbn 
            #print c.title


