#!/usr/bin/env python
"""
##########################################################################
Hardware.Component.Semiconductor.Optoelectronics Package LaserDiode Module
##########################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.optoelectronics.LaserDiode.py is
#       part of the RTK Project
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
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

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


class LaserDiode(Semiconductor):
    """
    The Optoelectronic Laser Diode data model contains the attributes and
    methods of an Optoelectronic Laser Diode component.  The attributes of an
    Optoelectronic Laser Diode are:

    :cvar int subcategory: default value: 24

    :ivar int type: default value: 0
    :ivar int application: default value: 0
    :ivar float required_power: default value: 0.0
    :ivar float piI: default value: 0.0
    :ivar float piA: default value: 0.0
    :ivar float piP: default value: 0.0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.13.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [3.23, 5.65]
    _lst_piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0,
                24.0, 450.0]
    _lst_piQ_count = [1.0, 1.0, 3.3]
    _lst_piQ_stress = [1.0, 1.0, 3.3]
    _lambdab_count = [[5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0,
                       230.0, 2.6, 87.0, 350.0, 2000.0],
                      [8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0,
                       300.0, 400.0, 4.5, 150.0, 600.0, 3500.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 24

    def __init__(self):
        """
        Method to initialize a Optoelectronic Laser Diode data model instance.
        """

        super(LaserDiode, self).__init__()

        # Define private list attributes.
        self._lst_lambdab_count = []

        # Define public scalar attributes.
        self.type = 0                       # Type index.
        self.application = 0                # Application index.
        self.required_power = 0.0           # Required optical power output.
        self.piI = 0.0                      #
        self.piA = 0.0
        self.piP = 0.0

    def set_attributes(self, values):
        """
        Method to set the Optoelectronic Laser Diode data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.type = int(values[117])
            self.application = int(values[118])
            self.required_power = float(values[101])
            self.piI = float(values[102])
            self.piA = float(values[103])
            self.piP = float(values[104])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Optoelectronic Laser Diode
        data model attributes.

        :return: (type, application, required_power, piI, piA, piP)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.type, self.application, self.required_power,
                             self.piI, self.piA, self.piP)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Optoelectronic Laser Diode
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self._lst_lambdab_count = self._lambdab_count[self.type - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piQ * piI * piA * piP * piE'

            # Set the base hazard rate for the model.
            if self.type == 1:
                self.base_hr = 3.23
            else:
                self.base_hr = 5.65
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-4635.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the forward current factor for the model.
            self.piI = self.operating_current**0.68
            self.hazard_rate_model['piI'] = self.piI

            # Set the application factor for the model.
            if self.application == 1:
                self.piA = 4.4
            else:
                self.piA = self.duty_cycle**0.5
            self.hazard_rate_model['piA'] = self.piA

            # Set the power degradation factor for the model.
            self.piP = 1.0 / \
                       (2.0 * (1.0 - (self.required_power / self.rated_power)))
            self.hazard_rate_model['piP'] = self.piP

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to dtermine whether the Optoelectronic Laser Diode is
        overstressed based on it's rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _reason = ''

        self.overstress = False

        if self.operating_voltage > 0.70 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                      ". Operating voltage > 70% rated voltage.\n"
            _reason_num += 1
        if self.junction_temperature > 125.0:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                      ". Junction temperature > 125.0C.\n"
            _reason_num += 1

        self.reason = _reason

        return False
