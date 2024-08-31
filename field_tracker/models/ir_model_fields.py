# -*- coding: utf-8 -*-
###################################################################################

# Author       :  A & M
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

from odoo import api, fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    custom_tracking = fields.Boolean(compute="_compute_custom_tracking", store=True, readonly=False)
    trackable = fields.Boolean(compute="_compute_trackable", defualt=False)

    @api.depends("tracking")
    def _compute_custom_tracking(self):
        for record in self:
            record.custom_tracking = record.tracking

    @api.depends("related", "store", "ttype")
    def _compute_trackable(self):
        keyword_blacklists = [
            "id",
            "write_date",
            "write_id",
            "create_date",
            "create_id",
            "activity_ids",
            "message_ids",
            "message_last_post",
            "message_main_attachment",
            "message_main_attachment_id",
        ]
        field_blacklists = [
            "binary",
            "json",
            "many2many",
            "one2many",
            "many2one_reference",
            "reference",
            "properties",
            "properties_definition",
        ]

        for rec in self:
            rec.trackable = rec.name not in keyword_blacklists and rec.store and not rec.related
            rec.trackable = rec.ttype not in field_blacklists and rec.store and not rec.related

    def write(self, vals):
        custom_tracking = None
        if "custom_tracking" in vals:
            self.env.registry.clear_cache()
            self.check_access_rights("write")
            custom_tracking = vals.pop("custom_tracking")
            self._write({"custom_tracking": custom_tracking})
            self.invalidate_model(fnames=["custom_tracking"])
        return super().write(vals)
