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


