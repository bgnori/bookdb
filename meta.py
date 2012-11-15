#!/usr/bin/python
# coding=utf-8


import yaml
import visit

class ValidationError(Exception):
    pass


class MetaVisitor(visit.Visitor):
    pass

visit.inject(MetaVisitor)
# visit.inject(BookVisitor)
with file("kw-schema.yaml") as f:
    print yaml.load(f.read())

