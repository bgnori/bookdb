#!/usr/bin/python
# coding=utf-8

import unittest
import yaml
import visit
import ypath

class TestYPathBasic(unittest.TestCase):
    def setUp(self):
        visit.inject(visit.Visitor)
        self.y = yaml.load('''
            a: 1
            b: 2
            c: [3, 4]
        ''')
        self.z = yaml.load('''
            - 0
            - one
            - { first: 3, second: 4}
        ''')

    def testRoot(self):
        root = ypath.find("/", self.y)
        self.assertEqual(self.y, root)

    def testSingleName1(self):
        x = ypath.find("/a", self.y)
        self.assertEqual(self.y["a"], x)

    def testSingleName2(self):
        x = ypath.find("/b", self.y)
        self.assertEqual(self.y["b"], x)

    def testIndexAfterName(self):
        x = ypath.find("/c/0", self.y)
        self.assertEqual(self.y["c"][0], x)

    def testSingleIndex1(self):
        x = ypath.find("/0", self.z)
        self.assertEqual(self.z[0], x)

    def testSingleIndex2(self):
        x = ypath.find("/1", self.z)
        self.assertEqual(self.z[1], x)

    def testNameAfterIndex(self):
        x = ypath.find("/2/second", self.z)
        self.assertEqual(self.z[2]["second"], x)


class TestYPathCond(unittest.TestCase):
    def setUp(self):
        visit.inject(visit.Visitor)
        self.y = yaml.load('''
            a: 1
            b: 2
            c: {x: 3, y: 4}
            d: {x: 5, y: 6}
            e: {x: 3, y: 6}
        ''')

    def testValueEq1(self):
        xs = ypath.find("//.[x=3]", self.y)
        self.assertIn(self.y["c"], xs)
        self.assertIn(self.y["e"], xs)

    def testValueEq2(self):
        xs = ypath.find("//.[y=6]", self.y)
        self.assertIn(self.y["d"], xs)
        self.assertIn(self.y["e"], xs)

class TestYPathParse(unittest.TestCase):
    def testNone(self):
        path, node, cond = ypath.yparse("")
        self.assertIsNone(path)
        self.assertIsNone(node)
        self.assertIsNone(cond)

    def testRoot(self):
        path, node, cond = ypath.yparse("/")
        self.assertEqual(path, ())
        self.assertIsNone(node)
        self.assertIsNone(cond)

