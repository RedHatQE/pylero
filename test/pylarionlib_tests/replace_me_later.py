#!/usr/bin/env python
# -*- coding: utf8 -*-

# A temporary, just-show-something-thing before proper testing code arises.

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from pylarionlib.server import Server
from pylarionlib.test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite

my_login = 'vkadlcik'
my_password = '94rskco.kftg9'
my_project_name = 'BrnoTraining'
my_server = Server('http://polarion.dqe.lab.eng.bos.redhat.com/polarion', my_login, my_password, my_project_name)


class TestWorkItemBasics(unittest.TestCase):

    test_session = None
    
    @classmethod    
    def setUpClass(cls):
        super(TestWorkItemBasics, cls).setUpClass()
        TestWorkItemBasics.test_session = my_server._createSession()
        TestWorkItemBasics.test_session._login()
        
    @classmethod
    def tearDownClass(cls):
        TestWorkItemBasics.test_session._logout()
        super(TestWorkItemBasics, cls).tearDownClass()

    def test_0001(self):
        permanent_title = 'vaskovo uzitkovy test 1'
        tc = FunctionalTestCase(TestWorkItemBasics.test_session)
        tc.title = permanent_title
        tc._crudCreate()
        self.assertTrue(tc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_title, tc.title)
        tc.title = 'tajna zmena v titulku!'
        self.assertNotEqual(permanent_title, tc.title)
        tc._crudRetrieve()
        self.assertEqual(permanent_title, tc.title)
 
    def test_0002(self):
        old_title = 'vaskovo stavebni test 1'
        new_title = 'zmena v titulku!'
        tc = StructuralTestCase(TestWorkItemBasics.test_session)
        tc.title = old_title
        tc._crudCreate()
        self.assertTrue(tc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(old_title, tc.title)
        tc.title = new_title
        self.assertEqual(new_title, tc.title)
        tc._crudUpdate()
        self.assertEqual(new_title, tc.title)
        tc._crudRetrieve()
        self.assertEqual(new_title, tc.title)
 
    def test_0003(self):
        title = 'vaskovo neuzitkovy test 1'
        tc1 = NonFunctionalTestCase(TestWorkItemBasics.test_session)
        tc1.title = title
        tc1._crudCreate()
        self.assertTrue(tc1.puri.startswith('subterra:data-service:objects:'))
        pid = tc1.pid
        tc2 = TestWorkItemBasics.test_session.getWorkItemByPID(pid)
        self.assertEqual(title, tc2.title)
        self.assertIsInstance(tc2, NonFunctionalTestCase)
        self.assertEqual(tc1.title, tc2.title)
 
    def test_0004(self):
        tc1 = TestSuite(TestWorkItemBasics.test_session)
        tc1.title = 'vaskovo testovy pruvod'
        tc1._crudCreate()
        tc2 = TestWorkItemBasics.test_session.getWorkItemByPURI(tc1.puri)
        self.assertEqual(tc1.puri, tc2.puri)
        self.assertEqual(tc1.pid, tc2.pid)
        self.assertEqual(tc1.__class__, tc2.__class__)
