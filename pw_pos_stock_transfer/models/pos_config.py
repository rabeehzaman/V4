# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pw_stock_location_id = fields.Many2one('stock.location', string="Shop Location", domain="[('usage', '=', 'internal'), ('company_id', '=', company_id)]")
    pw_enable_transfer = fields.Boolean('Stock Transfer')
    pw_is_done = fields.Boolean(string="Done State")

    @api.model
    def get_transfer_shop(self, config_id):
        return self.sudo().search_read([('id', '!=', config_id), ('pw_enable_transfer', '=', True)], ['name'])

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pw_stock_location_id = fields.Many2one(related='pos_config_id.pw_stock_location_id', readonly=False)
    pw_enable_transfer = fields.Boolean(related='pos_config_id.pw_enable_transfer', readonly=False)
    pw_is_done = fields.Boolean(related='pos_config_id.pw_is_done', readonly=False)
