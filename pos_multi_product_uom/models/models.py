# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import fields, models, api, tools, _
from itertools import groupby
from odoo.tools import  float_round

import logging
_logger = logging.getLogger(__name__)

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    product_uom_id = fields.Many2one('uom.uom', string='Product UoM', related='uom_id')

    @api.depends('product_uom_id','uom_id')
    def compute_product_uom(self):
        for res in self:
            if res.uom_id:
                res.product_uom_id = res.uom_id
            else:
                res.product_uom_id = res.product_id.uom_id.id
            return fields_return

    def get_product_uom(self, product_id):
        product = self.env['product.product'].browse(product_id)
        return product.uom_id

    def _export_for_ui(self, orderline):
        result = super(PosOrderLine, self)._export_for_ui(orderline)
        result.update({'uom_id': orderline.uom_id.id})
        return result

class StockPicking(models.Model):
    _inherit='stock.picking'
    
    def _prepare_stock_move_vals(self, first_line, order_lines):
        res = super()._prepare_stock_move_vals(first_line, order_lines)
        res['product_uom'] = first_line.product_uom_id.id
        return res

    def _create_move_from_pos_order_lines(self, lines):
        self.ensure_one()

        # start custom code: to prevent the grouping if orderline product have diffrent unit
        def _group_by_product_id(line):
            if line.uom_id.id != line.product_id.uom_id.id:
                return False
            return line.product_id.id

        lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key= lambda l: _group_by_product_id(l))
        
        #end custom code

        move_vals = []
        for dummy, olines in lines_by_product:
            order_lines = self.env['pos.order.line'].concat(*olines)
            move_vals.append(self._prepare_stock_move_vals(order_lines[0], order_lines))
        moves = self.env['stock.move'].create(move_vals)
        confirmed_moves = moves._action_confirm()
        confirmed_moves._add_mls_related_to_order(lines, are_qties_done=True)
        confirmed_moves.picked = True
        self._link_owner_on_return_picking(lines)