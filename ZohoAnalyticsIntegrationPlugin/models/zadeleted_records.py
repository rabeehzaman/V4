from datetime import datetime, timedelta
from odoo import models, fields


class DeletedRecords(models.Model):
    _name = "zadeleted.records"
    _description = "Stores deleted records."
    
    model_id = fields.Many2one('ir.model', string="Model")
    model_name = fields.Char(string='Model Name')
    record_id = fields.Integer(string ='Record Id')

