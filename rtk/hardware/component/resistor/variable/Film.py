#!/usr/bin/env python
"""
########################################################
Hardware.Component.Resistor.Variable Package Film Module
########################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.variable.Film.py is part of the RTK
#       Project
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

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.resistor.Resistor import Model as Resistor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class VarFilm(Resistor):
    """
    The VarFilm Variable resistor data model contains the attributes and
    methods of a VarFilm Variable resistor.  The attributes of a
    VarFilm Variable resistor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 39

    :ivar int n_taps: the number of taps on the potentiometer.
    :ivar int style: the index in the style list for the resistor.
    :ivar int specification: the index in the specification list for the
                             resistor.
    :ivar float piTAPS: the MIL-HDBK-217FN2 taps factor.
    :ivar float piV: the MIL-HDBK-217FN2 voltage stress factor.

    Covers specifications MIL-R-23285 and MIL-R-39023.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.15
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 14.0, 7.0, 24.0, 6.0, 12.0, 20.0, 30.0, 39.0, 0.5,
                22.0, 57.0, 1000.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [2.0, 4.0]
    _lst_lambdab_count = [0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2,
                          2.3, 0.024, 1.2, 3.4, 52.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 39                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Variable Film resistor data model instance.
        """

        super(VarFilm, self).__init__()

        self.n_taps = 3
        self.specification = 0
        self.piTAPS = 0.0
        self.piV = 0.0

    def set_attributes(self, values):
        """
        Method to set the Variable Film resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.specification = int(values[118])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Variable Film resistor
        data model attributes.

        :return: (n_taps, specification, piTAPS, piV)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.specification, self.piTAPS,
                             self.piV)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Variable Film resistor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 12.
        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                if self.specification == 1:
                    self.base_hr = 0.018 * \
                                   exp(((self.temperature_active + 273.0) /
                                        343.0)**7.4) * \
                                   exp((_stress / 2.55) *
                                       ((self.temperature_active + 273.0) /
                                        273.0)**3.6)
                elif self.specification == 2:
                    self.base_hr = 0.0257 * \
                                   exp(((self.temperature_active + 273.0) /
                                        398.0)**7.9) * \
                                   exp((_stress / 2.45) *
                                       ((self.temperature_active + 273.0) /
                                        273.0)**4.3)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance <= 10000.0:
                self.piR = 1.0
            elif self.resistance > 100000.0 and self.resistance <= 50000.0:
                self.piR = 1.1
            elif self.resistance > 50000.0 and self.resistance <= 200000.0:
                self.piR = 1.2
            elif self.resistance > 200000.0 and self.resistance <= 1000000.0:
                self.piR = 1.4
            elif self.resistance > 1000000.0:
                self.piR = 1.8
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.8:
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.9 and
                 _v_applied / self.rated_voltage <= 1.0):
                self.piV = 1.20
            self.hazard_rate_model['piV'] = self.piV

        return Resistor.calculate_part(self)
