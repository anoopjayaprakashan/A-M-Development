# -*- coding: utf-8 -*-
###################################################################################

# Author       :  A & M
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

{
    "name": "PostgreSQL Execute",
    "summary": """ Module to execute postgresql query """,
    "category": "Extra Tools",
    "version": "17.0.1.0.0",
    "author": "A & M",
    "license": "LGPL-3",
    "depends": ['base', 'mail'],
    "data": ['security/ir.model.access.csv',
             'views/psql_query_views.xml'],
    "images": ['static/description/banner.gif'],
    "installable": True,
    "application": False,
    "auto_install": False,
}
