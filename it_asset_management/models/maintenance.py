from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Maintenance(models.Model):
    _name = 'it.maintenance'
    _description = 'Maintenance des équipements'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom", required=True, help="Nom de l'opération de maintenance")
    equipment_id = fields.Many2one('it.equipment', string="Équipement", required=True, ondelete='cascade')
    start_date = fields.Date(string="Date de début", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Date de fin", required=True)
    state = fields.Selection([
        ('planned', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string="État", default='planned', tracking=True)
    description = fields.Text(string="Description")
    client_id = fields.Many2one('res.partner', string="Client", related='equipment_id.client_id')
    site_id = fields.Many2one('res.partner', string="Site", related='equipment_id.site_id')
    technician_id = fields.Many2one('hr.employee', string="Technicien assigné")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.name = f"Maintenance {self.equipment_id.name} - {fields.Date.today().strftime('%Y%m%d')}"