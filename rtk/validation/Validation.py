#!/usr/bin/env python
"""
##############################
Validation Package Data Module
##############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.validation.Validation.py is part of The RTK Project
#
# All rights reserved.


# Import other RTK modules.
try:
    from analyses.statistics.Bounds import calculate_beta_bounds
except ImportError:                         # pragma: no cover
    from rtk.analyses.statistics.Bounds import calculate_beta_bounds

def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:       # Type error
        _error_code = 10                                            # pragma: no cover
    elif 'invalid literal for int() with base 10' in message[0]:    # Value error
        _error_code = 10
    elif 'index out of range' in message[0]:                        # Index error
        _error_code = 40
    else:                                                           # Unhandled error
        _error_code = 1000                                          # pragma: no cover

    return _error_code


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Validation data model contains the attributes and methods for a
    verification and validation task. The attributes of a Validation model
    are:

    :ivar revision_id: default value: 0
    :ivar validation_id: default value: 0
    :ivar task_description: default value: ''
    :ivar task_type: default value: ''
    :ivar task_specification: default value: ''
    :ivar measurement_unit: default value: 0
    :ivar min_acceptable: default value: 0.0
    :ivar mean_acceptable: default value: 0.0
    :ivar max_acceptable: default value: 0.0
    :ivar variance_acceptable: default value: 0.0
    :ivar start_date: default value: 719163
    :ivar end_date: default value: 719163
    :ivar status: default value: 0.0
    :ivar minimum_time: default value: 0.0
    :ivar average_time: default value: 0.0
    :ivar maximum_time: default value: 0.0
    :ivar mean_time: default value: 0.0
    :ivar time_variance: default value: 0.0
    :ivar minimum_cost: default value: 0.0
    :ivar average_cost: default value: 0.0
    :ivar maximum_cost: default value: 0.0
    :ivar mean_cost: default value: 0.0
    :ivar cost_variance: default value: 0.0
    :ivar confidence: default value: 95.0
    """

    def __init__(self):
        """
        Method to initialize a Validation data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.revision_id = 0
        self.validation_id = 0
        self.task_description = ''
        self.task_type = 0
        self.task_specification = ''
        self.measurement_unit = 0
        self.min_acceptable = 0.0
        self.mean_acceptable = 0.0
        self.max_acceptable = 0.0
        self.variance_acceptable = 0.0
        self.start_date = 719163
        self.end_date = 719163
        self.status = 0.0
        self.minimum_time = 0.0
        self.average_time = 0.0
        self.maximum_time = 0.0
        self.mean_time = 0.0
        self.time_variance = 0.0
        self.minimum_cost = 0.0
        self.average_cost = 0.0
        self.maximum_cost = 0.0
        self.mean_cost = 0.0
        self.cost_variance = 0.0
        self.confidence = 95.0

    def set_attributes(self, values):
        """
        Method to set the Validation data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.validation_id = int(values[1])
            self.task_description = str(values[2])
            self.task_type = int(values[3])
            self.task_specification = str(values[4])
            self.measurement_unit = int(values[5])
            self.min_acceptable = float(values[6])
            self.mean_acceptable = float(values[7])
            self.max_acceptable = float(values[8])
            self.variance_acceptable = float(values[9])
            self.start_date = int(values[10])
            self.end_date = int(values[11])
            self.status = float(values[12])
            self.minimum_time = float(values[13])
            self.average_time = float(values[14])
            self.maximum_time = float(values[15])
            self.mean_time = float(values[16])
            self.time_variance = float(values[17])
            self.minimum_cost = float(values[18])
            self.average_cost = float(values[19])
            self.maximum_cost = float(values[20])
            self.mean_cost = float(values[21])
            self.cost_variance = float(values[22])
            self.confidence = float(values[23])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Verificaiton data model attributes.

        :return: (revision_id, validation_id, task_description, task_type,
                  task_specification, measurement_unit, min_acceptable,
                  mean_acceptable, max_acceptable, variance_acceptable,
                  start_date, end_date, status, minimum_time, average_time,
                  maximum_time, mean_time, time_variance, minimum_cost,
                  average_cost, maximum_cost, mean_cost, cost_variance,
                  confidence)
        :rtype: tuple
        """

        _values = (self.revision_id, self.validation_id, self.task_description,
                   self.task_type, self.task_specification,
                   self.measurement_unit, self.min_acceptable,
                   self.mean_acceptable, self.max_acceptable,
                   self.variance_acceptable, self.start_date, self.end_date,
                   self.status, self.minimum_time, self.average_time,
                   self.maximum_time, self.mean_time, self.time_variance,
                   self.minimum_cost, self.average_cost, self.maximum_cost,
                   self.mean_cost, self.cost_variance, self.confidence)

        return _values

    def calculate(self):
        """
        Method to calculate the expected task time, lower limit, and upper
        limit on task time.

        :return:
        :rtype:
        """

        # Calculate mean task time assuming a beta distribution.
        (_meanll, _mean,
         _meanul, _sd) = calculate_beta_bounds(self.minimum_time,
                                               self.average_time,
                                               self.maximum_time,
                                               self.confidence)

        self.mean_time = _mean
        self.time_variance = _sd**2.0

        # Calculate mean task cost assuming a beta distribution.
        (_meanll, _mean,
         _meanul, _sd) = calculate_beta_bounds(self.minimum_cost,
                                               self.average_cost,
                                               self.maximum_cost,
                                               self.confidence)

        self.mean_cost = _mean
        self.cost_variance = _sd**2.0

        return False


class Validation(object):
    """
    The Validation data controller provides an interface between the Validation
    data model and an RTK view model.  A single Validation controller can
    manage one or more Validation data models.  The attributes of a
    Validation data controller are:

    :ivar :py:class:`rtk.dao.DAO` _dao: the Data Access Object to use when
                                        communicating with the RTK Project
                                        database.
    :ivar int _last_id: the last Validation ID used.
    :ivar dict dicTasks: Dictionary of the Validation data models managed.  Key
                         is the Validation ID; value is a pointer to the
                         Validation data model instance.
    :ivar dict dicStatus: Dictionary of the Validation task status updates
                          managed.  Key is the update date; value is a list of
                          remaining time and remaining cost.
    """

    def __init__(self):
        """
        Initializes a Validation data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicTasks = {}
        self.dicStatus = {}

    def request_tasks(self, dao, revision_id):
        """
        Method to read the RTK Project database and load all the Validation
        tasks associated with the selected Revision.  For each Validation task
        returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Validation data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Tasks being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the tasks for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_validation')[0]

        _query = "SELECT * FROM rtk_validation \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_tests = len(_results)
        except TypeError:
            _n_tests = 0

        for i in range(_n_tests):
            _task = Model()
            _task.set_attributes(_results[i])
            self.dicTasks[_task.validation_id] = _task

        return(_results, _error_code)

    def request_status(self, revision_id):
        """
        Method to read the RTK Project database and load the Validation task
        status updates associated with the selected Revision.  For each
        Validation task update returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Add the instance to the dictionary of Updates being managed
           by this controller.

        :param int revision_id: the Revision ID to select the updates for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self.dicStatus.clear()

        _query = "SELECT fld_update_date, fld_time_remaining, \
                         fld_cost_remaining \
                  FROM rtk_validation_status \
                  WHERE fld_revision_id={0:d} \
                  ORDER BY fld_update_date".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_updates = len(_results)
        except TypeError:
            _n_updates = 0

        for i in range(_n_updates):
            self.dicStatus[_results[i][0]] = _results[i][1]

        return(_results, _error_code)

    def add_task(self, revision_id):
        """
        Adds a new Validation activity to the RTK Program's database.

        :param int revision_id: the Revision ID to select the tasks for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        try:
            _task_name = "New V&V Activity " + str(self._last_id + 1)
        except TypeError:                   # No tasks exist.
            _task_name = "New V&V Activity 1"

        _query = "INSERT INTO rtk_validation \
                  (fld_revision_id, fld_task_desc) \
                  VALUES (%d, '%s')" % (revision_id, _task_name)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new test was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted task.
        #   2. Create a new Validation model instance.
        #   4. Set the attributes of the new Validation model instance.
        #   5. Add the new Validation model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_validation')[0]

            _task = Model()
            _task.set_attributes((self._last_id, _task_name, 0, '', 0, 0.0,
                                  0.0, 0.0, 0.0, 719163, 719163, 0.0, 0.0, 0.0,
                                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                  95.0))
            self.dicTasks[_task.validation_id] = _task

        return(_results, _error_code)

    def delete_task(self, validation_id):
        """
        Deletes the currently selected Validation task from the RTK Program's
        database.

        :param int validation_id: the ID of the Validation task to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_validation \
                  WHERE fld_validation_id=%d" % validation_id
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            self.dicTasks.pop(validation_id)

        return(_results, _error_code)

    def save_task(self, validation_id):
        """
        Method to save the Validation model information to the open RTK Program
        database.

        :param int validation_id: the ID of the Validation task to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _task = self.dicTasks[validation_id]

        _query = "UPDATE rtk_validation \
                  SET fld_task_desc='{1:s}', fld_task_type={2:d}, \
                      fld_task_specification='{3:s}', \
                      fld_measurement_unit={4:d}, fld_min_acceptable={5:f}, \
                      fld_mean_acceptable={6:f}, fld_max_acceptable={7:f}, \
                      fld_variance_acceptable={8:f}, fld_start_date={9:d}, \
                      fld_end_date={10:d}, fld_status={11:f}, \
                      fld_minimum_time={12:f}, fld_average_time={13:f}, \
                      fld_maximum_time={14:f}, fld_mean_time={15:f}, \
                      fld_time_variance={16:f}, fld_minimum_cost={17:f}, \
                      fld_average_cost={18:f}, fld_maximum_cost={19:f}, \
                      fld_mean_cost={20:f}, fld_cost_variance={21:f}, \
                      fld_confidence={22:f} \
                  WHERE fld_validation_id={0:d}".format(
                      _task.validation_id, _task.task_description,
                      _task.task_type, _task.task_specification,
                      _task.measurement_unit, _task.min_acceptable,
                      _task.mean_acceptable, _task.max_acceptable,
                      _task.variance_acceptable, _task.start_date,
                      _task.end_date, _task.status, _task.minimum_time,
                      _task.average_time, _task.maximum_time, _task.mean_time,
                      _task.time_variance, _task.minimum_cost,
                      _task.average_cost, _task.maximum_cost, _task.mean_cost,
                      _task.cost_variance, _task.confidence)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_tasks(self):
        """
        Saves all Validation data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _task in self.dicTasks.values():
            (_results, _error_code) = self.save_task(_task.validation_id)

        return False

    def save_status(self, revision_id):
        """
        Method to save the V & V task status updates.

        :param int revision_id: the ID of the Revision to save updates for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        for i in range(len(self.dicStatus.values())):
            _query = "UPDATE rtk_validation_status \
                      SET fld_time_remaining={0:f} \
                      WHERE fld_update_date={1:d} \
                      AND fld_revision_id={2:d}".format(
                          self.dicStatus[self.dicStatus.keys()[i]],
                          self.dicStatus.keys()[i], revision_id)
            (_results,
             _error_code, __) = self._dao.execute(_query, commit=True)

            if _results:
                _query = "INSERT INTO rtk_validation_status \
                                      (fld_time_remaining, fld_update_date, \
                                       fld_revision_id) \
                          VALUES({0:f}, {1:d}, {2:d})".format(
                              self.dicStatus[self.dicStatus.keys()[i]],
                              self.dicStatus.keys()[i], revision_id)
                (_results,
                 _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
