#!/usr/bin/env python
""" This file contains configuration information and functions for
    RelKit.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       configuration.py is part of The RelKit Project
#
# All rights reserved.

import ConfigParser
from os import environ, path, mkdir, name

# Add localization support.
import locale
import gettext
_ = gettext.gettext

# Import other RelKit modules.
import utilities as _util
import widgets as _widg

#TODO: Create GUI to manipulate user configuration values.


grampus_times=[0.860, 1.258, 1.317, 1.442, 1.897, 2.011, 2.122, 2.439,
               3.203, 3.298, 3.902, 3.910, 4.000, 4.247, 4.411, 4.456,
               4.517, 4.899, 4.910, 5.676, 5.755, 6.137, 6.221, 6.311,
               6.613, 6.975, 7.335, 8.158, 8.498, 8.690, 9.042, 9.330,
               9.394, 9.426, 9.872, 10.191, 11.511, 11.575, 12.1, 12.126,
               12.368, 12.681, 12.795, 13.399, 13.668, 13.78, 13.877, 14.007,
               14.028, 14.035, 14.173, 14.173, 14.449, 14.587, 14.610, 15.07,
               16.0]

# Path to the directory containing icon files used by RelKit.  Defaults to
# /usr/share/pixmaps/reliafree/.
ICON_DIR = ''

# Path to the directory containing data files used by RelKit.  Defaults to
# /usr/share/reliafree/.
DATA_DIR = ''

# Path to the directory containing configuration files used by RelKit.
# Defaults to $HOME/.config/reliafree/ on POSIX systems.
CONF_DIR = ''

# Path to the directory containing log files used by RelKit.
# Defaults to $HOME/.config/reliafree/ on POSIX systems.
LOG_DIR = ''

# Global list containing the path to the format files to use for various
# widgets.
#
#    Position 00: Revision Tree formatting.
#    Position 01: Function Tree formatting.
#    Position 02: Requirements Tree formatting.
#    Position 03: Hardware Tree formatting.
#    Position 04: Validation Tree formatting.
#    Position 05: Reliability Growth Tree formatting.
#    Position 06: Field Incidents Tree formatting.
#    Position 07: Parts List formatting.
#    Position 08: Similar Item Analysis formatting.
#    Position 09: FMECA worksheet formatting.
#    Position 10: Failure Modes List formatting.
#    Position 11: ALT/ADT Planning List formatting.
#    Position 12: Failure Mechanisms List formatting.
#    Position 13: Reliability Growth Incident List formatting.
#    Position 14: Field Incident List formatting.
#    Position 15: Software Tree formatting.
#    Position 16: Dataset Tree formatting.
#    Position 17: Risk Analysis formatting.
RELIAFREE_FORMAT_FILE = []

# Global list containing the colors to use for various widgets.
#
#    Position 00: Revision row background color
#    Position 01: Revision row foreground color
#    Position 02: Function row background color
#    Position 03: Function row foreground color
#    Position 04: Requirement row background color
#    Position 05: Requirement row foreground color
#    Position 06: Assembly row background color
#    Position 07: Assembly row foreground color
#    Position 08: Validation row background color
#    Position 09: Validation row foreground color
#    Position 10: Reliability Growth row background color
#    Position 11: Reliability Growth row foreground color
#    Position 12: Program Incident row background color
#    Position 13: Program Incident row foreground color
#    Position 14: Part List row background color
#    Position 15: Part List row foreground color
#    Position 16: Overstressed Part row background color
#    Position 17: Overstressed Part row foreground color
#    Position 18: Tagged Part row background color
#    Position 19: Tagged Part row foreground color
#    Position 20: Part with no failure rate model row foreground color
RELIAFREE_COLORS = []

# Global variable list to house information about the prefix and next index
# to use when adding new revisions, functions, assemblies, parts,
# FMECA items, FMECA modes, FMECA effects, and FMECA causes.
#
#    Position 00: Revision prefix
#    Position 01: Next revision index
#    Position 02: Function prefix
#    Position 03: Next function index
#    Position 04: Assembly prefix
#    Position 05: Next assembly index
#    Position 06: Part prefix
#    Position 07: Next part index
#    Position 08: FMECA item prefix
#    Position 09: Next FMECA item index
#    Position 10: FMECA mode prefix
#    Position 11: Next FMECA mode index
#    Position 12: FMECA effect prefix
#    Position 13: NExt FMECA effect index
#    Position 14: FMECA cause prefix
#    Position 15: Next FMECA cause index
#    Position 16: Software prefix
#    Position 17: Next Software prefix
RELIAFREE_PREFIX = []

# Global list to house information about the active modules.
#    1 = active, 0 = inactive.
#
#    Position 00: Revision module status
#    Position 01: Requirements module status
#    Position 02: Function module status
#    Position 03: Hardware module status
#    Position 04: Software module status
#    Position 05: Validation module status
#    Position 06: Testing module status
#    Position 07: Maintenance Policy module status
#    Position 08: Field Incidents module status
#    Position 09: FMECA module status
#    Position 10: Survival Analysis module status
#    Position 11: RBD module status
#    Position 12: FTA module status
RELIAFREE_MODULES = []

# Global list for MySQL or SQLite3 connection information to the common
# database.
#
#    Position 00: Host name
#    Position 01: Host port
#    Position 02: Database name
#    Position 03: User name
#    Position 04: User password
RELIAFREE_COM_INFO = []

# Global list for MySQL or SQLite3 connection information to the Program
# database.
#
#    Position 00: Host name
#    Position 01: Host port
#    Position 02: Database name
#    Position 03: User name
#    Position 04: User password
RELIAFREE_PROG_INFO = []

# Variables to hold the backend database type for the program and common
# database.
BACKEND = ''
COM_BACKEND = ''

# Variables to support native language support.
LOCALE = 'en_US'

# Variables to control the display of numerical information.
FRMULT = 1.0
PLACES = 6
MTIME = 100.0

# Variables to control GUI options.
TABPOS = ['top', 'bottom', 'bottom']


class RelKitConf:
    """ The RelKit configuration class. """

    def __init__(self, level='site'):
        """
        Initializes the RelKit configuration parser.

        Keyword Arguments:
        level -- indicates which configuration file is to be read.
                 One of 'site' or 'user'.
        """

        if(name == 'posix'):
            self.OS = 'Linux'
            _SITEDIR = '/etc/reliafree/'
            _DATADIR = '/usr/share/reliafree/'
            _ICONDIR = '/usr/share/pixmaps/reliafree/'
            _LOGDIR = '/var/log/reliafree/'
            _HOMEDIR = environ['HOME']

        elif(name == 'nt'):
            self.OS = 'Windows'
            _HOMEDIR = environ['USERPROFILE']
            _DATADIR = _HOMEDIR + '/.config/reliafree/'
            _SITEDIR = _HOMEDIR + '/.config/reliafree/'
            _ICONDIR = _HOMEDIR + '/.config/reliafree/icons/'
            _LOGDIR = _HOMEDIR + '/.config/reliafree/logs/'

        if(level == 'site'):
            if(_util.dir_exists(_SITEDIR)):
                self.conf_dir = _SITEDIR
            else:
                self.conf_dir = _HOMEDIR + '/.config/reliafree/'

            if(_util.dir_exists(_DATADIR)):
                self.data_dir = _DATADIR
            else:
                self.data_dir = _HOMEDIR + '/.config/reliafree/data/'

            if(_util.dir_exists(_ICONDIR)):
                self.icon_dir = _ICONDIR
            else:
                self.icon_dir = _HOMEDIR + '/.config/reliafree/icons'

            if(_util.dir_exists(_LOGDIR)):
                self.log_dir = _LOGDIR
            else:
                self.log_dir = _HOMEDIR + '/.config/reliafree/logs/'

            self._conf_file = self.conf_dir + '/site.conf'

        elif(level == 'user'):
            self.conf_dir = _HOMEDIR + '/.config/reliafree/'

            if(_util.dir_exists(_DATADIR)):
                self.data_dir = _DATADIR
            else:
                self.data_dir = _HOMEDIR + '/.config/reliafree/data/'

            if(_util.dir_exists(_ICONDIR)):
                self.icon_dir = _ICONDIR
            else:
                self.icon_dir = _HOMEDIR + '/.config/reliafree/icons'

            if(_util.dir_exists(_LOGDIR)):
                self.log_dir = _LOGDIR
            else:
                self.log_dir = _HOMEDIR + '/.config/reliafree/logs/'

            self._conf_file = self.conf_dir + 'reliafree.conf'

        if not _util.file_exists(self._conf_file):
            self.create_default_configuration()

    def create_default_configuration(self):
        """
        Creates a default configuration file in the user's
        configuration directory.
        """
        from os.path import basename

        if(_util.dir_exists(self.conf_dir)):

            config = ConfigParser.ConfigParser()

            if(basename(self._conf_file) == 'site.conf'):
                dialog = _widg.make_dialog("RelKit common database information...")

                fixed = _widg.make_fixed()

                y_pos = 10
                label = _widg.make_label("RelKit common database host name:",
                                         width=340)
                txtDBHost = _widg.make_entry()
                fixed.put(label, 5, y_pos)
                fixed.put(txtDBHost, 345, y_pos)
                y_pos += 30

                label = _widg.make_label("RelKit common database socket:",
                                         width=340)
                txtDBSocket = _widg.make_entry()
                txtDBSocket.set_text("3306")
                fixed.put(label, 5, y_pos)
                fixed.put(txtDBSocket, 345, y_pos)
                y_pos += 30

                label = _widg.make_label("RelKit common database name:",
                                         width=340)
                txtDBName = _widg.make_entry()
                txtDBName.set_text("reliafreecom")
                fixed.put(label, 5, y_pos)
                fixed.put(txtDBName, 345, y_pos)
                y_pos += 30

                label = _widg.make_label("RelKit common database user name:",
                                         width=340)
                txtDBUser = _widg.make_entry()
                txtDBUser.set_text("reliafreecom")
                fixed.put(label, 5, y_pos)
                fixed.put(txtDBUser, 345, y_pos)
                y_pos += 30

                label = _widg.make_label("RelKit common database password:",
                                         width=340)
                txtDBPassword = _widg.make_entry()
                txtDBPassword.set_invisible_char("*")
                txtDBPassword.set_visibility(False)
                txtDBPassword.set_text("reliafreecom")
                fixed.put(label, 5, y_pos)
                fixed.put(txtDBPassword, 345, y_pos)
                y_pos += 30

                label = _widg.make_label("RelKit common database type:",
                                         width=340)
                cmbDBType = _widg.make_combo()
                _widg.load_combo(cmbDBType, [["mysql"], ["sqlite3"]])
                fixed.put(label, 5, y_pos)
                fixed.put(cmbDBType, 345, y_pos)
                y_pos += 30

                fixed.show_all()
                dialog.vbox.pack_start(fixed)
                response = dialog.run()

                if(response == -3):
                    reliafreecomlist = []
                    reliafreecomlist.append(txtDBHost.get_text())
                    reliafreecomlist.append(int(txtDBSocket.get_text()))
                    reliafreecomlist.append(txtDBName.get_text())
                    reliafreecomlist.append(txtDBUser.get_text())
                    reliafreecomlist.append(txtDBPassword.get_text())
                    reliafreecomlist.append(cmbDBType.get_active_text())

                dialog.destroy()

                config.add_section('Modules')
                config.set('Modules', 'prediction', 'True')
                config.set('Modules', 'fmeca', 'True')
                config.set('Modules', 'maintainability', 'True')
                config.set('Modules', 'maintenance', 'True')
                config.set('Modules', 'fraca', 'True')
                config.add_section('Backend')
                config.set('Backend', 'host', reliafreecomlist[0])
                config.set('Backend', 'socket', reliafreecomlist[1])
                config.set('Backend', 'database', reliafreecomlist[2])
                config.set('Backend', 'user', reliafreecomlist[3])
                config.set('Backend', 'password', reliafreecomlist[4])
                config.set('Backend', 'type', reliafreecomlist[5])

            elif(basename(self._conf_file) == 'reliafree.conf'):
                config.add_section('General')
                config.set('General', 'reportsize', 'letter')
                config.set('General', 'repairtimeunit', 'hours')
                config.set('General', 'parallelcalcs', 'False')
                config.set('General', 'frmultiplier', 1000000.0)
                config.set('General', 'failtimeunit', 'hours')
                config.set('General', 'calcreltime', 100.0)
                config.set('General', 'autoaddlistitems', 'False')
                config.set('General', 'decimal', 6)
                config.set('General', 'treetabpos', 'top')
                config.set('General', 'listtabpos', 'bottom')
                config.set('General', 'booktabpos', 'bottom')

                config.add_section('Backend')
                config.set('Backend', 'type', 'mysql')
                config.set('Backend', 'host', 'localhost')
                config.set('Backend', 'socket', 3306)
                config.set('Backend', 'database', '')
                config.set('Backend', 'user', '')
                config.set('Backend', 'password', '')

                config.add_section('Directories')
                config.set('Directories', 'datadir', 'data')
                config.set('Directories', 'icondir', 'icons')
                config.set('Directories', 'logdir', 'log')

                config.add_section('Files')
                config.set('Files', 'revisionformat', 'revision_format.xml')
                config.set('Files', 'functionformat', 'function_format.xml')
                config.set('Files', 'requirementformat', 'requirement_format.xml')
                config.set('Files', 'hardwareformat', 'hardware_format.xml')
                config.set('Files', 'validationformat', 'validation_format.xml')
                config.set('Files', 'rgformat', 'rg_format.xml')
                config.set('Files', 'fracaformat', 'fraca_format.xml')
                config.set('Files', 'partformat', 'part_format.xml')
                config.set('Files', 'rgincidentformat', 'rgincident_format.xml')
                config.set('Files', 'incidentformat', 'incident_format.xml')
                config.set('Files', 'siaformat', 'sia_format.xml')
                config.set('Files', 'fmecaformat', 'fmeca_format.xml')
                config.set('Files', 'modeformat', 'mode_format.xml')
                config.set('Files', 'altformat', 'alt_format.xml')
                config.set('Files', 'mechanismformat', 'mechanism_format.xml')
                config.set('Files', 'softwareformat', 'software_format.xml')
                config.set('Files', 'datasetformat', 'dataset_format.xml')
                config.set('Files', 'riskformat', 'risk_format.xml')

                config.add_section('Colors')
                config.set('Colors', 'revisionbg', '#FFFFFF')
                config.set('Colors', 'revisionfg', '#000000')
                config.set('Colors', 'functionbg', '#FFFFFF')
                config.set('Colors', 'functionfg', '#0000FF')
                config.set('Colors', 'requirementbg', '#FFFFFF')
                config.set('Colors', 'requirementfg', '#000000')
                config.set('Colors', 'assemblybg', '#FFFFFF')
                config.set('Colors', 'assemblyfg', '#000000')
                config.set('Colors', 'validationbg', '#FFFFFF')
                config.set('Colors', 'validationfg', '#00FF00')
                config.set('Colors', 'rgbg', '#FFFFFF')
                config.set('Colors', 'rgfg', '#000000')
                config.set('Colors', 'fracabg', '#FFFFFF')
                config.set('Colors', 'fracafg', '#000000')
                config.set('Colors', 'partbg', '#FFFFFF')
                config.set('Colors', 'partfg', '#000000')
                config.set('Colors', 'overstressbg', '#FF0000')
                config.set('Colors', 'overstressfg', '#FFFFFF')
                config.set('Colors', 'taggedbg', '#00FF00')
                config.set('Colors', 'taggedfg', '#FFFFFF')
                config.set('Colors', 'nofrmodelfg', '#A52A2A')

            try:
                parser = open(self._conf_file, 'w')
                config.write(parser)
                parser.close()

                print _("RelKit default configuration created.")
                return True
            except EnvironmentError:
                print _("Could not save your RelKit configuration.")
                return False

        else:
            try:
                mkdir(self.conf_dir)
                print _("RelKit configuration directory (%s) created.") % \
                self.conf_dir
                mkdir(self.data_dir)
                print _("RelKit data directory (%s) created.") % \
                self.data_dir
                mkdir(self.log_dir)
                print _("RelKit log file directory (%s) created.") % \
                self.log_dir
                mkdir(self.icon_dir)
                print _("RelKit icon directory (%s) created.") % \
                self.icon_dir
                self.__init__()
            except EnvironmentError:
                print _("Could not create RelKit default configuration.")

    def write_configuration(self):
        """ Writes changes to the user's configuration file. """

        if _util.file_exists(self._conf_file):
            config = ConfigParser.ConfigParser()
            config.add_section('General')
            config.set('General', 'reportsize', 'letter')
            config.set('General', 'repairtimeunit', 'hours')
            config.set('General', 'parallelcalcs', 'False')
            config.set('General', 'frmultiplier', FRMULT)
            config.set('General', 'failtimeunit', 'hours')
            config.set('General', 'calcreltime', MTIME)
            config.set('General', 'autoaddlistitems', 'False')
            config.set('General', 'decimal', PLACES)
            config.set('General', 'treetabpos', TABPOS[0])
            config.set('General', 'listtabpos', TABPOS[1])
            config.set('General', 'booktabpos', TABPOS[2])

            config.add_section('Backend')
            config.set('Backend', 'type', BACKEND)
            config.set('Backend', 'host', RELIAFREE_PROG_INFO[0])
            config.set('Backend', 'socket', RELIAFREE_PROG_INFO[1])
            config.set('Backend', 'database', '')
            config.set('Backend', 'user', RELIAFREE_PROG_INFO[3])
            config.set('Backend', 'password', RELIAFREE_PROG_INFO[4])

            config.add_section('Directories')
            config.set('Directories', 'datadir', 'data')
            config.set('Directories', 'icondir', 'icons')
            config.set('Directories', 'logdir', 'log')

            # Position 00: Revision Tree formatting.
            # Position 01: Function Tree formatting.
            # Position 02: Requirements Tree formatting.
            # Position 03: Hardware Tree formatting.
            # Position 04: Validation Tree formatting.
            # Position 05: Reliability Growth Tree formatting.
            # Position 06: Field Incidents Tree formatting.
            # Position 07: Parts List formatting.
            # Position 08: Similar Item Analysis formatting.
            # Position 09: FMECA worksheet formatting.
            # Position 10: Failure Modes List formatting.
            # Position 11: Failure Effects List formatting.
            # Position 12: Failure Mechanisms List formatting.
            config.add_section('Files')
            config.set('Files', 'revisionformat', path.basename(RELIAFREE_FORMAT_FILE[0]))
            config.set('Files', 'functionformat', path.basename(RELIAFREE_FORMAT_FILE[1]))
            config.set('Files', 'requirementformat', path.basename(RELIAFREE_FORMAT_FILE[2]))
            config.set('Files', 'hardwareformat', path.basename(RELIAFREE_FORMAT_FILE[3]))
            config.set('Files', 'validationformat', path.basename(RELIAFREE_FORMAT_FILE[4]))
            config.set('Files', 'rgformat', path.basename(RELIAFREE_FORMAT_FILE[5]))
            config.set('Files', 'fracaformat', path.basename(RELIAFREE_FORMAT_FILE[6]))
            config.set('Files', 'partformat', path.basename(RELIAFREE_FORMAT_FILE[7]))
            config.set('Files', 'siaformat', path.basename(RELIAFREE_FORMAT_FILE[8]))
            config.set('Files', 'fmecaformat', path.basename(RELIAFREE_FORMAT_FILE[9]))
            config.set('Files', 'modeformat', path.basename(RELIAFREE_FORMAT_FILE[10]))
            config.set('Files', 'altformat', path.basename(RELIAFREE_FORMAT_FILE[11]))
            config.set('Files', 'mechanismformat', path.basename(RELIAFREE_FORMAT_FILE[12]))
            config.set('Files', 'rgincidentformat', path.basename(RELIAFREE_FORMAT_FILE[13]))
            config.set('Files', 'incidentformat', path.basename(RELIAFREE_FORMAT_FILE[14]))
            config.set('Files', 'softwareformat', path.basename(RELIAFREE_FORMAT_FILE[15]))
            config.set('Files', 'datasetformat', path.basename(RELIAFREE_FORMAT_FILE[16]))
            config.set('Files', 'riskformat', path.basename(RELIAFREE_FORMAT_FILE[17]))

            # Position 00: Revision row background color
            # Position 01: Revision row foreground color
            # Position 02: Function row background color
            # Position 03: Function row foreground color
            # Position 04: Requirement row background color
            # Position 05: Requirement row foreground color
            # Position 06: Assembly row background color
            # Position 07: Assembly row foreground color
            # Position 08: Validation row background color
            # Position 09: Validation row foreground color
            # Position 10: Reliability Growth row background color
            # Position 11: Reliability Growth row foreground color
            # Position 12: Field Incident row background color
            # Position 13: Field Incident row foreground color
            # Position 14: Part List row background color
            # Position 15: Part List row foreground color
            # Position 16: Overstressed Part row background color
            # Position 17: Overstressed Part row foreground color
            # Position 18: Tagged Part row background color
            # Position 19: Tagged Part row foreground color
            # Position 20: Part with no failure rate model row foreground color
            config.add_section('Colors')
            config.set('Colors', 'revisionbg', RELIAFREE_COLORS[0])
            config.set('Colors', 'revisionfg', RELIAFREE_COLORS[1])
            config.set('Colors', 'functionbg', RELIAFREE_COLORS[2])
            config.set('Colors', 'functionfg', RELIAFREE_COLORS[3])
            config.set('Colors', 'requirementbg', RELIAFREE_COLORS[4])
            config.set('Colors', 'requirementfg', RELIAFREE_COLORS[5])
            config.set('Colors', 'assemblybg', RELIAFREE_COLORS[6])
            config.set('Colors', 'assemblyfg', RELIAFREE_COLORS[7])
            config.set('Colors', 'validationbg', RELIAFREE_COLORS[8])
            config.set('Colors', 'validationfg', RELIAFREE_COLORS[9])
            config.set('Colors', 'rgbg', RELIAFREE_COLORS[10])
            config.set('Colors', 'rgfg', RELIAFREE_COLORS[11])
            config.set('Colors', 'fracabg', RELIAFREE_COLORS[12])
            config.set('Colors', 'fracafg', RELIAFREE_COLORS[13])
            config.set('Colors', 'partbg', RELIAFREE_COLORS[14])
            config.set('Colors', 'partfg', RELIAFREE_COLORS[15])
            config.set('Colors', 'overstressbg', RELIAFREE_COLORS[16])
            config.set('Colors', 'overstressfg', RELIAFREE_COLORS[17])
            config.set('Colors', 'taggedbg', RELIAFREE_COLORS[18])
            config.set('Colors', 'taggedfg', RELIAFREE_COLORS[19])
            config.set('Colors', 'nofrmodelfg', RELIAFREE_COLORS[20])

            try:
                parser = open(self._conf_file,'w')
                config.write(parser)
                parser.close()
            except EnvironmentError:
                print _("Could not save your RelKit configuration.")

    def read_configuration(self):
        """ Reads the user's configuration file. """

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        try:
            if _util.file_exists(self._conf_file):
                config = ConfigParser.ConfigParser()
                config.read(self._conf_file)
                return config
            else:
                self.create_default_configuration()
                self.read_configuration()
        except:
            print _("There is a problem with your configuration file. Please, remove %s.") % self._conf_file
