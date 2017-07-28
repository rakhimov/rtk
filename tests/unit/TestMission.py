#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       TestMission.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the test class for testing Mission module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from usage.Mission import Model, Mission
from dao.DAO import DAO, RTKRevision, RTKMission

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMissionModel(unittest.TestCase):
    """
    Class for testing the Mission model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission class.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        _revision = RTKRevision()
        self.dao.db_add(_revision)

        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        self.dao.db_add(_mission)

        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        self.dao.db_add(_mission)

        self.DUT = Model()
        self.DUT.dao = self.dao

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test00_mission_create(self):
        """
        (TestMission) __init__ should create a Mission data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicMission, {})
        self.assertTrue(isinstance(self.DUT.dao, DAO))

        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_retrieve_all_missions(self):
        """
        (TestMission): retrieve_all should return a dictionary of RTKMission objects on success.
        """

        _dic_missions = self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(isinstance(_dic_missions, dict))
        self.assertTrue(isinstance(_dic_missions[1], RTKMission))

    @attr(all=True, unit=True)
    def test02a_retrieve_single_mission(self):
        """
        (TestMission): retrieve should return an instance of the RTKMission data model on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _mission = self.DUT.retrieve(1)

        self.assertTrue(isinstance(_mission, RTKMission))
        self.assertEqual(_mission.revision_id, 1)
        self.assertEqual(_mission.mission_id, 1)

    @attr(all=True, unit=True)
    def test02b_retrieve_missing_mission(self):
        """
        (TestMission): retrieve should return None when passes a Mission ID that doesn't exist.
        """

        _mission = self.DUT.retrieve(100)

        self.assertEqual(_mission, None)

    @attr(all=True, unit=True)
    def test03a_add_mission(self):
        """
        (TestMission): add_mission should return an RTKMission object on success.
        """

        _mission = self.DUT.add_mission(1)

        self.assertTrue(isinstance(_mission, RTKMission))
        self.assertEqual(_mission.revision_id, 1)

    @attr(all=True, unit=True)
    def test04a_delete_mission(self):
        """
        (TestMission): delete_mission should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertFalse(self.DUT.delete_mission(2))

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_mission_id(self):
        """
        (TestMission): delete_mission should return True when passed a Mission ID that doesn't exist.
        """

        self.assertTrue(self.DUT.delete_mission(100))

    @attr(all=True, unit=True)
    def test_05a_save_mission(self):
        """
        (TestMission): save_mission should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _mission = self.DUT.dicMission[1]
        _mission.description = 'Mission to save'

        self.assertFalse(self.DUT.save_mission(1))

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_mission(self):
        """
        (TestMission): save_mission should return True when passed a Revision ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.save_mission(100))

    @attr(all=True, unit=True)
    def test_06a_save_all_missions(self):
        """
        (TestMission): save_all_missions should return False on success.
        """

        self.assertFalse(self.DUT.save_all_missions())


class Test01MissionController(unittest.TestCase):
    """
    Class for testing the Mission Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission Data Controller.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')
        self.dao.db_add(RTKMission())
        self.dao.db_add(RTKMission())

        self.DUT = Mission()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestMission) __init__ should return a Mission Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Mission))

