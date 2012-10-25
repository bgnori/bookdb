#!/usr/bin/python
# coding=utf-8



class Book:
    fields = set(["isbn", "title", "props"]) #fixme 
    def __init__(self, isbn, title): #fixme I wanna use "new", not "init" 
        '''has to be unicode, not utf-8'''
        self.isbn = isbn  # has to validate isbn here.
        self.title = title  #check encode !
        self.props = {}

    #def __str__(self):
    #    raise UnicodeEncodeError

    def __unicode__(self):
        sp = "".join(["(%s: %s)"%(k, v) for k, v in self.props.iteritems()])
        return u'ISBN: %s, title: "%s" props: %s'%(self.isbn, self.title, sp)

    def tuplify(self):
        return (self.isbn, self.title)

    def hasValidISBN(self):
        """
        check ISBN check sum
        """
        return False
    def iterprops(self):
        return self.props.iteritems()

    def __getattr__(self, name):
        return self.props[name]

    def __setattr__(self, name, value):
        if name in self.fields:
            self.__dict__[name] = value
        else:
            self.__dict__["props"][name] = value
