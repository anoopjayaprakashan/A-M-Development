# -*- coding: utf-8 -*-
###################################################################################

# Author       :  A & M
# Copyright(c) :  2024-Present.
# License      :  LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

###################################################################################

import base64
import csv
import io
import re
import xlsxwriter
import xlsxwriter.utility
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class PsqlQueryExecute(models.Model):
    _name = 'psql.query.execute'
    _description = 'PostgresSQL Query Execute'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "query_name"

    PROHIBITED_WORDS = [
        'delete',
        'drop',
        'insert',
        'alter',
        'truncate',
        'execute',
        'create',
        'update'
    ]

    query_name = fields.Char(string='Identifier', help="Identifier", tracking=True)
    execute_query = fields.Text(string='Query', help="Query to Execute", tracking=True)
    query_result = fields.Html(string='Output', help="Output of the Execute Query")
    query_state = fields.Selection([('draft', 'New'), ('done', 'Verified')], string='Query Status', default='draft', tracking=True)
    modified_uid = fields.Many2one('res.users', string='Modified By')
    data_available = fields.Boolean(string='Data Available', default=False)

    def action_execute_query(self):
        try:
            for record in self:
                if record.execute_query:
                    query = record.execute_query.lower()
                    for word in self.PROHIBITED_WORDS:
                        expr = r'\b%s\b' % word
                        is_not_safe = re.search(expr, query)
                        if is_not_safe:
                            raise ValidationError(_("The query is not allowed...! Because it contains unsafe keyword '%s'") % (word.upper()))
                    self._cr.execute(record.execute_query)
                    table_header = ""
                    for key in [key[0] for key in self._cr.description]:
                        table_header += ("<th style='border:1px solid black !important'> %s </th>" % key)
                    table_datas = ""
                    query_data = self._cr.fetchall()
                    if query_data:
                        for query_res in query_data:
                            table_datas += "<tr>"
                            for rec in query_res:
                                table_datas += ("<td style='border:1px solid black !important'>{0}</td>".format(rec))
                            table_datas += "</tr>"
                        record.query_result = """ <div style="overflow:auto;"> 
                                                  <table class="table text-center table-border table-sm" style="width: max-content;">
                                                  <thead> <tr style='border:1px solid black !important;background: #d3d3d3;'> """ + str(table_header) + """</tr> </thead>
                                                  <tbody> """ + str(table_datas) + """</tbody> 
                                                  </table></div> """
                        record.data_available = True
                    else:
                        record.query_result = """ No data available at the time of execution..! """
                        record.data_available = False
                record.modified_uid = record.env.user.id
                record.query_state = 'done'
        except Exception as error:
            raise ValidationError(_(f"Query Execution Error :\n{error}"))

    def action_back_to_draft(self):
        for record in self:
            record.modified_uid = record.env.user.id
            record.query_result = ""
            record.query_state = 'draft'
            record.data_available = False

    def action_csv_download(self):
        fp = io.StringIO()
        writer = csv.writer(fp)
        for record in self:
            if record.execute_query:
                self._cr.execute(record.execute_query)
                headers = [col.name for col in self._cr.description]
                writer.writerow(headers)
                rows = self._cr.fetchall()
                for row in rows:
                    writer.writerow(row)
        file_data = fp.getvalue()
        fp.close()
        file_base64 = base64.b64encode(file_data.encode('utf-8'))
        attachment = self.env['ir.attachment'].create({
            'name': 'PostgresSQL Report.csv',
            'type': 'binary',
            'datas': file_base64,
            'store_fname': 'PostgresSQL Report.csv',
            'mimetype': 'text/csv',
        })
        url = f'/web/content/{attachment.id}?download=true'
        message = f"{self.env.user.partner_id.name} downloaded a CSV file containing information from database using the following query: '{self.execute_query}'."
        self.sudo().message_post(
            body=message,
            attachment_ids=[attachment.id],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    def action_xlsx_download(self):
        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        table_heading_no_format = workbook.add_format({
            'align': 'right',
            'valign': 'vleft',
            'bold': True,
            'size': 12,
            'bg_color': '#d3d3d3',
            'border': None
        })
        worksheet = workbook.add_worksheet('PostgresSQL Report.xlsx')
        for record in self:
            if record.execute_query:
                self._cr.execute(record.execute_query)
                col_index = 0
                for col_data in self._cr.description:
                    col_name = col_data.name
                    worksheet.set_column(col_index, col_index, 20)
                    worksheet.write(0, col_index, col_name, table_heading_no_format)
                    col_index += 1

                row_index = 1
                for row_data in self._cr.fetchall():
                    col_index = 0
                    for col_data in row_data:
                        if isinstance(col_data, (int, float)):
                            worksheet.write(row_index, col_index, col_data)
                        else:
                            worksheet.write(row_index, col_index, str(col_data))
                        col_index += 1
                    row_index += 1

        workbook.close()
        file_data = fp.getvalue()
        file_base64 = base64.b64encode(file_data)
        attachment = self.env['ir.attachment'].create({
            'name': 'PostgresSQL Report.xlsx',
            'type': 'binary',
            'datas': file_base64,
            'store_fname': 'PostgresSQL Report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        url = f'/web/content/{attachment.id}?download=true'
        message = f"{self.env.user.partner_id.name} downloaded a EXCEL file containing information from database using the following query: '{self.execute_query}'."
        self.sudo().message_post(
            body=message,
            attachment_ids=[attachment.id],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
