#!/usr/bin/python
# coding=utf-8


import yaml
import visit

class ValidationError(Exception):
    pass


class BookVisitor(visit.Visitor):
    pass

visit.inject(BookVisitor)

