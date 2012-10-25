#!/usr/bin/python
# coding=utf-8


def isbn_strip(s):
    """
    >>> isbn_strip("978-0-306-40615")
    (9, 7, 8, 0, 3, 0, 6, 4, 0, 6, 1, 5)
    >>> isbn_strip("0-201-53082-1")
    (0, 2, 0, 1, 5, 3, 0, 8, 2, 1)
    """
    def nums():
        for x in s:
            try:
                i = int(x)
            except:
                continue
            if str(i) == x:
                yield i
    return tuple(nums())


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
    ns = isbn_strip(s)
    w = (1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3)
    return 10 - (sum(map(lambda p : p[0] *p[1], zip(w, ns))) % 10 )


def validateISBN10(s):
    """
    from http://en.wikipedia.org/wiki/Check_digit#ISBN_10
    take the ISBN 0-201-53082-1. 
    The sum of products is 0*10 + 2*9 + 0*8 + 1*7 + 5*6 + 3*5 + 0*4 + 8*3 + 2*2 + 1*1 = 99 = 0 modulo 11. 
    So the ISBN is valid.
    >>> validateISBN10("0-201-53082-1")
    True
    """
    ns = isbn_strip(s)
    w = list(range(1, 11))
    w.reverse()
    return sum(map(lambda p: p[0]*p[1], zip(w, ns))) % 11 == 0


