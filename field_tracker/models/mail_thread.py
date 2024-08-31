# -*- coding: utf-8 -*-
###################################################################################

# Author       :  Anoop
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

from odoo import models, tools


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @tools.ormcache("self.env.uid", "self.env.su")
    def _track_get_fields(self):
        model_alt_fields = []
        model_id = self.env['ir.model'].search([('model', '=', self._name)])
        if model_id:
            for name, field in self._fields.items():
                if self.env['ir.model.fields'].search([('name', '=', name), ('model_id.id', 'in', model_id.ids)]).custom_tracker:
                    model_alt_fields.append(name)
            model_fields = {name for name in model_alt_fields}
        else:
            model_fields = {name for name, field in self._fields.items() if getattr(field, 'tracking', None) or getattr(field, 'track_visibility', None)}
        return model_fields and set(self.fields_get(model_fields, attributes=()))
