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

if False:
    with file("sample.yaml") as f:
        y = yaml.load(f.read())

