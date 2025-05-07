from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Maintenance(models.Model):
    _name = 'it.maintenance'
    _description = 'Maintenance des équipements'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom", required=True, help="Nom de l'opération de maintenance")
    parc_id = fields.Many2one('it.parc.informatique', string="Parc Informatique", tracking=True)
    start_date = fields.Date(string="Date de début", required=True, default=fields.Date.today, tracking=True)
    end_date = fields.Date(string="Date de fin", required=True, tracking=True)
    state = fields.Selection([
        ('planned', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string="État", default='planned', tracking=True)
    description = fields.Text(string="Description")
    client_id = fields.Many2one('res.partner', string="Client", related='parc_id.client_id', domain=[('est_un_client', '=', True)])
    site_id = fields.Many2one('res.partner', string="Site")  # Non related, à remplir via onchange
    technician_id = fields.Many2one('hr.employee', string="Technicien assigné", tracking=True)
    equipment_ids = fields.Many2many('it.equipment', string="Équipements", domain="[('parc_id', '=', parc_id)]")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")

    @api.onchange('parc_id')
    def _onchange_parc_id(self):
        if self.parc_id:
            self.name = f"Maintenance {self.parc_id.name} - {fields.Date.today().strftime('%Y%m%d')}"
            if self.parc_id.equipment_ids:
                self.site_id = self.parc_id.equipment_ids[0].site_id

    @api.model
    def update_maintenance_state(self):
        """Update state to 'in_progress' for maintenance records where start_date is today and state is 'planned'."""
        today = date.today()
        maintenance_records = self.search([
            ('start_date', '=', today),
            ('state', '=', 'planned')
        ])
        for record in maintenance_records:
            record.state = 'in_progress'
            # Optional: Add a message to the chatter for tracking
            record.message_post(body=f"Maintenance automatically set to 'In Progress' on {today}.")