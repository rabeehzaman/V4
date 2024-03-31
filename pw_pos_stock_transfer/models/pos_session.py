# -*- coding: utf-8 -*-
from odoo import models, fields, _


class PosSession(models.Model):
    _inherit = 'pos.session'

    transfer_count = fields.Integer('Transfers', compute='_compute_transfer_count')

    def _compute_transfer_count(self):
        for session in self:
            session.transfer_count = self.env['stock.picking'].search_count([('pw_pos_session_id', '=', session.id)])

    def action_open_transfers(self):
        return {
            'name': _('Transfers'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('pw_pos_session_id', '=', self.id)],
        }
