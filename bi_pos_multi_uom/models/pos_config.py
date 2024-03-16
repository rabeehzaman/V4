# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    product_multi_uom = fields.Boolean(string="Product Multi UOM")


class PosOrder(models.Model):
    _inherit = 'pos.order'

    uom = fields.Boolean(string="uom", related='config_id.product_multi_uom', readonly=True)


    def _prepare_invoice_line(self, order_line):
        name = order_line.product_id.get_product_multiline_description_sale()
        return {
            'product_id': order_line.product_id.id,
            'quantity': order_line.qty if self.amount_total >= 0 else -order_line.qty,
            'discount': order_line.discount,
            'price_unit': order_line.price_unit,
            'name': name,
            'tax_ids': [(6, 0, order_line.tax_ids_after_fiscal_position.ids)],
            'product_uom_id': order_line.uom_id.id,
        }


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    uom_id = fields.Many2one('uom.uom', string="Unit Of Measure")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            try:
                if vals.get('uom_id'):
                    vals['uom_id'] = vals.get('uom_id')[0]
            except Exception:
                vals['uom_id'] = vals.get('uom_id') or None
                pass
        res = super(PosOrderLine, self).create(vals_list)
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_uom_ids = fields.One2many('product.template.uom.line', 'product_uom_line_id', string="discard Lines")
    point_of_sale_uom = fields.Boolean(string="Point Of Sale UOM")



class ProductTemplateUomLine(models.Model):
    _name = 'product.template.uom.line'
    _description = "Point of Sale Product UOM"

    product_uom_line_id = fields.Many2one('product.template', string="Product UOM")
    unit_of_measure_id = fields.Many2one('uom.uom', string="Unit Of Measure")
    sale_price = fields.Float(string="Sale Price")
    custom_id=fields.Many2one(related="product_uom_line_id.uom_id.category_id",string="category select")
    


class POSSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.config_id.product_multi_uom:
            result.append('product.template.uom.line')
        return result

    def _loader_params_product_template_uom_line(self):
        return {'search_params': {'domain': [], 'fields': ['product_uom_line_id', 'unit_of_measure_id', 'sale_price']}}

    def _get_pos_ui_product_template_uom_line(self, params):
        return self.env['product.template.uom.line'].search_read(**params['search_params'])

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('product_uom_ids')
        result['search_params']['fields'].append('point_of_sale_uom')
        return result


class PosPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        return {
            'name': first_line.name,
            'product_uom': first_line.product_id.uom_id.id,
            'picking_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': first_line.product_id.id,
            'product_uom_qty': abs(sum(order_lines.mapped('qty'))),
            'state': 'draft',
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'company_id': self.company_id.id,
        }