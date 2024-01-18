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
    product_uom_id = fields.Many2one('uom.uom', string='Product UoM', compute="compute_product_uom")
    uom_factor_qty = fields.Float(compute='_compute_uom_factor_qty', string="UoM Factor Qty",  store=True)
    secondary_uom_id = fields.Many2one('uom.uom', string='UoM')
    secondary_uom_qty = fields.Float(string='Qty')
    secondary_uom_with_qty = fields.Text(string='Secondary UoM Qty', compute="_compute_secondary_uom_with_qty", store=True)
    view = fields.Text(copy=False, string=' ')

    @api.onchange('product_uom_id')
    def compute_product_uom(self):
        for res in self:
            if res.uom_id:
                res.product_uom_id = res.uom_id
            else:
                res.product_uom_id = res.product_id.uom_id.id

    @api.depends('secondary_uom_id')
    def _compute_uom_factor_qty(self):
        for line in self:
            if line.uom_id and line.secondary_uom_id:
                line.uom_factor_qty = line.qty*line.secondary_uom_id.factor_inv
                # if line.product_uom_id.uom_type == 'bigger':
                #     line.uom_factor_qty = line.qty*line.product_uom_id.factor_inv

    @api.depends('secondary_uom_id', 'secondary_uom_qty')
    def _compute_secondary_uom_with_qty(self):
        for line in self:
            if line and line.secondary_uom_id and line.secondary_uom_id.name:
                line.secondary_uom_with_qty = str(
                    line.secondary_uom_qty) + ' ' + line.secondary_uom_id.name
            else:
                uom_id = self.get_product_uom(line.product_id.id)
                if uom_id and len(uom_id):
                    line.secondary_uom_with_qty = str(
                        line.qty) + ' ' + uom_id.name

    @api.model
    def _order_line_fields(self, line, session_id=None):
        fields_return = super(PosOrderLine, self)._order_line_fields(
            line, session_id=None)
        if line and line[2] and line[2].get('uom_id'):
            fields_return[2].update({'uom_id': line[2].get('uom_id', '')})
            fields_return[2].update(
                {'secondary_uom_id': line[2].get('uom_id', '')})
            uom_id = self.get_product_uom(line[2].get('product_id'))
            if uom_id:
                fields_return[2].update({'uom_id': uom_id.id})
                fields_return[2].update({'view': '/'+ uom_id.name})
            if fields_return[2].get('secondary_uom_id'):
                secondary_uom_id = self.env['uom.uom'].search(
                    [('id', '=', fields_return[2].get('secondary_uom_id'))], limit=1)
                if secondary_uom_id and uom_id:
                    factor_inv = secondary_uom_id.factor_inv/uom_id.factor_inv
                    fields_return[2].update(
                        {'secondary_uom_qty': fields_return[2].get('qty')})
                    fields_return[2].update({'qty':  float_round(fields_return[2].get(
                        'secondary_uom_qty')*factor_inv ,precision_rounding= uom_id.rounding)})
                    fields_return[2].update(
                        {'price_unit': (line[2].get('price_unit'))/factor_inv})

        else:
            uom_id = self.get_product_uom(line[2].get('product_id'))
            fields_return[2].update({'uom_id': uom_id})
            fields_return[2].update({'secondary_uom_id': uom_id})
            if fields_return[2].get('secondary_uom_id'):
                secondary_uom_id = self.env['uom.uom'].search(
                    [('id', '=', fields_return[2].get('secondary_uom_id'))], limit=1)
                if secondary_uom_id and uom_id:
                    factor_inv = secondary_uom_id.factor_inv/uom_id.factor_inv
                    fields_return[2].update(
                        {'secondary_uom_qty': fields_return[2].get('qty')})
                    fields_return[2].update({'qty':float_round(fields_return[2].get(
                        'secondary_uom_qty')*factor_inv ,uom_id.rounding)})
                    fields_return[2].update(
                        {'price_unit': (line[2].get('price_unit'))/factor_inv})

        return fields_return

    def get_product_uom(self, product_id):
        product = self.env['product.product'].browse(product_id)
        return product.uom_id


    def _export_for_ui(self, orderline):
        result = super(PosOrderLine, self)._export_for_ui(orderline)
        result.update({'uom_id': orderline.uom_id.id})
        if orderline.secondary_uom_id.id != orderline.uom_id.id:
            factor_inv = orderline.secondary_uom_id.factor_inv/orderline.uom_id.factor_inv
            result.update({'uom_id': orderline.secondary_uom_id.id or orderline.uom_id.id})
            result.update({'qty': orderline.secondary_uom_qty or orderline.qty})
            result.update({'price_unit': orderline.price_unit*factor_inv or orderline.price_unit})
            result.update({'refunded_qty': -sum(orderline.mapped('refund_orderline_ids.secondary_uom_qty')) or orderline.refunded_qty})  
        return result

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#     def _prepare_stock_move_vals(self, first_line, order_lines):
#         rs = super(StockPicking, self)._prepare_stock_move_vals(
#             first_line, order_lines)
#         if first_line.uom_id:
#             rs.update({'product_uom': first_line.uom_id.id})
#         return rs


