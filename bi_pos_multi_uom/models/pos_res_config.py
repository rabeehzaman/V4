# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	pos_product_multi_uom = fields.Boolean(related='pos_config_id.product_multi_uom', readonly=False)

