# -*- coding: utf-8 -*-
#
#       rtk.requirement.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Controller."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataController  # pylint: disable=E0401
from datamodels import RTKDataMatrix  # pylint: disable=E0401
# pylint: disable=E0401
from dao import RTKRequirement, RTKHardware, RTKSoftware, RTKValidation
from . import dtmRequirement


class RequirementDataController(RTKDataController):
    """
    Provide an interface between the Requirement data model and an RTK View.

    A single Requirement controller can manage one or more Requirement data
    models.  The attributes of a Requirement data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Requirement data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Requirement
                    Data Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmRequirement(dao),
            rtk_module='requirement',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_rqmt_hw_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                 RTKHardware)
        self._dmx_rqmt_sw_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                 RTKSoftware)
        self._dmx_rqmt_val_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                  RTKValidation)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Requirement module.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'rqrmnt_hrdwr':
            self._dmx_rqmt_hw_matrix.select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='hardware_id',
                rheader='requirement_code',
                cheader='comp_ref_des')
            _matrix = self._dmx_rqmt_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_hw_matrix.dic_row_hdrs

        elif matrix_type == 'rqrmnt_sftwr':
            self._dmx_rqmt_sw_matrix.select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='software_id',
                rheader='requirement_code',
                cheader='description')
            _matrix = self._dmx_rqmt_sw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_sw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_sw_matrix.dic_row_hdrs

        elif matrix_type == 'rqrmnt_vldtn':
            self._dmx_rqmt_val_matrix.select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='validation_id',
                rheader='requirement_code',
                cheader='description')
            _matrix = self._dmx_rqmt_val_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_val_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_val_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def request_insert(self, revision_id, parent_id):
        """
        Request to add an RTKRequirement table record.

        :param int revision_id: the ID of the Revision to add the new
                                Requirement to.
        :param int parent_id: the ID of the parent Requirement to add the new
                              Requirement to.
        :keyword bool sibling: indicates whether or not to insert a sibling
                               (default) or child (derived) Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id, parent_id=parent_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedRequirement',
                    requirement_id=self._dtm_data_model.last_id,
                    parent_id=parent_id)
        else:
            _msg = _msg + '  Failed to add a new Requirement to the RTK ' \
                'Program database.'

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_insert_matrix(self, matrix_type, item_id, heading, row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'rqrmnt_hrdwr':
            _error_code, _msg = self._dmx_rqmt_hw_matrix.insert(
                item_id, heading, row=row)
        elif matrix_type == 'rqrmnt_sftwr':
            _error_code, _msg = self._dmx_rqmt_sw_matrix.insert(
                item_id, heading, row=row)
        elif matrix_type == 'rqrmnt_vldtn':
            _error_code, _msg = self._dmx_rqmt_val_matrix.insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_type=matrix_type,
                item_id=item_id,
                row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, requirement_id):
        """
        Request to delete an RTKRequirement table record.

        :param int requirement_id: the Requirement ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.delete(requirement_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedRequirement')

    def request_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'rqrmnt_hrdwr':
            _error_code, _msg = self._dmx_rqmt_hw_matrix.delete(
                item_id, row=row)
        elif matrix_type == 'rqrmnt_sftwr':
            _error_code, _msg = self._dmx_rqmt_sw_matrix.delete(
                item_id, row=row)
        elif matrix_type == 'rqrmnt_vldtn':
            _error_code, _msg = self._dmx_rqmt_val_matrix.delete(
                item_id, row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedMatrix')

    def request_update(self, requirement_id):
        """
        Request to update an RTKRequirement table record.

        :param int requirement_id: the ID of the requirement to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update(requirement_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedRequirement')

    def request_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'rqrmnt_hrdwr':
            _error_code, _msg = self._dmx_rqmt_hw_matrix.update(
                revision_id, matrix_type)
        elif matrix_type == 'rqrmnt_sftwr':
            _error_code, _msg = self._dmx_rqmt_sw_matrix.update(
                revision_id, matrix_type)
        elif matrix_type == 'rqrmnt_vldtn':
            _error_code, _msg = self._dmx_rqmt_val_matrix.update(
                revision_id, matrix_type)
        else:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:s}.'.format(matrix_type)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedMatrix')

    def request_update_all(self):
        """
        Request to update all records in the RTKRequirement table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
