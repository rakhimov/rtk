#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.relay.Relay.py is part of the RTK Project
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
#############################################
Hardware.Component.Relay Package Relay Module
#############################################
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


class Model(Component):
    """
    The Relay data model contains the attributes and methods of a Relay
    component.  The attributes of a Relay are:

    :cvar int category: default value: 6

    :ivar int quality: the index for the MIL-HDBK-217FN2 quality level.
    :ivar int construction: the index for the MIL-HDBK-217FN2 construction.
    :ivar float q_override: the user-defined quality factor.
    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar float piQ: the MIL-HDBK-217FN2 quality factor.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the Relay is over-stressed.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 13.
    """

    category = 6

    def __init__(self):
        """
        Method to initialize an Relay data model instance.
        """

        super(Model, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.
        self.lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Define public scalar attributes.
        self.quality = 0                    # Quality level.
        self.construction = 0               # Relay construction.
        self.q_override = 0.0               # User-defined piQ.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Method to set the Relay data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:127])

        try:
            self.quality = int(values[116])
            self.construction = int(values[117])
            self.q_override = float(values[127])
            self.base_hr = float(values[128])
            self.piQ = float(values[129])
            self.piE = float(values[130])
            self.reason = str(values[131])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Relay data model
        attributes.

        :return: (quality, construction, q_override, base_hr, piQ, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.construction, self.q_override,
                             self.base_hr, self.piQ, self.piE, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Relay data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

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

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
        Method to determine whether the Relay is overstressed based on it's
        rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _reason = ''

        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False
        # TODO: Update this after unpacking the book at the new house.
        if _harsh:
            if self.operating_current > 0.75 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 75% rated current.\n"
                _reason_num += 1
            # elif Aidx == 3 and Ioper > 0.40 * Irated:
            #     self.overstress = True
            #     _reason = _reason + str(_reason_num) + \
            #               ". Operating current > 40% rated current.\n"
            #     _reason_num += 1
        else:
            if self.operating_current > 0.90 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 90% rated current.\n"
                _reason_num += 1
            # elif Aidx == 3 and Ioper > 0.50 * Irated:
            #     self.overstress = True
            #     _reason = _reason + str(_reason_num) + \
            #               ". Operating current > 50% rated current.\n"
            #     _reason_num += 1

        self.reason = _reason

        return False
