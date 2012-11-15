#!/usr/bin/python
# coding=utf-8

import unittest
import yaml
import visit

class TestVisitor(unittest.TestCase):
    def setUp(self):
        visit.inject(visit.Visitor)

    def testRecursive(self):
        y = yaml.load('''&A [*A] ''')

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

if False:
    with file("sample.yaml") as f:
        y = yaml.load(f.read())

if False:
    y = yaml.load('''
        key-foo: 'value-foo'
        key-bar: 'value-bar'
        array: [1, 2, 3]''')
    print y
