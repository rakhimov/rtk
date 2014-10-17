#!/usr/bin/env python
"""
rotary.py contains the rotary switch component class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rotary.py is part of The RTK Project
#
#       Copyright 2007-2013 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved.

import gettext
import locale

from math import exp

try:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
from switch import Switch

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Rotary(Switch):
    """
    Rotary Switch Component Class.
    Covers specifications MIL-S-3786.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.3.
    """

    _application = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]
    _construction = ["", _(u"Ceramic RF Wafers"), _(u"Medium Power Wafers")]
    _quality = ["", u"MIL-SPEC", _(u"Lower")]

    def __init__(self):
        """
        Initializes the Rotary Switch Component Class.
        """

        Switch.__init__(self)

        self.subcategory = 69               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0,
                     0.5, 25.0, 67.0, 1200.0]
        self._lambdab_count = [0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2,
                               15.0, 0.16, 8.2, 22.0, 390.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Construction:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Rotary Switch Component Class prediction
        calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Switch.assessment_inputs_create(self, part, layout,
                                                   x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the component specific input widgets.
        part.cmbConstruction = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox()
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the component specific input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbApplication, _x_pos, _y_pos[0])
        layout.move(part.txtCycleRate, _x_pos, _y_pos[1])
        layout.move(part.txtCurrentRated, _x_pos, _y_pos[2])
        layout.move(part.txtCurrentOper, _x_pos, _y_pos[3])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[4])

        # Connect the component specific widgets to callback methods.
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Rotary Switch Component Class calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Switch.reliability_results_create(self, part, layout,
                                                     x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos)

        # Create the component specific reliability result display widgets.
        part.txtPiCYC = _widg.make_entry(width=100, editable=False, bold=True)
        # Create the piL Entry.  This value is stored in the pi_u field in the
        # program database.
        part.txtPiL = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.move(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.move(part.txtPiE, _x_pos, _y_pos[2])
        layout.put(part.txtPiCYC, _x_pos, _y_pos[3])
        layout.put(part.txtPiL, _x_pos, _y_pos[4])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Switch.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Switch.assessment_results_load(self, part)

        part.txtPiCYC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 71))))
        part.txtPiL.set_text(str(fmt.format(_model.get_value(_row, 82))))

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper Bypass Capacitor
        class.

        :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
        :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                     in List class gtk.TreeModel().
        :param gtk.TreeModel systemmodel: the RTK Hardware class
                                          gtk.TreeModel().
        :param gtk.TreeIter systemrow: the currently selected
                                       gtk.TreeIter() in the RTK Hardware
                                       class gtk.TreeModel().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        def _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part count hazard rate calculations for the
            Rotary Switch Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Qidx = partmodel.get_value(partrow, 85)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            if Qidx == 1:
                _hrmodel['piQ'] = 1.0
            else:
                _hrmodel['piQ'] = 50.0

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Rotary Switch Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piCYC * piL * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Aidx = partmodel.get_value(partrow, 5)
            Cidx = partmodel.get_value(partrow, 16)
            Cycles = partmodel.get_value(partrow, 19)
            n = partmodel.get_value(partrow, 40)
            Ioper = partmodel.get_value(partrow, 62)
            Qidx = partmodel.get_value(partrow, 85)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            if Qidx == 1:
                lambda_be = 0.0067
                if Cidx == 1:
                    lambda_b = 0.00003
                else:
                    lambda_b = 0.00003
            elif Qidx == 2:
                lambda_be = 0.10
                if Cidx == 1:
                    lambda_b = 0.02
                else:
                    lambda_b = 0.06
            else:
                lambda_be = 0.10
                lambda_b = 0.06

            _hrmodel['lambdab'] = lambda_be + n * lambda_b

            # Cycling Rate correction factor.
            if Cycles <= 1.0:
                _hrmodel['piCYC'] = 1.0
            else:
                _hrmodel['piCYC'] = Cycles

            # Load Stress correction factor.
            if Aidx == 1:                   # Resistive
                K = 0.8
            elif Aidx == 2:                 # Inductive
                K = 0.4
            elif Aidx == 3:                 # Lamp
                K = 0.2
            else:                           # Default
                K = 1.0

            S = Ioper / Irated
            _hrmodel['piL'] = exp((S / K) ** 2)

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            # Calculate the component dormant hazard rate.
            _lambdad = _calc.dormant_hazard_rate(_category_id, _subcategory_id,
                                                 _active_env, _dormant_env,
                                                 _lambdaa)

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 71, _hrmodel['piCYC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 82, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, _lambdad)
            systemmodel.set_value(systemrow, 32, _lambdap)
            systemmodel.set_value(systemrow, 60, _overstress)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        _calc_model = systemmodel.get_value(systemrow, 10)

        if _calc_model == 1:
            _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow)
        elif _calc_model == 2:
            _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow)

        return False
