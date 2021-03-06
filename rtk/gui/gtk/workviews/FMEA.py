# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.FMEA.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""FMEA Work View."""

from datetime import datetime
from sortedcontainers import SortedDict  # pylint: disable=E0401
from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from gui.gtk.assistants import AddControlAction  # pylint: disable=E0401
from .WorkView import RTKWorkView


class FMEA(RTKWorkView):
    """
    Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional FMEA attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | tvw_fmea `cursor_changed`                 |
    +----------+-------------------------------------------+
    |      1   | tvw_fmea `button_press_event`             |
    +----------+-------------------------------------------+
    |      2   | tvw_fmea `edited`                         |
    +----------+-------------------------------------------+
    """

    _lst_control_type = [_(u"Prevention"), _(u"Detection")]

    def __init__(self, controller):
        """
        Initialize the Work View for the FMEA.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='FMEA')

        # Initialize private dictionary attributes.
        self._dic_icons['mode'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/mode.png'
        self._dic_icons['mechanism'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/mechanism.png'
        self._dic_icons['cause'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/cause.png'
        self._dic_icons['control'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/control.png'
        self._dic_icons['action'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/action.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None
        self._dtc_fmea = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _bg_color = '#FFFFFF'
        _fg_color = '#000000'
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['ffmeca']
        _fmt_path = "/root/tree[@name='FFMECA']/column"
        _tooltip = _(u"Displays the Functional Failure Mode and Effects "
                     u"Analysis (FMEA) for the currently selected Function.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            _bg_color,
            _fg_color,
            pixbuf=True,
            indexed=True)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        # Load the severity classes into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(7)
        for _item in controller.RTK_CONFIGURATION.RTK_SEVERITY:
            _severity = controller.RTK_CONFIGURATION.RTK_SEVERITY[_item][1]
            _model.append((_severity, ))

        # Load the users into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(8)
        for _item in controller.RTK_CONFIGURATION.RTK_USERS:
            _user = controller.RTK_CONFIGURATION.RTK_USERS[_item][0] + ', ' + \
                controller.RTK_CONFIGURATION.RTK_USERS[_item][1]
            _model.append((_user, ))

        # Load the status values into the gtk.CellRendererCombo()
        _model = self._do_get_cell_model(10)
        for _item in controller.RTK_CONFIGURATION.RTK_ACTION_STATUS:
            _severity = \
                controller.RTK_CONFIGURATION.RTK_ACTION_STATUS[_item][0]
            _model.append((_severity, ))

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        for _column in self.treeview.get_columns():
            for _cell in _column.get_cell_renderers():
                try:
                    _cell.connect('edited', self._do_edit_cell)
                except TypeError:
                    print "FIXME: Handle TypeError in " \
                          "gui.gtk.workviews.FMEA.__init__()"

        _label = rtk.RTKLabel(
            _(u"FMEA"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Failure Mode and "
                      u"Effects Analysis (FMEA) for the "
                      u"selected function."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        self.pack_end(self._make_treeview(), True, True)
        self.show_all()

        pub.subscribe(self._on_select_function, 'selectedFunction')

    def _do_change_row(self, treeview):
        """
        Handle events for the FMEA Tree View RTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the FMEA RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeViewRTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
            _level = _node_id.count('.')
            _control = _node_id.split('.')[_level][0] == '0'
        except TypeError:
            _node_id = None
            _level = 0
            _control = False

        if _level == 1:
            _headings = [
                _(u"Mode ID"),
                _(u"Failure Mode"),
                _(u"Local Effect"),
                _(u"Next Effect"),
                _(u"End Effect"),
                _(u"Design Provisions"),
                _(u"Operator Actions"),
                _(u"Severity Classification"), '', '', '', '', '', '', '', '',
                _(u"Remarks")
            ]
        elif _level == 2 and _control:
            _headings = [
                _(u"Control ID"),
                _(u"Control"), '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', ''
            ]
        elif _level == 2 and not _control:
            _headings = [
                _(u"Action ID"),
                _(u"Recommended Action"), '', '', '', '', '', '',
                _(u"Action Owner"),
                _(u"Action  Due Date"),
                _(u"Action Status"),
                _(u"Action Taken"),
                _(u"Approved"),
                _(u"Approval Date"),
                _(u"Closed"),
                _(u"Closure Date"), ''
            ]
        else:
            _headings = []

        _columns = self.treeview.get_columns()

        i = 0
        for _heading in _headings:
            _label = rtk.RTKLabel(
                _heading, justify=gtk.JUSTIFY_CENTER, wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            if _heading == '':
                _columns[i].set_visible(False)
            else:
                _columns[i].set_visible(True)

            i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, __new_text):
        """
        Handle edits of the FMEA Work View RTKTreeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`.
        :param str path: the path that was edited.
        :param str __new_text: the edited text.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.treeview.get_model()
        try:
            _node_id = _model[path][18]
            _entity = self._dtc_fmea.request_select(_node_id)
            if _entity.is_mode:
                _entity.description = _model[path][1]
                _entity.effect_local = _model[path][2]
                _entity.effect_next = _model[path][3]
                _entity.effect_end = _model[path][4]
                _entity.design_provisions = _model[path][5]
                _entity.operator_actions = _model[path][6]
                _entity.severity_class = _model[path][7]
                _entity.remarks = _model[path][16]
            elif _entity.is_control:
                _entity.description = _model[path][1]
            elif _entity.is_action:
                _entity.action_recommended = _model[path][1]
                _entity.action_owner = _model[path][8]
                _entity.action_due_date = datetime.strptime(
                    _model[path][9], '%Y-%m-%d')
                _entity.action_status = _model[path][10]
                _entity.action_taken = _model[path][11]
                _entity.action_approved = _model[path][12]
                _entity.action_approve_date = datetime.strptime(
                    _model[path][13], '%Y-%m-%d')
                _entity.action_closed = _model[path][14]
                _entity.action_close_date = datetime.strptime(
                    _model[path][15], '%Y-%m-%d')
        except TypeError:
            _return = True
        except AttributeError:
            _return = True

        return _return

    def _do_get_cell_model(self, column):
        """
        Retrieve the gtk.CellRendererCombo() gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cell_renderers()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _do_load_tree(self, tree, row=None):
        """
        Iterate through the tree and load the FMEA RTKTreeView().

        :param tree: the treelib Tree() holding the (partial) FMEA to load.
        :param row: the parent gtk.Iter() of the entity being added to the
                    FMEA RTKTreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _data = []
        _model = self.treeview.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data
        _node_id = _node.identifier

        try:
            if _entity.is_mode:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mode'], 22, 22)
                _data = [
                    _entity.mode_id, _entity.description, _entity.effect_local,
                    _entity.effect_next, _entity.effect_end,
                    _entity.design_provisions, _entity.operator_actions,
                    _entity.severity_class, '', '', '', '', 0, '', 0, '',
                    _entity.remarks, _icon, _node_id
                ]
                _row = None
            elif _entity.is_mechanism:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mechanism'], 22, 22)
                _data = [
                    _entity.mechanism_id, _entity.description,
                    _entity.effect_local, _entity.effect_next,
                    _entity.effect_end, _entity.design_provisions,
                    _entity.operator_actions, _entity.severity_class,
                    _entity.remarks, _icon
                ]
            elif _entity.is_cause:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['cause'], 22, 22)
                _data = [
                    _entity.cause_id, _entity.description,
                    _entity.effect_local, _entity.effect_next,
                    _entity.effect_end, _entity.design_provisions,
                    _entity.operator_actions, _entity.severity_class,
                    _entity.remarks, _icon
                ]
            elif _entity.is_control and row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['control'], 22, 22)
                _data = [
                    _entity.control_id, _entity.description, '', '', '', '',
                    '', '', '', '', '', '', 0, '', 0, '', '', _icon, _node_id
                ]
            elif _entity.is_action and row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['action'], 22, 22)
                _data = [
                    _entity.action_id, _entity.action_recommended, '', '', '',
                    '', '', '', _entity.action_owner, _entity.action_due_date,
                    _entity.action_status, _entity.action_taken,
                    _entity.action_approved, _entity.action_approve_date,
                    _entity.action_closed, _entity.action_close_date, '',
                    _icon, _node_id
                ]

            try:
                _row = _model.append(row, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.workviews.FMEA.FMEA._do_load_tree."
            except ValueError:
                print "FIXME: Handle ValueError in " \
                      "gtk.gui.workviews.FMEA.FMEA._do_load_tree."

        except AttributeError:
            print "FIXME: Handle AttributeError in " \
                  "gtk.gui.workviews.FMEA.FMEA._do_load_tree."
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, _row)

        return None

    def _do_request_calculate(self, __button):
        """
        Calculate the FMEA RPN or criticality.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        # FIXME: Add code to _do_request_calculate() when refactoring the Hardware module.
        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 18)

        # Delete the selected entity from the RTK Program database and then
        # refresh the TreeView.
        if not self._dtc_fmea.request_delete(_node_id):
            self._on_select_function(self._function_id)
        else:
            _return = True

        return _return

    def _do_request_insert(self, __button, sibling=True):
        """
        Request to insert a new entity to the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :param bool sibling: indicator variable that determines whether a
                             sibling entity be added (default) or a child
                             entity be added to the currently selected entity.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _choose = False

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
            _level = _node_id.count('.')
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _level = 1
            _prow = None

        if sibling:
            if _level == 1:
                _entity_id = self._function_id
                _parent_id = _node_id
                _level = 'mode'
            else:
                _entity_id = _model.get_value(_prow, 0)
                _parent_id = _model.get_value(_prow, 18)
                _choose = True

        elif not sibling:
            if _level == 1:
                _entity_id = _model.get_value(_row, 0)
                _parent_id = _node_id
                _choose = True

            elif _level == 2:
                _prompt = _(u"A FMEA control or an action cannot have a "
                            u"child entity.")
                _dialog = rtk.RTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error')

                if _dialog.do_run() == gtk.RESPONSE_OK:
                    _dialog.do_destroy()

                _return = True

        if _choose:
            _dialog = AddControlAction()
            _response = _dialog.do_run()

            if _dialog.do_run() == gtk.RESPONSE_OK:
                _control = _dialog.rdoControl.get_active()
                _action = _dialog.rdoAction.get_active()

                if _control:
                    _level = 'control'
                elif _action:
                    _level = 'action'

            else:
                _return = True

            _dialog.do_destroy()

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if (not _return and not self._dtc_fmea.request_insert(
                _entity_id, _parent_id, _level)):
            self._on_select_function(self._function_id)
        else:
            _return = True

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_fmea.request_update_all()

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the FMEA class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the FMEA Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new FMEA entity at the same level as the "
              u"currently selected entity."),
            _(u"Add a new FMEA entity one level below the currently "
              u"selected entity."),
            _(u"Remove the selected entity from the FMEA."),
            _(u"Calculate the FMEA."),
            _(u"Save the FMEA to the open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_insert, self._do_request_insert,
            self._do_request_delete, self._do_request_calculate,
            self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'calculate', 'save'
        ]

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_treeview(self):
        """
        Make the FMEA RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(label=_(u"Failure Mode and Effects Analysis "
                                      u"(FMEA)"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the FMEA Work View RTKTreeView().

        :param treeview: the FMEA TreeView RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`gtk.gdk.Event`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to insert sibling, insert child, delete " \
                  "(selected), save (selected), and save all in " \
                  "rtk.gui.gtk.moduleviews.FMEA._on_button_press()."

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_select_function(self, module_id):
        """
        Respond to selectedFunction signal from pypubsub.

        :param int function_id: the ID of the Function that was selected.
        :return: None
        :rtype: None
        """
        self._function_id = module_id

        _model = self.treeview.get_model()
        _model.clear()

        self._dtc_fmea = self._mdcRTK.dic_controllers['ffmea']

        _fmea = self._dtc_fmea.request_select_all(self._function_id, functional=True)
        self._do_load_tree(_fmea)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return None
