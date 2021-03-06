#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestCoil.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Inductive Coil module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.inductor.Coil import Coil

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestCoilModel(unittest.TestCase):
    """
    Class for testing the Inductive Coil data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Inductive Coil class.
        """

        self.DUT = Coil()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        self._inductor_values = (1.0, 2.0, 3.0, 4.0, 5.0, 1, 2, 3, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestCoil) __init__ should return an Inductive Coil data model
        """

        self.assertTrue(isinstance(self.DUT, Coil))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Inductor class was properly initialized.
        self.assertEqual(self.DUT.category, 5)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Inductive Coil class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 63)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.piC, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestCoil) set_attributes should return a 0 error code on success
        """

        _my_values = (1.0, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._inductor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.construction, 2)
        self.assertEqual(self.DUT.piC, 1.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestCoil) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (1.0, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._inductor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestCoil) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (None, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._inductor_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestCoil) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, 0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestCoil) get_attributes(set_attributes(values)) == values
        """

        _my_values = (1.0, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._inductor_values + \
                  _my_values

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:104], self._inductor_values)

        self.assertEqual(_result[104:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestCoil) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.031)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.3E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_delta_t(self):
        """
        (TestCoil) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 3
        self.DUT.specification = 2
        self.DUT.insulation_class = 1
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piC * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0004903725)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 0.3)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.8844695E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_delta_t(self):
        """
        (TestCoil) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 3
        self.DUT.specification = 2
        self.DUT.insulation_class = 2
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piC * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0005663419)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 0.3)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.7961032E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mil_c_15035(self):
        """
        (TestCoil) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 3

        self.DUT.specification = 1
        self.DUT.insulation_class = 4

        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piC * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0003809064)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 0.3)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.5708767E-10)
