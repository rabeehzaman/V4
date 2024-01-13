from odoo import api, models


SKIPPEDTABLELIST = ['zadeleted.records', 'ir.attachment','ir.actions.act_window.view','mail.message','ir.ui.view',
                    'mail.followers','mail.mail', 'ir.model.data','bus.bus','ir.model.fields','ir.model','ir.model.contraint','ir.model.access']


class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'

    def unlink(self):
        zadeleted_recs = self.env['zadeleted.records']
        if self and not self._transient and self._name not in SKIPPEDTABLELIST:
            model_name = self._name
            model_rec = self.env['ir.model'].sudo().search(
                [('model', '=', model_name)])
            for rec in self:
                deleted_rec = zadeleted_recs.sudo().create(
                    {
                     'model_name':model_name,
                     'record_id':rec.id,
                     'model_id': model_rec.id
                    })
        return super(BaseModelExtend, self).unlink()
