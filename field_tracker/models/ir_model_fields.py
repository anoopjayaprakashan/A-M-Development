# -*- coding: utf-8 -*-
###################################################################################

# Author       :  Anoop
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

from odoo import api, fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    custom_tracker = fields.Boolean(compute="_compute_custom_tracker", store=True, readonly=False)
    trackable = fields.Boolean(compute="_compute_trackable", defualt=False, store=True)

    @api.depends("tracking")
    def _compute_custom_tracker(self):
        for record in self:
            record.custom_tracker = record.tracking

    @api.depends("related", "store", "ttype")
    def _compute_trackable(self):
        keyword_blacklists = [
            "id",
            "write_date",
            "active_lang_count",
            "activity_ids",
            "message_ids",
            "message_last_post",
            "message_main_attachment",
            "message_main_attachment_id",
            "__last_update",
            "write_date",
            "write_uid",
            "display_name",
            "create_date",
            "create_uid",
            "xml_id",
            "id",
            "sequence"
        ]

        field_blacklists = [
            "binary",
            "json",
            "html",
            "many2many",
            "one2many",
            "many2one_reference",
            "reference",
            "properties",
            "properties_definition",
        ]

        for rec in self:
            rec.trackable = rec.ttype not in field_blacklists and rec.store and not rec.related and rec.name not in keyword_blacklists

    def write(self, vals):
        if "custom_tracker" in vals:
            self.env.registry.clear_cache()
            self.check_access_rights("write")
            custom_tracker = vals.pop("custom_tracker")
            self._write({"custom_tracker": custom_tracker})
            self.invalidate_model(fnames=["custom_tracker"])
        return super().write(vals)
