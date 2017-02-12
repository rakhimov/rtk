#!/usr/bin/env python -O
"""
This is the test class for testing the Physics of Failure Load class.
"""

# -*- coding: utf-8 -*-
#
#       tests.pof.TestLoad.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from analyses.pof.Load import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestLoadModel(unittest.TestCase):
    """
    Class for testing the Load model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Load model class.
        """

        self.DUT = Model(0)

    @attr(all=True, unit=True)
    def test_mode_create(self):
        """
        (TestLoad) __init__ should return instance of Load data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.load_id, None)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.damage_model, 0)
        self.assertEqual(self.DUT.priority, 0)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestLoad) set_attributes should return 0 with good inputs
        """

        _values = (0, 1, 'Test Load', 2, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLoad) set_attributes should return 40 with missing input(s)
        """

        _values = (0, 0, 'Test Load', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestLoad) set_attributes should return 10 with wrong data type
        """

        _values = (0, 0, 'Test Load', None, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestLoad) set_attributes should return 10 with bad value
        """

        _values = (0, 0, 'Test Load', '', 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLoad) get_attributes should return good values
        """

        _values = (0, None, '', 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestLoad) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 'Test Load', 2, 1)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)