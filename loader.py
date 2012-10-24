#!/usr/bin/python
# coding=utf-8

import lxml.etree as et
import utf8csv



googlexmlpath = {
    'id':"""/library/books/book/id""",
    'url':"""/library/books/book/url""",
    'title':"""/library/books/book/title""",
    'contributor':"""/library/books/book/contributor""",
    'type':"""/library/books/book/identifier/type""",  # = ISBN
    'value':"""/library/books/book/identifier/value"""
}

def isbn_strip(s):
    """
    >>> isbn_strip("978-0-306-40615")
    '978030640615'
    >>> isbn_strip("0-201-53082-1")
    '0201530821'
    """

def ISBN13CheckDigit(s):
    """
    from wikipeida http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13_check_digit_calculation
        s = 9*1 + 7*3 + 8*1 + 0*3 + 3*1 + 0*3 + 6*1 + 4*3 + 0*1 + 6*3 + 1*1 + 5*3
          =   9 +  21 +   8 +   0 +   3 +   0 +   6 +  12 +   0 +  18 +   1 +  15
          = 93
        93 / 10 = 9 remainder 3
        10 - 3 = 7
    >>> ISBN13CheckDigit("978-0-306-40615")
    3
    """

def validateISBN10(s):
    """
    from http://en.wikipedia.org/wiki/Check_digit#ISBN_10
    take the ISBN 0-201-53082-1. 
    The sum of products is 0*10 + 2*9 + 0*8 + 1*7 + 5*6 + 3*5 + 0*4 + 8*3 + 2*2 + 1*1 = 99 = 0 modulo 11. 
    So the ISBN is valid.
    >>> validateISBN10("0-201-53082-1")
    """


class Book:
    def __init__(self, title, contributors, isbn):
        self.title = title or ''
        self.contributors = contributors or ''
        self.ISBN = isbn or ''


    def tuplify(self):
        return (self.title, self.contributors, self.ISBN)

    def hasValidISBN(self):
        """
        check ISBN check sum


        """
        return False

    
    @classmethod
    def write_csv(kls, bs, csvf):
        """
        seq: sequence of Book instance
        >>> from StringIO import StringIO
        >>> f = StringIO()
        >>> Book.write_csv([Book("How to use books", "author", "00000000000")], f)
        >>> f.getvalue()
        "something" #FIXME
        """
        w = utf8csv.UnicodeWriter(csvf)
        for b in bs:
            w.writerow(b.tuplify())

    @classmethod
    def read_csv(kls, csvf):
        """
        """
        reader = utf8csv.UnicodeReader(csvf)
        for r in reader:
            print r


    @classmethod
    def read_xml(kls, xmlf):
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
        bs = Book.read_xml(f)
    with file("test.csv", 'w') as f:
        Book.write_csv(bs, f)


