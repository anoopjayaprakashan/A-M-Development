# -*- coding: utf-8 -*-
###################################################################################

# Author       :  A & M
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

{
    "name"         : "Package Installer",
    "summary"      : """ Module to install python packages """,
    "description"  : """ Module to install python packages """,
    "category"     : "Extra Tools",
    "version"      : "17.0.1.0.0",
    "author"       : "Anoop",
    "maintainer"   : "Anoop",
    "license"      : "LGPL-3",
    "depends"      : ['base', 'mail'],
    "data"         : ['security/ir.model.access.csv',
                      'wizard/pip_installer.xml'],
    "assets"       : {'web.assets_backend': ['pip_installer/static/src/js/pip_installer.js',
                                             'pip_installer/static/src/xml/pip_installer.xml']},

    "images"       : ['static/description/banner.gif'],
    "installable"  : True,
    "application"  : False,
    "auto_install" : False,
}
