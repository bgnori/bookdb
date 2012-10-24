#!/usr/bin/python
# coding utf8

import lxml.etree as et

googlexmlpath = {
    'id':"""/library/books/book/id""",
    'url':"""/library/books/book/url""",
    'title':"""/library/books/book/title""",
    'contributor':"""/library/books/book/contributor""",
    'type':"""/library/books/book/identifier/type""",  # = ISBN
    'value':"""/library/books/book/identifier/value"""
}



class Book:
    def __init__(self, title, contributors, isbn):
        self.title = title 
        self.contributors = contributors
        self.ISBN = isbn

    
    @classmethod
    def write_csv(kls, bs, coref):
        """
        seq: sequence of Book instance
        >>> from StringIO import StringIO
        >>> f = StringIO()
        >>> Book.write_csv([Book("How to use books", "author", "00000000000")], f)
        >>> f.getvalue()
        "something" #FIXME
        """
        #implement me!

    @classmethod
    def load(kls, f):
        """
        Load books from google books xml.
        usage: #fix this to use doctest
        with file("GoogleBooks/2012.xml") as f:
            bs = Book.load(f)
        for b in bs:
            print b.title #prints titles
        """
        r = []
        t = et.parse(f)
        for found in t.xpath("/library/books/book"):
            title = found.xpath("title")[0].text
            google_id = found.xpath("id")[0].text
            url = found.xpath("url")[0].text
            #contributors = found.xpath("contributor")[0].text
            contributors = None
            isbn = found.xpath("identifier/value")[0].text
            b = kls(title, contributors, isbn)
            r.append(b)
        return r

if __name__ == "__main__":
    with file("GoogleBooks/2012.xml") as f:
        bs = Book.load(f)
    for b in bs:
        print b.title


