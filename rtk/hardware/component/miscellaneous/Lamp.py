#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Lamp.py is part of the RTK
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
####################################################
Hardware.Component.Miscellaneous Package Lamp Module
####################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.Component import Model as Component

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


class Lamp(Component):
    """
    The Lamp data model contains the attributes and methods of a Lamp
    component.  The attributes of an Lamp are:

    :cvar int category: the Component category.
    :cvar int subcategory: the Component subcategory.

    :ivar int application: the MIL-HDBK-217FN2 application list index.
    :ivar float illuminate_hours: the MIL-HDBK-217FN2 mission illumination
                                  hours.
    :ivar float operate_hours: the MIL-HDBK-217FN2 mission hours.
    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar float piU: the MIL-HDBK-217FN2 utilization factor.
    :ivar float piA: the MIL-HDBK-217FN2 application factor.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the lamp is overstressed.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 20.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piA = [1.0, 3.3]
    _lst_piE = [1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 5.0, 6.0, 5.0, 0.7, 4.0,
                6.0, 27.0]
    _lst_lambdab_count = [[3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0, 23.0,
                           19.0, 2.7, 16.0, 23.0, 100.0],
                          [13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0,
                           77.0, 64.0, 9.0, 51.0, 77.0, 350.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    category = 6
    subcategory = 4

    def __init__(self):
        """
        Method to initialize an Lamp data model instance.
        """

        super(Lamp, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.application = 0                # AC or DC lamp.
        self.illuminate_hours = 0.0         # Mission hours lamp is lit.
        self.operate_hours = 0.0            # Mission hours.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piU = 0.0                      # Utilization pi factor.
        self.piA = 0.0                      # Application pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Method to set the Lamp data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:127])

        try:
            self.application = int(values[116])
            self.illuminate_hours = float(values[127])
            self.operate_hours = float(values[128])
            self.base_hr = float(values[129])
            self.piU = float(values[130])
            self.piA = float(values[131])
            self.piE = float(values[132])
            self.reason = str(values[133])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Lamp data model
        attributes.

        :return: (application, illuminate_hours, operate_hours, base_hr,
                  piU, piA, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.application, self.illuminate_hours,
                             self.operate_hours, self.base_hr, self.piU,
                             self.piA, self.piE, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Lamp data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.base_hr = self._lst_lambdab_count[self.application - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piU * piA * piE'

            # Set the model's base hazard rate.
            self.base_hr = 0.074 * self.rated_voltage**1.29
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's utilization factor.
            if self.illuminate_hours / self.operate_hours < 0.10:
                self.piU = 0.10
            elif(self.illuminate_hours / self.operate_hours >= 0.10 and
                 self.illuminate_hours / self.operate_hours <= 0.90):
                self.piU = 0.72
            else:
                self.piU = 1.0
            self.hazard_rate_model['piU'] = self.piU

            # Set the application factor.
            self.piA = self._lst_piA[self.application - 1]
            self.hazard_rate_model['piA'] = self.piA

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        _keys = self.hazard_rate_model.keys()
        _values = self.hazard_rate_model.values()

        for i in range(len(_keys)):
            vars()[_keys[i]] = _values[i]

        self.hazard_rate_active = eval(self.hazard_rate_model['equation'])
        self.hazard_rate_active = (self.hazard_rate_active +
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / \
                                  Configuration.FRMULT

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
