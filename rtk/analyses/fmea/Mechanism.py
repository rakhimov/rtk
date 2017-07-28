#!/usr/bin/env python
"""
#####################
FMEA Mechanism Module
#####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Mechanism.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class OutOfRangeError(Exception):
    """
    Exception raised when an input value is outside legal limits.
    """

    def __init__(self, message):
        """
        Method to initialize OutOfRangeError instance.
        """

        Exception.__init__(self)

        self.message = message


class Model(object):
    """
    The Mechanism data model contains the attributes and methods of a FMEA
    failure mechanism.  A Mode will consist of one or more Mechanisms.
    The attributes of a Mechanism are:

    :ivar int mode_id: the ID of the failure Mode this failure Mechanism is
                       associated with.
    :ivar int mechanism_id: the failure Mechanism ID.
    :ivar str description: the description of the failure Mechanism.
    :ivar int rpn_occurrence: the Risk Priority Number occurrence rank before
                              action.
    :ivar int rpn_detection: the Risk Priority Number detection rank before
                             action.
    :ivar int rpn: the Risk Priority Number before action.
    :ivar int rpn_occurrence_new: the Risk Priority Number occurrence rank
                                  after action.
    :ivar int rpn_detection_new: the Risk Priority Number detection rank
                                 after action.
    :ivar int rpn_new: the Risk Priority Number after action.
    :ivar int include_pof: indicates whether or not to include the failure
                           Mechanism in the Physics of Failure analysis.
    """

    def __init__(self):
        """
        Method to initialize an Mechanism data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicCauses = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.mode_id = 0
        self.mechanism_id = 0
        self.description = ''
        self.rpn_occurrence = 10
        self.rpn_detection = 10
        self.rpn = 1000
        self.rpn_occurrence_new = 10
        self.rpn_detection_new = 10
        self.rpn_new = 1000
        self.include_pof = 0

    def calculate(self, severity, severity_new):
        """
        Method to calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Mechanism is associated
                             with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not 0 < severity < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_occurrence < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_detection < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN detection is outside the range "
                                    u"[1, 10]."))
        if not 0 < severity_new < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN new severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_occurrence_new < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN new occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_detection_new < 11:
            _return = True
            raise OutOfRangeError(_(u"RPN new detection is outside the range "
                                    u"[1, 10]."))

        self.rpn = int(severity) * int(self.rpn_occurrence) * \
                   int(self.rpn_detection)
        self.rpn_new = int(severity_new) * int(self.rpn_occurrence_new) * \
                   int(self.rpn_detection_new)

        return _return


class Mechanism(object):
    """
    The Mechanism data controller provides an interface between the Mechanism
    data model and an RTK view model.  A single Mechanism data controller can
    control one or more Mechanism data models.  Currently the Mechanism
    data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data controller instance.
        """

        pass
