#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.BoM.py is part of The RTK Project
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
###############################################
Hardware Package Bill of Materials (BoM) Module
###############################################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    from hardware.assembly.Assembly import Model as Assembly
    from hardware.component.Component import Model as Component
    import hardware.component.capacitor.electrolytic.Aluminum as Aluminum
    import hardware.component.capacitor.electrolytic.Tantalum as Tantalum
    import hardware.component.capacitor.fixed.Ceramic as Ceramic
    import hardware.component.capacitor.fixed.Glass as Glass
    import hardware.component.capacitor.fixed.Mica as Mica
    import hardware.component.capacitor.fixed.Paper as Paper
    import hardware.component.capacitor.fixed.Plastic as Plastic
    import hardware.component.capacitor.variable.Variable as Variable
    import hardware.component.connection.Multipin as Multipin
    import hardware.component.connection.PCB as PCB
    import hardware.component.connection.Socket as Socket
    import hardware.component.connection.Solder as Solder
    import hardware.component.inductor.Coil as Coil
    import hardware.component.inductor.Transformer as Transformer
    import hardware.component.integrated_circuit.Linear as Linear
    import hardware.component.integrated_circuit.Logic as Logic
    import hardware.component.integrated_circuit.PALPLA as PALPLA
    import hardware.component.integrated_circuit.Microprocessor as \
        Microprocessor
    import hardware.component.integrated_circuit.Memory as Memory
    import hardware.component.integrated_circuit.GaAs as GaAs
    import hardware.component.integrated_circuit.VLSI as VLSI
    import hardware.component.meter.Meter as Meter
    import hardware.component.miscellaneous.Crystal as Crystal
    import hardware.component.miscellaneous.Filter as Filter
    import hardware.component.miscellaneous.Fuse as Fuse
    import hardware.component.miscellaneous.Lamp as Lamp
    import hardware.component.relay.Mechanical as Mechanical
    import hardware.component.relay.SolidState as SolidState
    import hardware.component.resistor.fixed.Composition as Composition
    import hardware.component.resistor.fixed.Film as Film
    import hardware.component.resistor.fixed.Wirewound as Wirewound
    import hardware.component.resistor.variable.Composition as VarComposition
    import hardware.component.resistor.variable.Film as VarFilm
    import hardware.component.resistor.variable.NonWirewound as NonWirewound
    import hardware.component.resistor.variable.Thermistor as Thermistor
    import hardware.component.resistor.variable.Wirewound as VarWirewound
    import hardware.component.semiconductor.Diode as Diode
    import hardware.component.semiconductor.transistor.Bipolar as Bipolar
    import hardware.component.semiconductor.transistor.FET as FET
    import hardware.component.semiconductor.transistor.Unijunction as \
        Unijunction
    import hardware.component.semiconductor.Thyristor as Thyristor
    import hardware.component.semiconductor.optoelectronic.Detector as \
        Detector
    import hardware.component.semiconductor.optoelectronic.Display as Display
    import hardware.component.semiconductor.optoelectronic.LaserDiode as \
        LaserDiode
    import hardware.component.switch.Breaker as Breaker
    import hardware.component.switch.Rotary as Rotary
    import hardware.component.switch.Sensitive as Sensitive
    import hardware.component.switch.Thumbwheel as Thumbwheel
    import hardware.component.switch.Toggle as Toggle
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.hardware.assembly.Assembly import Model as Assembly
    from rtk.hardware.component.Component import Model as Component
    import rtk.hardware.component.capacitor.electrolytic.Aluminum as Aluminum
    import rtk.hardware.component.capacitor.electrolytic.Tantalum as Tantalum
    import rtk.hardware.component.capacitor.fixed.Ceramic as Ceramic
    import rtk.hardware.component.capacitor.fixed.Glass as Glass
    import rtk.hardware.component.capacitor.fixed.Mica as Mica
    import rtk.hardware.component.capacitor.fixed.Paper as Paper
    import rtk.hardware.component.capacitor.fixed.Plastic as Plastic
    import rtk.hardware.component.capacitor.variable.Variable as Variable
    import rtk.hardware.component.connection.Multipin as Multipin
    import rtk.hardware.component.connection.PCB as PCB
    import rtk.hardware.component.connection.Socket as Socket
    import rtk.hardware.component.connection.Solder as Solder
    import rtk.hardware.component.inductor.Coil as Coil
    import rtk.hardware.component.inductor.Transformer as Transformer
    import rtk.hardware.component.integrated_circuit.Linear as Linear
    import rtk.hardware.component.integrated_circuit.Logic as Logic
    import rtk.hardware.component.integrated_circuit.PALPLA as PALPLA
    import rtk.hardware.component.integrated_circuit.Microprocessor as \
        Microprocessor
    import rtk.hardware.component.integrated_circuit.Memory as Memory
    import rtk.hardware.component.integrated_circuit.GaAs as GaAs
    import rtk.hardware.component.integrated_circuit.VLSI as VLSI
    import rtk.hardware.component.meter.Meter as Meter
    import rtk.hardware.component.miscellaneous.Crystal as Crystal
    import rtk.hardware.component.miscellaneous.Filter as Filter
    import rtk.hardware.component.miscellaneous.Fuse as Fuse
    import rtk.hardware.component.miscellaneous.Lamp as Lamp
    import rtk.hardware.component.relay.Mechanical as Mechanical
    import rtk.hardware.component.relay.SolidState as SolidState
    import rtk.hardware.component.resistor.fixed.Composition as Composition
    import rtk.hardware.component.resistor.fixed.Film as Film
    import rtk.hardware.component.resistor.fixed.Wirewound as Wirewound
    import rtk.hardware.component.resistor.variable.Composition as \
        VarComposition
    import rtk.hardware.component.resistor.variable.Film as VarFilm
    import rtk.hardware.component.resistor.variable.NonWirewound as \
        NonWirewound
    import rtk.hardware.component.resistor.variable.Thermistor as Thermistor
    import rtk.hardware.component.resistor.variable.Wirewound as VarWirewound
    import rtk.hardware.component.semiconductor.Diode as Diode
    import rtk.hardware.component.semiconductor.transistor.Bipolar as Bipolar
    import rtk.hardware.component.semiconductor.transistor.FET as FET
    import rtk.hardware.component.semiconductor.transistor.Unijunction as \
        Unijunction
    import rtk.hardware.component.semiconductor.Thyristor as Thyristor
    import rtk.hardware.component.semiconductor.optoelectronic.Detector as \
        Detector
    import rtk.hardware.component.semiconductor.optoelectronic.Display as \
        Display
    import rtk.hardware.component.semiconductor.optoelectronic.LaserDiode as \
        LaserDiode
    import rtk.hardware.component.switch.Breaker as Breaker
    import rtk.hardware.component.switch.Rotary as Rotary
    import rtk.hardware.component.switch.Sensitive as Sensitive
    import rtk.hardware.component.switch.Thumbwheel as Thumbwheel
    import rtk.hardware.component.switch.Toggle as Toggle

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def load_capacitor(subcategory):
    """
    Function to load the capacitor data model.

    :param int subcategory: the subcategory of the capacitor data model to load.
    :return: _component
    :rtype: an instance of the appropriate capacitor data model.
    """

    _dicCapacitors = {1: Paper.Bypass(), 2: Paper.Feedthrough(),
                      3: Plastic.Film(), 4: Paper.Metallized(),
                      5: Plastic.Plastic(), 6: Plastic.SuperMetallized(),
                      7: Mica.Mica(), 8: Mica.Button(), 9: Glass.Glass(),
                      10: Ceramic.General(), 11: Ceramic.Chip(),
                      12: Tantalum.Solid(), 13: Tantalum.NonSolid(),
                      14: Aluminum.Wet(), 15: Aluminum.Dry(),
                      16: Variable.Ceramic(), 17: Variable.Piston(),
                      18: Variable.AirTrimmer(), 19: Variable.Vacuum()}
    _component = _dicCapacitors[subcategory]

    return _component


