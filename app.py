#!/usr/bin/python
# coding=utf-8


import model
import loader

import codecs
import sys
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

import re

class CUIApp:
    """
    CUI Application.
    use command module?

    """
    def __init__(self):
        self.bs = []
        self.filename = "test.csv"
        self.marked = []

    def load(self):
        with file(self.filename) as f:
            self.bs = loader.read_csv(f)

    def save(self):
        with file(self.filename, 'w') as f:
            loader.write_csv(self.bs, f)

    def sync(self):
        self.save()# FIXME incremental write

    def listall(self):
        for b in self.bs:
            print "=" * 60
            print "ISBN:", b.isbn
            print "title:", b.title

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

    def book(self, isbn):
        pass

    def mark(self, b):
        self.marked.append(b)

    def unmark(self, b):
        self.marked.remove(b)

    def showmarked(self):
        for b in self.marked:
            print b

    def mkshelf(self, name):
        if not self.marked:
            return
        for b in self.marked:
            setattr(b, "shelf", name,)

    def selectschelf(self, name):
        pass

    def rmshelf(self):
        pass

    

app = CUIApp()

app.load()
#app.listall()
#app.find(u"482.*")
#app.find(u"入門") #FIXME
app.mark(app.book("4582851037"))
app.mark(app.book("4873115094"))
app.showmarked()

