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


def ISBN13CheckDigit(in_s):
    """
    from wikipeida http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13_check_digit_calculation
        s = 9*1 + 7*3 + 8*1 + 0*3 + 3*1 + 0*3 + 6*1 + 4*3 + 0*1 + 6*3 + 1*1 + 5*3
          =   9 +  21 +   8 +   0 +   3 +   0 +   6 +  12 +   0 +  18 +   1 +  15
          = 93
        93 / 10 = 9 remainder 3
        10 - 3 = 7
    >>> ISBN13CheckDigit("978-0-306-40615")
    7
    >>> ISBN13CheckDigit("978-4-10-109205")
    8
    """
    if isinstance(in_s, str):
        ns = isbn_strip(in_s)
    elif isinstance(in_s, (list, tuple)):
        ns = in_s
    else:
        raise "Bad input"

    w = (1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3)
    return 10 - (sum(map(lambda p : p[0] *p[1], zip(w, ns))) % 10 )


def ISBN10CheckDigit(in_s):
    """
        http://ja.wikipedia.org/wiki/ISBN#.E3.83.81.E3.82.A7.E3.83.83.E3.82.AF.E3.83.87.E3.82.A3.E3.82.B8.E3.83.83.E3.83.88
        10×4 + 9×1 + 8×0 + 7×1 + 6×0 + 5×9 + 4×2 + 3×0 + 2×5
        = 40  +  9  +  0  +  7  +  0  +  45  +  8  +  0  +  10
        = 119
        119 ÷ 11 = 10 あまり 9
        11 - 9 = 2
        >>> ISBN10CheckDigit("410109205")
        2
    """


def validateISBN10(in_s):
    """
    from http://en.wikipedia.org/wiki/Check_digit#ISBN_10
    take the ISBN 0-201-53082-1. 
    The sum of products is 0*10 + 2*9 + 0*8 + 1*7 + 5*6 + 3*5 + 0*4 + 8*3 + 2*2 + 1*1 = 99 = 0 modulo 11. 
    So the ISBN is valid.
    >>> validateISBN10("0-201-53082-1")
    True
    """
    if isinstance(in_s, str):
        ns = isbn_strip(in_s)
    elif isinstance(in_s, (list, tuple)):
        ns = in_s
    else:
        raise "Bad input"

    w = list(range(1, 11))
    w.reverse()
    return sum(map(lambda p: p[0]*p[1], zip(w, ns))) % 11 == 0


def isbn10to13(xs):
    """
    Convert isbn-10 to isbn-13
    1) removes old checkdigit
    2) add 978 to head
    3) calc check digit

    >>> xs = isbn_strip("4-00-310101-4")
    >>> ys = isbn_strip("978-4-00-310101-8")
    >>> isbn10to13(xs) == ys
    True
    """
    pass