def load_connection(subcategory):
    """
    Function to load the connection data model.

    :param int subcategory: the subcategory of the connection data model to load.
    :return: _component
    :rtype: an instance of the appropriate connection data model.
    """

    _dicConnection = {1: Multipin.Multipin(), 2: PCB.PCB(), 3: Socket.Socket(),
                      4: Solder.PTH(), 5: Solder.NonPTH()}
    _component = _dicConnection[subcategory]

    return _component


def load_inductor(subcategory):
    """
    Function to load the inductor data model.

    :param int subcategory: the subcategory of the inductor data model to load.
    :return: _component
    :rtype: an instance of the appropriate inductor data model.
    """

    _dicInductor = {1: Transformer.Transformer(), 2: Coil.Coil()}
    _component = _dicInductor[subcategory]

    return _component


def load_integrated_circuit(subcategory):
    """
    Function to load the integrated circuit data model.

    :param int subcategory: the subcategory of the integrated circuit data model to 
                            load.
    :return: _component
    :rtype: an instance of the appropriate integrated circuit data model.
    """

    _dicIC = {1: Linear.Linear(), 2: Logic.Logic(), 3: PALPLA.PALPLA(),
              4: Microprocessor.Microprocessor(), 5: Memory.ROM(),
              6: Memory.EEPROM(), 7: Memory.DRAM(), 8: Memory.SRAM(),
              9: GaAs.GaAs(), 10: VLSI.VLSI()}
    _component = _dicIC[subcategory]

    return _component


def load_meter(subcategory):
    """
    Function to load the meter data model.

    :param int subcategory: the subcategory of the meter data model to load.
    :return: _component
    :rtype: an instance of the appropriate meter data model.
    """

    _dicMeter = {1: Meter.ElapsedTime(), 2: Meter.Panel()}
    _component = _dicMeter[subcategory]

    return _component


def load_miscellaneous(subcategory):
    """
    Function to load the miscellaneous data model.

    :param int subcategory: the subcategory of the miscellaneous data model to load.
    :return: _component
    :rtype: an instance of the appropriate miscellaneous data model.
    """

    _dicMisc = {1: Crystal.Crystal(), 2: Filter.Filter(), 3: Fuse.Fuse(),
                4: Lamp.Lamp()}
    _component = _dicMisc[subcategory]

    return _component


def load_relay(subcategory):
    """
    Function to load the relay data model.

    :param int subcategory: the subcategory of the relay data model to load.
    :return: _component
    :rtype: an instance of the appropriate relay data model.
    """

    _dicRelay = {1: Mechanical.Mechanical(), 2: SolidState.SolidState()}
    _component = _dicRelay[subcategory]

    return _component


def load_resistor(subcategory):
    """
    Function to load the resistor data model.

    :param int subcategory: the subcategory of the resistor data model to load.
    :return: _component
    :rtype: an instance of the appropriate resistor data model.
    """

    _dicResistor = {1: Composition.Composition(), 2: Film.Film(),
                    3: Film.FilmPower(), 4: Film.FilmNetwork(),
                    5: Wirewound.Wirewound(), 6: Wirewound.WirewoundPower(),
                    7: Wirewound.WirewoundChassisMount(),
                    8: Thermistor.Thermistor(), 9: VarWirewound.VarWirewound(),
                    10: VarWirewound.PrecisionWirewound(),
                    11: VarWirewound.SemiPrecisionWirewound(),
                    12: VarWirewound.PowerWirewound(),
                    13: NonWirewound.NonWirewound(),
                    14: VarComposition.VarComposition(), 15: VarFilm.VarFilm()}
    _component = _dicResistor[subcategory]

    return _component


