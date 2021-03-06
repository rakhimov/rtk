#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMilHdbkF.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKMilHdbkF module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKMilHdbkF import RTKMilHdbkF

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMilHdbkF(unittest.TestCase):
    """
    Class for testing the RTKMilHdbkF class.
    """

    _attributes = (1, 0.00235, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKMilHdbkF class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMilHdbkF).first()
        self.DUT.A1 = self._attributes[1]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkmilhdbkf_create(self):
        """
        (TestRTKMilHdbkF) __init__ should create an RTKMilHdbkF model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMilHdbkF))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mil_hdbk_f')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.A1, 0.00235)
        self.assertEqual(self.DUT.A2, 0.0)
        self.assertEqual(self.DUT.B1, 0.0)
        self.assertEqual(self.DUT.B2, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.lambdaDB, 0.0)
        self.assertEqual(self.DUT.lambdaBP, 0.0)
        self.assertEqual(self.DUT.lambdaCYC, 0.0)
        self.assertEqual(self.DUT.lambdaEOS, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.piCD, 0.0)
        self.assertEqual(self.DUT.piCF, 0.0)
        self.assertEqual(self.DUT.piCR, 0.0)
        self.assertEqual(self.DUT.piCV, 0.0)
        self.assertEqual(self.DUT.piCYC, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piF, 0.0)
        self.assertEqual(self.DUT.piI, 0.0)
        self.assertEqual(self.DUT.piK, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.piM, 0.0)
        self.assertEqual(self.DUT.piMFG, 0.0)
        self.assertEqual(self.DUT.piN, 0.0)
        self.assertEqual(self.DUT.piNR, 0.0)
        self.assertEqual(self.DUT.piP, 0.0)
        self.assertEqual(self.DUT.piPT, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piR, 0.0)
        self.assertEqual(self.DUT.piS, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.pi_u, 0.0)
        self.assertEqual(self.DUT.pi_v, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKMilHdbkF) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKMilHdbkF) set_attributes should return a zero error code on success
        """

        _attributes = (0.00235, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMilHdbkF {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKMilHdbkF) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.00235, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 'None', 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMilHdbkF " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKMilHdbkF) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.00235, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKMilHdbkF.set_attributes().")
