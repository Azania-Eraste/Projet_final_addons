from odoo import models, fields, api

class ITEquipmentRequest(models.Model):
    _name = 'it.equipment.request'
    _description = 'Demande d\'assistance pour équipement informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Titre", required=True, tracking=True)
    equipment_id = fields.Many2one(
        'it.equipment', 
        string="Équipement", 
        required=True, 
        ondelete='cascade', 
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner', 
        string="Client", 
        required=True, 
        default=lambda self: self.env.user.partner_id,
        tracking=True
    )
    description = fields.Text(string="Description", required=True, tracking=True)
    priority = fields.Selection([
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique')
    ], string="Priorité", default='medium', required=True, tracking=True)
    state = fields.Selection([
        ('new', 'Nouveau'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('cancelled', 'Annulé')
    ], string="État", default='new', tracking=True)
    create_date = fields.Datetime(string="Date de création", readonly=True, default=fields.Datetime.now)
    attachment_ids = fields.Many2many(
        'ir.attachment', 
        string="Pièces jointes", 
        readonly=True
    )

    @api.model
    def create(self, vals):
        request = super(ITEquipmentRequest, self).create(vals)
        request.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=f"Nouvelle demande d'assistance: {request.name}",
            user_id=request.equipment_id.user_id.id or request.env.user.id
        )
        return request