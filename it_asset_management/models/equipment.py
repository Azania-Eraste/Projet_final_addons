from odoo import models, fields, api
from datetime import datetime, timedelta

class ITEquipment(models.Model):
    _name = 'it.equipment'
    _description = 'Équipement informatique'

    name = fields.Char(string="Nom", required=True)
    type_id = fields.Many2one("it.equipment.type", string="Type", help="Définir le type d'équipement", ondelete='cascade', required=True)
    serial_number = fields.Char(string="Numéro de série")
    brand = fields.Char(string="Marque")
    model = fields.Char(string="Modèle")
    image = fields.Binary('Image')
    parc_id = fields.Many2one('it.parc.informatique', string="Parc Informatique", required=True)
    client_id = fields.Many2one('res.partner', string="Client", related='parc_id.client_id')
    warranty_end_date = fields.Date(string="Fin de garantie")
    site_id = fields.Many2one('res.partner', string="Site", domain="[('parent_id', '=', client_id)]")
    user_id = fields.Many2one('res.users', string="Utilisateur assigné")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('retired', 'Retiré')
    ], string="État", default='active')
    alert_triggered = fields.Boolean(string="Alerte déclenchée", default=False)

    @api.model
    def check_warranty_alerts(self):
        """Vérifie les équipements dont la garantie expire dans 30 jours."""
        today = datetime.today().date()
        threshold_date = today + timedelta(days=30)
        equipments = self.search([
            ('warranty_end_date', '<=', threshold_date),
            ('warranty_end_date', '>=', today),
            ('alert_triggered', '=', False)
        ])
        for equipment in equipments:
            self.env['mail.activity'].create({
                'res_id': equipment.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'it.equipment')]).id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': f"Alerte : Fin de garantie pour {equipment.name}",
                'date_deadline': equipment.warranty_end_date,
                'user_id': equipment.client_id.user_id.id or self.env.user.id
            })
            equipment.alert_triggered = True