#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.fixed.Composition.py is part of the RTK
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

"""
############################################################
Hardware.Component.Resistor.Fixed Package Composition Module
############################################################
"""

import gettext
import locale

try:
    import Configuration
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
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


class Composition(Resistor):
    """
    The Carbon Composition resistor data model contains the attributes and
    methods of a Carbon Composition resistor.  The attributes of a carbon
    composition resistor are:

    :cvar list _lst_piR: list of resistance factor values.
    :cvar list _lst_piE: list of environment factor values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for
                                   MIL-HDBK-217FN2 parts count.
    :cvar int subcategory: default value: 25

    Covers specifications MIL-R-11 and MIL-R-39008.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.1
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piR = [1.0, 1.1, 1.6, 2.5]
    _lst_piE = [1.0, 3.0, 8.0, 5.0, 13.0, 4.0, 5.0, 7.0, 11.0, 19.0, 0.5, 11.0,
                27.0, 490.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
    _lst_lambdab_count = [0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052,
                          0.0065, 0.016, 0.025, 0.025, 0.00025, 0.0098, 0.035,
                          0.36]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 25                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Carbon Composition resistor data model instance.
        """

        super(Composition, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Carbon Composition resistor
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piR * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.hazard_rate_model['lambdab'] = \
                    4.5E-9 * \
                    exp(12.0 * ((self.temperature_active + 273.0) / 343.0)) * \
                    exp((_stress / 0.6) * ((self.temperature_active +
                                            273.0) / 273.0))
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Resistance factor.
            if self.resistance < 100000.0:
                self.piR = 1.0
            elif self.resistance >= 100000.0 and self.resistance < 1.0E6:
                self.piR = 1.1
            elif self.resistance >= 1.0E6 and self.resistance < 1.0E7:
                self.piR = 1.6
            elif self.resistance >= 1.0E7:
                self.piR = 2.5
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate_part(self)
