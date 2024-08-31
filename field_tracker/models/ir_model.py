# -*- coding: utf-8 -*-
###################################################################################

# Author       :  A & M
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

from odoo import api, fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    tracked_field_count = fields.Integer(compute="_compute_tracked_field_count")

    @api.depends("field_id.custom_tracking")
    def _compute_tracked_field_count(self):
        for rec in self:
            rec.tracked_field_count = len(rec.field_id.filtered("custom_tracking"))
