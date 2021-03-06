#!/usr/bin/env python -O
"""
This is the test class for testing Plastic capacitor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestPlastic.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.capacitor.fixed.Plastic import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPlasticFilmModel(unittest.TestCase):
    """
    Class for testing the Plastic Film capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Plastic Film Capacitor class.
        """

        self.DUT = Film()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPlasticFilm) __init__ should return a Plastic Film capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Film))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Plastic Button capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0,
                                         11.0, 20.0, 20.0, 0.5, 11.0, 29.0,
                                         530.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0021, 0.0042, 0.017,
                                                   0.010, 0.030, 0.0068, 0.013,
                                                   0.026, 0.048, 0.044, 0.0010,
                                                   0.023, 0.063, 1.1])
        self.assertEqual(self.DUT.subcategory, 42)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 338.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.030)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.0E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 65C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 338.0
        self.DUT.quality = 1
        self.DUT.specification = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001254613)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.820527619)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.37043496E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp_CQR(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 65C CQR specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 338.0
        self.DUT.quality = 1
        self.DUT.specification = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001254613)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.403325323)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.05637842E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_temp(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.specification = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00100153)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.820527619)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.09398790E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_temp(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.specification = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.000901055)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.820527619)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.84236964E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestPlasticFilm) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 170C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 443.0
        self.DUT.quality = 1
        self.DUT.specification = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.000886959)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.820527619)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.68839672E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPlasticFilm) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestPlasticFilm) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestPlasticPlasticModel(unittest.TestCase):
    """
    Class for testing the Plastic capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Plastic Capacitor class.
        """

        self.DUT = Plastic()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPlasticPlastic) __init__ should return a Plastic capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Plastic))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Plastic capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 10.0, 5.0, 16.0, 6.0, 11.0,
                                         18.0, 30.0, 23.0, 0.5, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0041, 0.0083, 0.042,
                                                   0.021, 0.067, 0.026, 0.048,
                                                   0.086, 0.14, 0.10, 0.0020,
                                                   0.054, 0.15, 2.5])
        self.assertEqual(self.DUT.subcategory, 44)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPlasticPlastic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.067)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.01E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestPlasticPlastic) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.00198303)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.196902034)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.42409526E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestPlasticPlastic) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0017840883)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.196902034)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.28122733E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPlasticPlastic) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestPlasticPlastic) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestSuperMetallizedPlasticModel(unittest.TestCase):
    """
    Class for testing the Super-Metallized Plastic capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Super-Metallized Plastic Capacitor class.
        """

        self.DUT = SuperMetallized()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSuperMetallizedPlastic) __init__ should return a Super-Metallized Plastic capacitor model
        """

        self.assertTrue(isinstance(self.DUT, SuperMetallized))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Super-Metallized Plastic capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [1.0, 4.0, 8.0, 5.0, 14.0, 4.0, 6.0,
                                         13.0, 20.0, 20.0, 0.5, 11.0, 29.0,
                                         530.0])
        self.assertEqual(self.DUT._piQ, [0.02, 0.1, 0.3, 1.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0023, 0.0092, 0.019,
                                                   0.012, 0.033, 0.0096, 0.014,
                                                   0.034, 0.053, 0.048, 0.0011,
                                                   0.026, 0.07, 1.2])
        self.assertEqual(self.DUT.subcategory, 45)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 398.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestSuperMetallizedPlastic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.033)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.6E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestSuperMetallizedPlastic) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0009911602)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 4.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.314821244)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.04255874E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestSuperMetallizedPlastic) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestSuperMetallizedPlastic) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