def load_semiconductor(subcategory):
    """
    Function to load the semiconductor data model.

    :param int subcategory: the subcategory of the semiconductor data model to load.
    :return: _component
    :rtype: an instance of the appropriate semiconductor data model.
    """

    _dicSemiconductors = {1: Diode.LowFrequency(), 2: Diode.HighFrequency(),
                          3: Bipolar.LFBipolar(), 4: FET.LFSiFET(),
                          5: Unijunction.Unijunction(),
                          6: Bipolar.HFLNBipolar(), 7: Bipolar.HFHPBipolar(),
                          8: FET.HFGaAsFET(), 9: FET.HFSiFET(),
                          10: Thyristor.Thyristor(), 11: Detector.Detector(),
                          12: Display.Display(), 13: LaserDiode.LaserDiode()}
    _component = _dicSemiconductors[subcategory]

    return _component


def load_switch(subcategory):
    """
    Function to load the switch data model.

    :param int subcategory: the subcategory of the switch data model to load.
    :return: _component
    :rtype: an instance of the appropriate switch data model.
    """

    _dicSwitch = {1: Toggle.Toggle(), 2: Sensitive.Sensitive(),
                  3: Rotary.Rotary(), 4: Thumbwheel.Thumbwheel(),
                  5: Breaker.Breaker()}
    _component = _dicSwitch[subcategory]

    return _component


class ParentError(Exception):
    """
    Exception raised when a revision ID is not passed or when initializing an
    instance of the BoM model.
    """

    pass


