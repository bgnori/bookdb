#!/usr/bin/python
# coding=utf-8

import model
import loader

import codecs
import sys
#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

import re
import readline
import cmd
import isbn as libisbn

    
class CUIApp(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        app = model.App()

        with file(app.filename) as f:
            app.load(loader.read_csv(f))
        self.app = app

    def do_echoarg(self, arg):
        print repr(arg)

    def do_quit(self, arg):
        self.do_exit(arg)
    def do_exit(self, arg):
        app = self.app
        with file(app.filename, 'w') as f:
            loader.write_csv(app.save(), f)
        sys.exit(0)

    def do_list(self, arg):
        app = self.app
        try:
            n = int(arg)
        except:
            n = -1
        for b in app.get_list(n):
            print "=" * 60
            print "ISBN:", b.isbn
            print "title:", b.title

    def do_mark(self, arg):
        app = self.app
        b = app.isbn(arg)
        if b:
            app.mark(b)
            print "marked ", b.title
        else:
            print "no such book"

    def do_unmark(self, arg):
        app = self.app
        b = app.isbn(arg)
        if b:
            app.unmark(b)
            print "unmarked ", b.title
        else:
            print "no such book"

    def do_marked(self, arg):
        app = self.app
        for b in app.marked:
            print unicode(b)



if __name__ == "__main__":
    app = CUIApp()
    app.cmdloop()


