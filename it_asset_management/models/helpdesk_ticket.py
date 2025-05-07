from odoo import fields, models

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    equipment_id = fields.Many2one('it.equipment', string="Équipement")