class BoM(object):
    
    """
    The BoM data controller provides an interface between the BoM data model and an 
    RTK view model.  A single BoM data controller can manage one or more BoM data 
    models.  The attributes of a BoM data controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar _last_id: the last Hardware ID used.
    :ivar dicHardware: Dictionary of the Hardware data models managed.  Key is
                       the Hardware ID; value is a pointer to the Hardware data
                       model instance.
    """

    def __init__(self):
        """ Method to initialize a BoM data controller instance. """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Define private scalar attributes.
        self._last_id = None

        # Define public dictionary attributes.
        self.dicHardware = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def request_bom(self, revision_id):
        """
        Method to read the RTK Project database and load all the Hardware associated 
        with the selected Revision.  For each hardware item returned:

        #. Retrieve the hardware assemblies and components from the RTK Project
           database.
        #. Create an Assembly or Component data model instance as appropriate.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of hardware being managed
           by this controller.

        :param int revision_id: the Revision ID to select the requirements for.
        :return: (_results, _error_code)
        :rtype: tuple
        """
        # TODO: Consider refactoring request_bom; current McCabe Complexity metric = 14.
        self._last_id = self.dao.get_last_id('rtk_hardware')[0]

        # Select everything from the hardware, stress, reliability, and
        # maintainability tables.
        _query = "SELECT t1.fld_revision_id, t1.fld_hardware_id, \
                         t1.fld_alt_part_number, t1.fld_attachments, \
                         t1.fld_cage_code, t1.fld_comp_ref_des, t1.fld_cost, \
                         t1.fld_cost_failure, t1.fld_cost_hour, \
                         t1.fld_description, t1.fld_duty_cycle, \
                         t1.fld_environment_active, \
                         t1.fld_environment_dormant, t1.fld_figure_number, \
                         t1.fld_humidity, t1.fld_lcn, t1.fld_level, \
                         t1.fld_manufacturer, t1.fld_mission_time, \
                         t1.fld_name, t1.fld_nsn, t1.fld_overstress, \
                         t1.fld_page_number, t1.fld_parent_id, t1.fld_part, \
                         t1.fld_part_number, t1.fld_quantity, t1.fld_ref_des, \
                         t1.fld_reliability_goal, \
                         t1.fld_reliability_goal_measure, \
                         t1.fld_remarks, t1.fld_rpm, \
                         t1.fld_specification_number, \
                         t1.fld_tagged_part, t1.fld_temperature_active, \
                         t1.fld_temperature_dormant, t1.fld_vibration, \
                         t1.fld_year_of_manufacture, t2.fld_current_ratio, \
                         t2.fld_max_rated_temperature, \
                         t2.fld_min_rated_temperature, \
                         t2.fld_operating_current, t2.fld_operating_power, \
                         t2.fld_operating_voltage, t2.fld_power_ratio, \
                         t2.fld_rated_current, t2.fld_rated_power, \
                         t2.fld_rated_voltage, t2.fld_temperature_rise, \
                         t2.fld_voltage_ratio, t3.fld_add_adj_factor, \
                         t3.fld_availability_logistics, \
                         t3.fld_availability_mission, \
                         t3.fld_avail_log_variance, \
                         t3.fld_avail_mis_variance, \
                         t3.fld_failure_dist, t3.fld_failure_parameter_1, \
                         t3.fld_failure_parameter_2, \
                         t3.fld_failure_parameter_3, \
                         t3.fld_hazard_rate_active, \
                         t3.fld_hazard_rate_dormant, \
                         t3.fld_hazard_rate_logistics, \
                         t3.fld_hazard_rate_method, \
                         t3.fld_hazard_rate_mission, \
                         t3.fld_hazard_rate_model, \
                         t3.fld_hazard_rate_percent, \
                         t3.fld_hazard_rate_software, \
                         t3.fld_hazard_rate_specified, \
                         t3.fld_hazard_rate_type, t3.fld_hr_active_variance, \
                         t3.fld_hr_dormant_variance, \
                         t3.fld_hr_logistics_variance, \
                         t3.fld_hr_mission_variance, \
                         t3.fld_hr_specified_variance, \
                         t3.fld_mtbf_logistics, t3.fld_mtbf_mission, \
                         t3.fld_mtbf_specified, t3.fld_mtbf_log_variance, \
                         t3.fld_mtbf_miss_variance, \
                         t3.fld_mtbf_spec_variance, t3.fld_mult_adj_factor, \
                         t3.fld_reliability_logistics, \
                         t3.fld_reliability_mission, \
                         t3.fld_rel_log_variance, t3.fld_rel_miss_variance, \
                         t3.fld_survival_analysis, t1.fld_cost_type, \
                         t1.fld_repairable, t1.fld_total_part_quantity, \
                         t1.fld_total_power_dissipation, \
                         t1.fld_category_id, t1.fld_subcategory_id, \
                         t2.fld_junction_temperature, \
                         t2.fld_knee_temperature, t2.fld_thermal_resistance, \
                         t2.fld_tref, t2.fld_reason, t3.fld_float1, t3.fld_float2, \
                         t3.fld_float3, t3.fld_float4, t3.fld_float5, \
                         t3.fld_float6, t3.fld_float7, t3.fld_float8, \
                         t3.fld_float9, t3.fld_float10, t3.fld_float11, \
                         t3.fld_float12, t3.fld_float13, t3.fld_float14, \
                         t3.fld_float15, t3.fld_float16, t3.fld_float17, \
                         t3.fld_float18, t3.fld_float19, t3.fld_float20, \
                         t3.fld_int1, t3.fld_int2, t3.fld_int3, t3.fld_int4, \
                         t3.fld_int5, t3.fld_int6, t3.fld_int7, t3.fld_int8, \
                         t3.fld_int9, t3.fld_int10, t3.fld_varchar1, \
                         t3.fld_varchar2, t3.fld_varchar3, t3.fld_varchar4, \
                         t3.fld_varchar5 \
            FROM rtk_hardware AS t1 \
            INNER JOIN rtk_stress AS t2 \
            ON t2.fld_hardware_id=t1.fld_hardware_id \
            INNER JOIN rtk_reliability AS t3 \
            ON t3.fld_hardware_id=t1.fld_hardware_id \
            WHERE t1.fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _n_assemblies = len(_results)
        except TypeError:
            _n_assemblies = 0

        for i in range(_n_assemblies):
            if _results[i][24] == 0:
                _hardware = Assembly()
                _hardware.set_attributes(_results[i])
                self.dicHardware[_hardware.hardware_id] = _hardware
            elif _results[i][24] == 1:
                self.load_component(_results[i])

        for _key in self.dicHardware.keys():
            _hardware = self.dicHardware[_key]
            for _key2 in self.dicHardware.keys():
                _hardware2 = self.dicHardware[_key2]
                if(_hardware2.parent_id == _hardware.hardware_id and
                   _hardware2.part == 0):
                    try:
                        _hardware.dicAssemblies[_hardware.hardware_id].append(_hardware2)
                    except KeyError:
                        _hardware.dicAssemblies[_hardware.hardware_id] = [_hardware2]
                elif(_hardware2.parent_id == _hardware.hardware_id and
                     _hardware2.part == 1):
                    try:
                        _hardware.dicComponents[_hardware.hardware_id].append(_hardware2)
                    except KeyError:
                        _hardware.dicComponents[_hardware.hardware_id] = [_hardware2]

        return(_results, _error_code)

    def load_component(self, attributes):
        """
        Method to load the correct Component based on the category and
        subcategory ID's.

        :param tuple attributes: the attributes of the component to load.
        :return: an instance of the appropriate Component class.
        :rtype: object
        """
        # TODO: Consider refactoring load_component; current McCabe Complexity metric = 12.
        # Select the correct component type and create an instance of it's
        # data model.
        if attributes[90] < 1 or attributes[91] < 1:
            _component = Component()
        elif attributes[90] == 1:
            _component = load_capacitor(attributes[91])
        elif attributes[90] == 2:
            _component = load_connection(attributes[91])
        elif attributes[90] == 3:
            _component = load_inductor(attributes[91])
        elif attributes[90] == 4:
            _component = load_integrated_circuit(attributes[91])
        elif attributes[90] == 5:
            _component = load_meter(attributes[91])
        elif attributes[90] == 6:
            _component = load_miscellaneous(attributes[91])
        elif attributes[90] == 7:
            _component = load_relay(attributes[91])
        elif attributes[90] == 8:
            _component = load_resistor(attributes[91])
        elif attributes[90] == 9:
            _component = load_semiconductor(attributes[91])
        elif attributes[90] == 10:
            _component = load_switch(attributes[91])

        # Set the attributes of the component and add it to the dictionary of
        # hardware items managed by this controller.
        _component.set_attributes(attributes)
        self.dicHardware[_component.hardware_id] = _component

        # Set the hardware as a part/component.
        _component.part = 1

        return _component

    def add_hardware(self, revision_id, hardware_type, parent_id=None):
        """
        Method to add a new Hardware item to the RTK Project for the selected
        Revision.

        :param int revision_id: the Revision ID to add the new Hardware
                                item(s).
        :param int hardware_type: the type of Hardware item to add.
                                  * 0 = Assembly
                                  * 1 = Component
        :keyword int parent_id: the Hardware ID of the parent hardware item.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # By default we add the new Hardware item as an immediate child of the
        # top-level assembly.
        if parent_id is None:
            # FIXME: See bug 191.
            parent_id = 0

        _query = "INSERT INTO rtk_hardware \
                  (fld_revision_id, fld_parent_id, fld_part) \
            VALUES({0:d}, {1:d}, {2:d})".format(revision_id, parent_id, 
                                                hardware_type)
        (_results, _error_code, _hardware_id) = self.dao.execute(_query,
                                                                  commit=True)

        # If the new hardware item was added successfully to the RTK Project
        # database, add a record to the stress table in the RTK Project
        # database.
        if _results:
            _query = "INSERT INTO rtk_stress (fld_hardware_id) \
                VALUES({0:d})".format(_hardware_id)
            (_results, _error_code, _) = self.dao.execute(_query, commit=True)

        # If the record was successfully added to the stress table, add a
        # record to the reliability table.
        if _results:
            _query = "INSERT INTO rtk_reliability (fld_hardware_id) \
                VALUES({0:d})".format(_hardware_id)
            (_results, _error_code, _) = self.dao.execute(_query, commit=True)

        # If the new hardware item was added successfully to all the tables in
        # the RTK Project database:
        #   1. Retrieve the ID of the newly inserted hardware item.
        #   2. Create a new Assembly or Component data model instance.
        #   3. Set the attributes of the new Assembly or Component data model
        #      instance.
        #   4. Add the new Assembly or Component model to the controller
        #      dictionary.
        if _results:
            self._last_id = self.dao.get_last_id('rtk_hardware')[0]
            if hardware_type == 0:
                _hardware = Assembly()
            elif hardware_type == 1:
                _hardware = Component()

            _hardware.set_attributes((revision_id, self._last_id, '', '', '',
                                      '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                                      50.0, '', 1, 0, 10.0, '', '', 0, '',
                                      parent_id, hardware_type, '', 1, '',
                                      1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                                      2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                                      1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                                      0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0,
                                      1, 0, 0.0))
            self.dicHardware[_hardware.hardware_id] = _hardware

        return(_hardware, _error_code)

    def delete_hardware(self, hardware_id):
        """
        Method to delete a Hardware item from the RTK Project database.

        :param int hardware_id: the Hardware ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete all the child hardware, if any.
        _query = "DELETE FROM rtk_hardware \
                  WHERE fld_parent_id={0:d}".format(hardware_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        # Then delete the parent hardware.
        _query = "DELETE FROM rtk_hardware \
                  WHERE fld_hardware_id={0:d}".format(hardware_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        self.dicHardware.pop(hardware_id)

        return(_results, _error_code)

    def copy_hardware(self, revision_id, failure_info=True, matrix=True):
        """
        Method to copy a Hardware item from the currently selected Revision to
        the new Revision.

        :param int revision_id: the ID of the newly created Revision.
        :keyword bool failure_info: indicates whether or not to copy failure
                                    information from the old Hardware to the
                                    new Hardware.
        :keyword bool matrix: indicates whether or not to copy functional
                              matrix information from the old Hardware to the
                              new Hardware.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Consider refactoring copy_hardware; current McCabe Complexity index = 14.
        # FIXME: Write one or more integration tests for copy_hardware.
        # Find the existing maximum Hardware ID already in the RTK Program
        # database and increment it by one.  If there are no existing
        # Hardware items set the first Hardware ID to zero.
        _query = "SELECT MAX(fld_hardware_id) FROM rtk_hardware"
        (_hardware_id, _error_code, __) = self.dao.execute(_query,
                                                            commit=False)

        if _hardware_id[0][0] is not None:
            _hardware_id = _hardware_id[0][0] + 1
        else:
            _hardware_id = 0

        # Copy the Hardware hierarchy for the new Revision.
        _dic_index_xref = {}
        _dic_index_xref[-1] = -1
        for _hardware in self.dicHardware.values():
            # Set the category and subcategory ID's to zero for assemblies.
            if _hardware.part != 1:
                _category_id = 0
                _subcategory_id = 0
            else:
                _category_id = _hardware.category_id
                _subcategory_id = _hardware.subcategory_id

            _query = "INSERT INTO rtk_hardware \
                      (fld_revision_id, fld_hardware_id, fld_cage_code, \
                       fld_category_id, fld_description, fld_figure_number, \
                       fld_lcn, fld_level, fld_manufacturer, \
                       fld_mission_time, fld_name, fld_nsn, fld_page_number, \
                       fld_parent_id, fld_part, fld_part_number, \
                       fld_quantity, fld_ref_des, fld_remarks, \
                       fld_specification_number, fld_subcategory_id) \
                      VALUES ({0:d}, {1:d}, '{2:s}', {3:d}, '{4:s}', '{5:s}', \
                              '{6:s}', {7:d}, {8:d}, {9:f}, '{10:s}', \
                              '{11:s}', '{12:s}', {13:d}, {14:d}, '{15:s}', \
                              {16:d}, '{17:s}', '{18:s}', '{19:s}', \
                              {20:d})".format(revision_id, _hardware_id,
                                              _hardware.cage_code,
                                              _category_id,
                                              _hardware.description,
                                              _hardware.figure_number,
                                              _hardware.lcn, _hardware.level,
                                              _hardware.manufacturer,
                                              _hardware.mission_time,
                                              _hardware.name, _hardware.nsn,
                                              _hardware.page_number,
                                              _hardware.parent_id,
                                              _hardware.part,
                                              _hardware.part_number,
                                              _hardware.quantity,
                                              _hardware.ref_des,
                                              _hardware.remarks,
                                              _hardware.specification_number,
                                              _subcategory_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            if failure_info:
                # FIXME: See bug 192.
                _query = "INSERT INTO rtk_reliability \
                    (fld_hardware_id, fld_hazard_rate_active, \
                     fld_hazard_rate_dormant, fld_hazard_rate_software, \
                     fld_hazard_rate_specified, fld_hazard_rate_type, \
                     fld_mtbf_logistics, fld_mtbf_specified, \
                     fld_add_adj_factor, fld_failure_dist, \
                     fld_failure_parameter_1, fld_failure_parameter_2, \
                     fld_failure_parameter_3, fld_hazard_rate_method, \
                     fld_hazard_rate_model, fld_mult_adj_factor, \
                     fld_survival_analysis, fld_float_1, fld_float_2, \
                     fld_float_3, fld_float_4, fld_float_5, fld_float_6, \
                     fld_float_7, fld_float_8, fld_float_9, fld_float_10, \
                     fld_float_11, fld_float_12, fld_float_13, fld_float_14, \
                     fld_float_15, fld_float_16, fld_float_17, fld_float_18, \
                     fld_float_19, fld_float_20, fld_int_1, fld_int_2, fld_int_3, \
                     fld_int_4, fld_int_5, fld_int_6, fld_int_7, fld_int_8, \
                     fld_int_9, fld_int_10, fld_varchar_1, fld_varchar_2, \
                     fld_varchar_3, fld_varchar_4, fld_varchar_5) \
                    VALUES ({0:d}, {1:f}, {2:f}, {3:f}, {4:f}, {5:d}, {6:f}, \
                    {7:f}, {8:f}, {9:d}, {10:f}, {11:f}, {12:f}, {13:d}, '{14:s}', \
                    {15:f}, {16:d})".format(_hardware_id, 
                                           _hardware.hazard_rate_active,
                                           _hardware.hazard_rate_dormant,
                                           _hardware.hazard_rate_software,
                                           _hardware.hazard_rate_specified,
                                           _hardware.hazard_rate_type,
                                           _hardware.mtbf_logistics,
                                           _hardware.mtbf_specified, 
                                           _hardware.add_adj_factor, 
                                           _hardware.failure_dist, 
                                           _hardware.failure_parameter_1, 
                                           _hardware.failure_parameter_2, 
                                           _hardware.failure_parameter_3, 
                                           _hardware.hazard_rate_method, 
                                           _hardware.hazard_rate_model, 
                                           _hardware.mult_adj_factor, 
                                           _hardware.survival_analysis)
                (_results, _error_code, __) = self.dao.execute(_query,
                                                                commit=True)

            # Add the Hardware item to the prediction table if it's a part.
            # Otherwise add it to the similar item table.
            if _hardware.part == 1:
                _query = "INSERT INTO rtk_prediction \
                          (fld_hardware_id) \
                          VALUES ({0:d})".format(_hardware_id)
            else:
                _query = "INSERT INTO rtk_similar_item \
                          (fld_hardware_id) \
                          VALUES ({0:d})".format(_hardware_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            _query = "INSERT INTO rtk_allocation \
                      (fld_hardware_id) \
                      VALUES ({0:d})".format(_hardware_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            _query = "INSERT INTO rtk_hazard \
                      (fld_hardware_id) \
                      VALUES ({0:d})".format(_hardware_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            _query = "INSERT INTO rtk_stress \
                      (fld_hardware_id) \
                      VALUES ({0:d})".format(_hardware_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            if matrix:
                _query = "SELECT MAX(fld_matrix_id) FROM rtk_matrices"
                (_matrix_id, _error_code, __) = self.dao.execute(_query,
                                                                  commit=False)

                if _matrix_id[0][0] is not None:
                    _matrix_id = _matrix_id[0][0] + 1
                else:
                    _matrix_id = 0

                _query = "SELECT fld_function_id \
                          FROM tbl_functions \
                          WHERE fld_revision_id=%d" % revision_id
                (_function_ids,
                 _error_code,
                 __) = self.dao.execute(_query, commit=False)

                for __, _function_id in enumerate(_function_ids):
                    _query = "INSERT INTO rtk_matrices \
                              (fld_revision_id, fld_matrix_type, \
                               fld_matrix_id, fld_row_id, fld_col_id) \
                              VALUES({0:d}, 0, {1:d}, \
                                     {2:d}, {3:d})".format(revision_id,
                                                           _matrix_id,
                                                           _hardware_id,
                                                           _function_id[0])
                    (_results,
                     _error_code,
                     __) = self.dao.execute(_query, commit=True)

            # Add an entry to the Hardware ID cross-reference dictionary for
            # for the newly added Hardware item.
            _dic_index_xref[_hardware.hardware_id] = _hardware_id

            _hardware_id += 1

        # Update the parent IDs for the new Hardware items using the index
        # cross-reference dictionary that was created when adding the new
        # Hardware items.
        for _key in _dic_index_xref.keys():
            _query = "UPDATE rtk_hardware \
                      SET fld_parent_id={0:d} \
                      WHERE fld_parent_id={1:d} \
                      AND fld_revision_id={2:d}".format(_dic_index_xref[_key],
                                                        _key, revision_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

        return False

    def add_failure_modes(self, hardware_id):
        """
        Method to add default failure modes to the selected component.

        :param int hardware_id: the component Hardware ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _category_id = self.dicHardware[hardware_id].category_id
        _subcategory_id = self.dicHardware[hardware_id].subcategory_id

        # Retrieve the default failure modes for the component from the common
        # database.
        _modes = Configuration.RTK_FAILURE_MODES[_category_id][_subcategory_id]

        # Add the default failure modes to the open RTK Program database.
        _base_query = "INSERT INTO rtk_modes \
                       (fld_hardware_id, fld_mode_id\
                        fld_description, fld_mode_ratio) \
                       VALUES ({0:d}, {1:d}, '{2:s}', {3:f})"
        for __, _mode in enumerate(_modes):
            _query = _base_query.format(hardware_id, _mode[0], _mode[1],
                                        _mode[2])
            (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _return

    def save_hardware_item(self, hardware_id):
        """
        Method to save the Assembly or Component attributes to the RTK Project
        database.

        :param int hardware_id: the ID of the hardware to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """
        # TODO: Consider refactoring save_hardware_item; current McCabe Complexity index = 11.
        _hardware = self.dicHardware[hardware_id]

        # Save the base attributes.
        _query = "UPDATE rtk_hardware \
                  SET fld_alt_part_number='{0:s}', fld_attachments='{1:s}', \
                      fld_cage_code='{2:s}', fld_comp_ref_des='{3:s}', \
                      fld_cost={4:f}, fld_cost_failure={5:f}, \
                      fld_cost_hour={6:f}, fld_description='{7:s}', \
                      fld_duty_cycle={8:f}, fld_environment_active={9:d}, \
                      fld_environment_dormant={10:d}, \
                      fld_figure_number='{11:s}', fld_humidity={12:f}, \
                      fld_lcn='{13:s}', fld_level={14:d}, \
                      fld_manufacturer={15:d}, fld_mission_time={16:f}, \
                      fld_name='{17:s}', fld_nsn='{18:s}', \
                      fld_overstress={19:d}, fld_page_number='{20:s}', \
                      fld_parent_id={21:d}, fld_part={22:d}, \
                      fld_part_number='{23:s}', fld_quantity={24:d}, \
                      fld_ref_des='{25:s}', fld_reliability_goal={26:f}, \
                      fld_reliability_goal_measure={27:d}, \
                      fld_remarks='{28:s}', fld_rpm={29:f}, \
                      fld_specification_number='{30:s}', \
                      fld_tagged_part={31:d}, fld_temperature_active={32:f}, \
                      fld_temperature_dormant={33:f}, fld_vibration={34:f}, \
                      fld_year_of_manufacture={35:d}".format(
                          _hardware.alt_part_number, _hardware.attachments,
                          _hardware.cage_code, _hardware.comp_ref_des,
                          _hardware.cost, _hardware.cost_failure,
                          _hardware.cost_hour, _hardware.description,
                          _hardware.duty_cycle, _hardware.environment_active,
                          _hardware.environment_dormant,
                          _hardware.figure_number, _hardware.humidity,
                          _hardware.lcn, _hardware.level,
                          _hardware.manufacturer, _hardware.mission_time,
                          _hardware.name, _hardware.nsn, _hardware.overstress,
                          _hardware.page_number, _hardware.parent_id,
                          _hardware.part, _hardware.part_number,
                          _hardware.quantity, _hardware.ref_des,
                          _hardware.reliability_goal,
                          _hardware.reliability_goal_measure,
                          _hardware.remarks, _hardware.rpm,
                          _hardware.specification_number,
                          _hardware.tagged_part, _hardware.temperature_active,
                          _hardware.temperature_dormant, _hardware.vibration,
                          _hardware.year_of_manufacture)

        if _hardware.part == 0:
            _query = _query + ", fld_cost_type={0:d}, fld_repairable={1:d}, \
                               fld_total_part_quantity={2:d}, \
                               fld_total_power_dissipation={3:f}".format(
                                   _hardware.cost_type, _hardware.repairable,
                                   _hardware.total_part_quantity,
                                   _hardware.total_power_dissipation)
        elif _hardware.part == 1:
            _query = _query + ", fld_category_id={0:d}, \
                               fld_subcategory_id={1:d}".format(
                                   _hardware.category_id,
                                   _hardware.subcategory_id)

        _query = _query + " WHERE fld_revision_id={0:d} \
                            AND fld_hardware_id={1:d}".format(
                                _hardware.revision_id, hardware_id)

        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        # Save the stress attributes.
        _query = "UPDATE rtk_stress \
                  SET fld_current_ratio={0:f}, \
                      fld_max_rated_temperature={1:f}, \
                      fld_min_rated_temperature={2:f}, \
                      fld_operating_current={3:f}, fld_operating_power={4:f}, \
                      fld_operating_voltage={5:f}, fld_power_ratio={6:f}, \
                      fld_rated_current={7:f}, fld_rated_power={8:f}, \
                      fld_rated_voltage={9:f}, fld_temperature_rise={10:f}, \
                      fld_voltage_ratio={11:f}".format(
                          _hardware.current_ratio,
                          _hardware.max_rated_temperature,
                          _hardware.min_rated_temperature,
                          _hardware.operating_current,
                          _hardware.operating_power,
                          _hardware.operating_voltage, _hardware.power_ratio,
                          _hardware.rated_current, _hardware.rated_power,
                          _hardware.rated_voltage, _hardware.temperature_rise,
                          _hardware.voltage_ratio)

        if _hardware.part == 1:
            _query = _query + ", fld_junction_temperature={0:f}, \
                               fld_knee_temperature={1:f}, \
                               fld_thermal_resistance={2:f}, \
                               fld_tref={3:f}".format(
                                   _hardware.junction_temperature,
                                   _hardware.knee_temperature,
                                   _hardware.thermal_resistance,
                                   _hardware.reference_temperature)

        _query = _query + " WHERE fld_hardware_id={0:d}".format(hardware_id)

        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        # Save the reliability attributes.
        # If the hardware item is a part, create a list of float, integer, and
        # string values to hold the reliability inputs/results.
        _float = []
        _int = []
        _str = []
        if _hardware.part == 1:
            _rel_io = _hardware.get_attributes()[92:]
            _float = [x for x in _rel_io if isinstance(x, float)]
            _int = [x for x in _rel_io if isinstance(x, int)]
            _str = [x for x in _rel_io if isinstance(x, str)]
        _float += [0.0] * (20 - len(_float))
        _int += [0] * (10 - len(_int))
        _str += [''] * (5 - len(_str))
        _query = "UPDATE rtk_reliability \
                  SET fld_add_adj_factor={1:f}, \
                      fld_availability_logistics={2:f}, \
                      fld_availability_mission={3:f}, \
                      fld_avail_log_variance={4:f}, \
                      fld_avail_mis_variance={5:f}, fld_failure_dist={6:d}, \
                      fld_failure_parameter_1={7:f}, \
                      fld_failure_parameter_2={8:f}, \
                      fld_failure_parameter_3={9:f}, \
                      fld_hazard_rate_active={10:g}, \
                      fld_hazard_rate_dormant={11:g}, \
                      fld_hazard_rate_logistics={12:g}, \
                      fld_hazard_rate_method={13:g}, \
                      fld_hazard_rate_mission={14:g}, \
                      fld_hazard_rate_model='{15:s}', \
                      fld_hazard_rate_percent={16:f}, \
                      fld_hazard_rate_software={17:g}, \
                      fld_hazard_rate_specified={18:g}, \
                      fld_hazard_rate_type={19:d}, \
                      fld_hr_active_variance={20:g}, \
                      fld_hr_dormant_variance={21:g}, \
                      fld_hr_logistics_variance={22:g}, \
                      fld_hr_mission_variance={23:g}, \
                      fld_hr_specified_variance={24:g}, \
                      fld_mtbf_logistics={25:f}, fld_mtbf_mission={26:f}, \
                      fld_mtbf_specified={27:f}, \
                      fld_mtbf_log_variance={28:f}, \
                      fld_mtbf_miss_variance={29:f}, \
                      fld_mtbf_spec_variance={30:f}, \
                      fld_mult_adj_factor={31:f}, \
                      fld_reliability_logistics={32:f}, \
                      fld_reliability_mission={33:f}, \
                      fld_rel_log_variance={34:f}, \
                      fld_rel_miss_variance={35:f}, \
                      fld_survival_analysis={36:d}, \
                      fld_float1={37:g}, fld_float2={38:g}, \
                      fld_float3={39:g}, fld_float4={40:g}, \
                      fld_float5={41:g}, fld_float6={42:g}, \
                      fld_float7={43:g}, fld_float8={44:g}, \
                      fld_float9={45:g}, fld_float10={46:g}, \
                      fld_float11={47:g}, fld_float12={48:g}, \
                      fld_float13={49:g}, fld_float14={50:g}, \
                      fld_float15={51:g}, fld_float16={52:g}, \
                      fld_float17={53:g}, fld_float18={54:g}, \
                      fld_float19={55:g}, fld_float20={56:g}, \
                      fld_int1={57:d}, fld_int2={58:d}, fld_int3={59:d}, \
                      fld_int4={60:d}, fld_int5={61:d}, fld_int6={62:d}, \
                      fld_int7={63:d}, fld_int8={64:d}, fld_int9={65:d}, \
                      fld_int10={66:d}, fld_varchar1='{67:s}', \
                      fld_varchar2='{68:s}', fld_varchar3='{69:s}', \
                      fld_varchar4='{70:s}', fld_varchar5='{71:s}' \
                  WHERE fld_hardware_id={0:d}".format(
                      hardware_id, _hardware.add_adj_factor,
                      _hardware.availability_logistics,
                      _hardware.availability_mission,
                      _hardware.avail_log_variance,
                      _hardware.avail_mis_variance, _hardware.failure_dist,
                      _hardware.failure_parameter_1,
                      _hardware.failure_parameter_2,
                      _hardware.failure_parameter_3,
                      _hardware.hazard_rate_active,
                      _hardware.hazard_rate_dormant,
                      _hardware.hazard_rate_logistics,
                      _hardware.hazard_rate_method,
                      _hardware.hazard_rate_mission,
                      '',
                      _hardware.hazard_rate_percent,
                      _hardware.hazard_rate_software,
                      _hardware.hazard_rate_specified,
                      _hardware.hazard_rate_type,
                      _hardware.hr_active_variance,
                      _hardware.hr_dormant_variance,
                      _hardware.hr_logistics_variance,
                      _hardware.hr_mission_variance,
                      _hardware.hr_specified_variance,
                      _hardware.mtbf_logistics, _hardware.mtbf_mission,
                      _hardware.mtbf_specified, _hardware.mtbf_log_variance,
                      _hardware.mtbf_miss_variance,
                      _hardware.mtbf_spec_variance,
                      _hardware.mult_adj_factor,
                      _hardware.reliability_logistics,
                      _hardware.reliability_mission,
                      _hardware.rel_log_variance,
                      _hardware.rel_miss_variance, _hardware.survival_analysis,
                      _float[0], _float[1], _float[2], _float[3], _float[4],
                      _float[5], _float[6], _float[7], _float[8], _float[9],
                      _float[10], _float[11], _float[12], _float[13],
                      _float[14], _float[15], _float[16], _float[17],
                      _float[18], _float[19], _int[0], _int[1], _int[2],
                      _int[3], _int[4], _int[5], _int[6], _int[7], _int[8],
                      _int[9], _str[0], _str[1], _str[2], _str[3], _str[4])
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return (_results, _error_code)

    def save_bom(self):
        """
        Method to save all Assembly and Component data models managed by the
        controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _hardware in self.dicHardware.values():
            (_results,
             _error_code) = self.save_hardware_item(_hardware.hardware_id)

        return False

    def request_calculate(self, hardware_id=0):
        """
        Method to request the Hardware BoM calculations be performed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.dicHardware[hardware_id].calculate(self.dicHardware[hardware_id])

        return False
