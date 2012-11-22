#!/usr/bin/python
# coding=utf-8

import visit


def yparse(ypath):
    return None, None, None


def find(ypath, node):
    '[]'

    xs = ypath.split("/")
    
    n = node
    for x in xs:
        if not x:
            continue
        try:
            ik = int(x)
        except:
            ik = x
        n = n[ik]
    return n

