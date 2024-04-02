# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
from odoo.tools import float_round


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pw_pos_session_id = fields.Many2one(
        string='POS Session',
        comodel_name='pos.session'
    )

    def _get_lot_id(self, lot_name, product_id):
        lot = self.env['stock.lot'].sudo().search([('name', '=', lot_name), ('product_id', '=', product_id.id)], limit=1)
        if not lot:
            lot = self.env['stock.lot'].sudo().create({
                'product_id': product_id.id,
                'company_id': self.env.user.company_id.id,
                'name': lot_name,
            })
        return lot

    @api.model
    def create_pos_internal_transfer(self, picking_data):
        transfer_state = picking_data.get('transfer_state')
        operation_type = picking_data.get('operation_type')
        dest_shop_id = self.env['pos.config'].sudo().browse(picking_data.get('dest_shop_id'))
        pos_session = self.env['pos.session'].browse(picking_data.get('session_id'))
        config_id = pos_session.config_id
        location_id = config_id.pw_stock_location_id
        location_dest_id = dest_shop_id.pw_stock_location_id
        if operation_type == 'receive':
            location_id = dest_shop_id.pw_stock_location_id
            location_dest_id = config_id.pw_stock_location_id
        warehouse_id = location_id.warehouse_id
        picking_type_id = self.env['stock.picking.type'].with_context(active_test=False).search([('code', '=', 'internal'), ('warehouse_id', '=', warehouse_id.id)], limit=1)
        partner_id = picking_data.get('partner_id')
        move_lines = []
        if picking_type_id and location_id and location_dest_id:
            if transfer_state == 'draft':
                for data in picking_data.get('lines'):
                    product = self.env['product.product'].sudo().browse(data.get('product_id'))
                    quantity = data.get('quantity', 0)
                    secondary_uom_id = self.env['uom.uom'].browse(data.get('uom_id'))
                    uom_id = product.uom_id
                    factor_inv = secondary_uom_id.factor_inv/uom_id.factor_inv
                    product_uom_qty = float_round(quantity*factor_inv, precision_rounding=uom_id.rounding)
                    if product and product.type != 'service' and quantity > 0:
                        move_lines.append((0, 0, {
                            'name': product.name,
                            'product_id': product.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'product_uom_qty': product_uom_qty,
                            # 'product_uom': product.uom_id.id,
                            'product_uom': uom_id.id,
                        }))
                picking = self.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'origin': pos_session.name,
                    'state': 'draft',
                    'pw_pos_session_id': pos_session.id,
                    'picking_type_id': picking_type_id.id,
                    'move_ids': move_lines,
                })
            if transfer_state == 'done':
                picking = self.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'origin': pos_session.name,
                    'state': 'draft',
                    'pw_pos_session_id': pos_session.id,
                    'picking_type_id': picking_type_id.id,
                })
                for data in picking_data.get('lines'):
                    move_line_ids = []
                    product = self.env['product.product'].browse(data.get('product_id'))
                    uom_id = data.get('uom_id')
                    quantity = data.get('quantity', 0)
                    pack_lot_lines = data.get('pack_lot_lines', [])
                    sr_data = []
                    uom_id = product.uom_id
                    secondary_uom_id = self.env['uom.uom'].browse(data.get('uom_id'))
                    factor_inv = secondary_uom_id.factor_inv/uom_id.factor_inv
                    product_uom_qty = float_round(quantity*factor_inv, precision_rounding=uom_id.rounding)
                    if pack_lot_lines:
                        for line in pack_lot_lines:
                            sr_data.append(line.get('lot_name'))
                    if product.tracking == 'serial':
                        move = self.env['stock.move'].create({
                            'name': product.name,
                            'product_id': product.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'product_uom_qty': product_uom_qty,
                            # 'product_uom': product.uom_id.id,
                            'product_uom': product.uom_id.id,
                            'picking_id': picking.id,
                        })
                        for serial in sr_data:
                            lot = self._get_lot_id(serial, product)
                            move_line = self.env['stock.move.line'].sudo().create({
                                'move_id': move.id,
                                'product_id': product.id,
                                'quantity': 1.0,
                                'lot_id': lot.id,
                                'product_uom_id': product.uom_id.id,
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id
                            })
                        move_lines.append(move.id)
                    elif product.tracking == 'lot':
                        move = self.env['stock.move'].create({
                            'name': product.name,
                            'product_id': product.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'product_uom_qty': product_uom_qty,
                            # 'product_uom': product.uom_id.id,
                            'product_uom': uom_id.id,
                            'picking_id': picking.id,
                        })
                        lot = self._get_lot_id(data[0], product)
                        move_line = self.env['stock.move.line'].sudo().create({
                            'move_id': move.id,
                            'product_id': product.id,
                            'quantity': product_uom_qty,
                            'lot_id': lot.id,
                            'product_uom_id': product.uom_id.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                        })
                        move_lines.append(move.id)
                    else:
                        move = self.env['stock.move'].create({
                            'name': product.name,
                            'product_id': product.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'quantity': product_uom_qty,
                            'is_inventory': True,
                            'product_uom_qty': product_uom_qty,
                            'product_uom': product.uom_id.id,
                            'picking_id': picking.id,
                        })
                        picking.action_confirm()
                
                picking.button_validate()
            return {'result': True, 'header': 'Transfer Created', 'body': 'Transfer Ref: '+picking.name}
        return {'result': False, 'header': 'Picking Data not found', 'body': ''}
