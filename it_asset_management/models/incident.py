from odoo import models, fields

class ITIncident(models.Model):
    _name = 'it.incident'
    _description = 'Incident informatique'
    _inherit = ['helpdesk.ticket']

    equipment_id = fields.Many2one('it.equipment', string="Équipement concerné")
    client_id = fields.Many2one('res.partner', string="Client", related='equipment_id.client_id')
    site_id = fields.Many2one('res.partner', string="Site", related='equipment_id.site_id')
    technician_id = fields.Many2one('hr.employee', string="Technicien assigné")