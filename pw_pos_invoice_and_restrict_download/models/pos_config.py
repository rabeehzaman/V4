# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pw_auto_invoice = fields.Boolean('Auto Invoicing')
    pw_stop_invoice_pdf = fields.Boolean('Restrict Invoice PDF Download')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pw_auto_invoice = fields.Boolean(related='pos_config_id.pw_auto_invoice', readonly=False)
    pw_stop_invoice_pdf = fields.Boolean(related='pos_config_id.pw_stop_invoice_pdf', readonly=False)
