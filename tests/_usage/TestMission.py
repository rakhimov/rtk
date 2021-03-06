#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.usage.TestMission.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing Mission module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from usage import dtmMission
from dao import DAO
from dao import RTKMission

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMissionDataModel(unittest.TestCase):
    """
    Class for testing the Mission model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission class.
        """
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmMission(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestMissionModel) __init__ should return a Mission model
        """
        self.assertTrue(isinstance(self.DUT, dtmMission))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestMissionModel): select_all() should return a Tree() object populated with RTKMission instances on success.
        """
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMission))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestMissionModel): select() should return an instance of the RTKMission data model on success.
        """
        self.DUT.select_all(1)
        _mission = self.DUT.select(1)

        self.assertTrue(isinstance(_mission, RTKMission))
        self.assertEqual(_mission.mission_id, 1)
        self.assertEqual(_mission.description, 'Test Mission Description')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestMissionModel): select should return None when passed a Mission ID that doesn't exist.
        """
        self.DUT.select_all(1)
        self.assertEqual(self.DUT.select(100), None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestMissionModel): insert() should return a zero error code on success.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 2)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestMissionModel): delete() should return False on success.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(2)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestMissionModel): delete() should return True when passed a Mission ID that doesn't exist.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Mission ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestMissionModel): update() should return a zero error code on success.
        """
        self.DUT.select_all(1)

        _mission = self.DUT.tree.get_node(1).data
        _mission.description = 'Test Mission Description'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestMissionModel): update() should return a non-zero error code when passed a Mission ID that doesn't exist.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Mission ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestMissionModel): update_all() should return a zero error code on success.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
