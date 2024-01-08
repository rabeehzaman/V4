# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders, draft=False):
        res = super(PosOrder, self).create_from_ui(orders=orders, draft=draft)
        for order in res:
            if order.get('account_move'):
                order['invoice_number'] = self.env['account.move'].sudo().browse(order.get('account_move')).name
        return res
