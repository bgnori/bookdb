#!/usr/bin/python
# coding=utf-8

import unittest
import yaml
import visit

class TestVisitor(unittest.TestCase):
    def setUp(self):
        visit.inject(visit.Visitor)

    def testInt(self):
        self.assertEqual(yaml.load('1'), 1)

    def testStr0(self):
        self.assertEqual(yaml.load('abc'), 'abc')

    def testStr1(self):
        self.assertEqual(yaml.load('"abc"'), 'abc')

    def testStr2(self):
        self.assertEqual(yaml.load('""'), '')

    def testBoolTrue(self):
        self.assertIsInstance(yaml.load('True'), bool)
        self.assertEqual(yaml.load('True'), True)

    def testBooltrue(self):
        self.assertIsInstance(yaml.load('true'), bool)
        self.assertEqual(yaml.load('true'), True)

    def testBoolFalse(self):
        self.assertIsInstance(yaml.load('False'), bool)
        self.assertEqual(yaml.load('False'), False)

    def testBoolfalse(self):
        self.assertIsInstance(yaml.load('false'), bool)
        self.assertEqual(yaml.load('false'), False)

    def testValue(self):
        y = yaml.load('=: foo')
        self.assertIn("=", y)

    def testNone(self):
        self.assertIsNone(yaml.load(''))

    def testEmptyList(self):
        self.assertEqual(yaml.load('[]'), [])

    def testOneItemList(self):
        self.assertIsInstance(yaml.load('[0]'), list)
        self.assertEqual(yaml.load('[0]'), [0])

    def testTwoItemList(self):
        self.assertEqual(yaml.load('[0, "a"]'), [0, 'a'])

    def testEmptyDict(self):
        self.assertEqual(yaml.load('{}'), {})

    def testOneItemDict(self):
        self.assertEqual(yaml.load('{"one":1 }'), {'one':1})

    def testTwoItemDict(self):
        self.assertEqual(yaml.load("""
        one: 1
        2: "two"
        """), {'one':1, 2:"two"})

    def testDictInList(self):
        self.assertEqual(yaml.load('[{}]'), [{}])

    def testListInDict(self):
        self.assertEqual(yaml.load('{foo: []}'), {"foo": []})

    def testRecursiveList(self):
        y = yaml.load('''&A [*A] ''')
        self.assertEqual(y[0], y)

    def testRecursiveDict(self):
        y = yaml.load('''&A {foo: *A} ''')
        self.assertEqual(y['foo'], y)


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
        root = visit.find("/", self.y)
        self.assertEqual(self.y, root)

    def testSingleName1(self):
        x = visit.find("/a", self.y)
        self.assertEqual(self.y["a"], x)

    def testSingleName2(self):
        x = visit.find("/b", self.y)
        self.assertEqual(self.y["b"], x)

    def testIndexAfterName(self):
        x = visit.find("/c/0", self.y)
        self.assertEqual(self.y["c"][0], x)

    def testSingleIndex1(self):
        x = visit.find("/0", self.z)
        self.assertEqual(self.z[0], x)

    def testSingleIndex2(self):
        x = visit.find("/1", self.z)
        self.assertEqual(self.z[1], x)

    def testNameAfterIndex(self):
        x = visit.find("/2/second", self.z)
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
        xs = visit.find("//.[x=3", self.y)
        self.assertIn(self.y["c"], xs)
        self.assertIn(self.y["e"], xs)

    def testValueEq2(self):
        xs = visit.find("//.[y=6", self.y)
        self.assertIn(self.y["d"], xs)
        self.assertIn(self.y["e"], xs)