#     def _create_move_from_pos_order_lines(self, lines):
#         self.ensure_one()
#         # lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
#         for line in lines:
#             order_lines = self.env['pos.order.line'].concat(*line)
#             first_line = order_lines[0]
#             current_move = self.env['stock.move'].create(
#                 self._prepare_stock_move_vals(first_line, order_lines)
#             )
#             if first_line.product_id.tracking != 'none' and (self.picking_type_id.use_existing_lots or self.picking_type_id.use_create_lots):
#                 for line in order_lines:
#                     sum_of_lots = 0
#                     for lot in line.pack_lot_ids.filtered(lambda l: l.lot_name):
#                         if line.product_id.tracking == 'serial':
#                             qty = 1
#                         else:
#                             qty = abs(line.qty)
#                         ml_vals = current_move._prepare_move_line_vals()
#                         ml_vals.update({'qty_done': qty})
#                         if self.picking_type_id.use_existing_lots:
#                             existing_lot = self.env['stock.production.lot'].search([
#                                 ('company_id', '=', self.company_id.id),
#                                 ('product_id', '=', line.product_id.id),
#                                 ('name', '=', lot.lot_name)
#                             ])
#                             if not existing_lot and self.picking_type_id.use_create_lots:
#                                 existing_lot = self.env['stock.production.lot'].create({
#                                     'company_id': self.company_id.id,
#                                     'product_id': line.product_id.id,
#                                     'name': lot.lot_name,
#                                 })
#                             ml_vals.update({
#                                 'lot_id': existing_lot.id,
#                             })
#                         else:
#                             ml_vals.update({
#                                 'lot_name': lot.lot_name,
#                             })
#                         self.env['stock.move.line'].create(ml_vals)
#                         sum_of_lots += qty
#                     if abs(line.qty) != sum_of_lots:
#                         difference_qty = abs(line.qty) - sum_of_lots
#                         ml_vals = current_move._prepare_move_line_vals()
#                         if line.product_id.tracking == 'serial':
#                             ml_vals.update({'qty_done': 1})
#                             for i in range(int(difference_qty)):
#                                 self.env['stock.move.line'].create(ml_vals)
#                         else:
#                             ml_vals.update({'qty_done': difference_qty})
#                             self.env['stock.move.line'].create(ml_vals)
#             else:
#                 current_move.product_packaging_quantity = abs(
#                     sum(order_lines.mapped('qty')))
#             confirmed_moves = current_move._action_confirm()
#             confirmed_moves._add_mls_related_to_order(lines, are_qties_done=True)
#             confirmed_moves.picked = True
#         self._link_owner_on_return_picking(lines)


class PosOrderReport(models.Model):
    _inherit = 'report.pos.order'
    product_qty = fields.Float(string='Product Quantity', readonly=True)
  
