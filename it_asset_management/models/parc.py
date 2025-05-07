from odoo import models, fields, api

class ItParcInformatique(models.Model):
    _name = 'it.parc.informatique'
    _description = 'Parc Informatique'

    name = fields.Char(string="Nom du Parc", required=True)
    equipment_ids = fields.One2many('it.equipment', 'parc_id', string="Équipements")
    client_id = fields.Many2one('res.partner', string="Client", domain=[('est_un_client', '=', True)])
    equipment_count = fields.Integer(string="Nombre d'équipements", compute='_compute_equipment_count')

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)

    def action_open_equipments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Équipements du Parc',
            'res_model': 'it.equipment',
            'view_mode': 'kanban,list,form',
            'domain': [('parc_id', '=', self.id)],
            'context': {'default_parc_id': self.id},
            'view_id': self.env.ref('it_asset_management.view_it_equipment_kanban').id,
        }