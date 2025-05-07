from odoo import fields, models

class ITIncident(models.Model):
    _name = 'it.incident'
    _inherit = 'helpdesk.ticket'
    _description = 'Incident informatique'

    equipment_id = fields.Many2one('it.equipment', string="Équipement concerné")
    description = fields.Text()
    client_id = fields.Many2one('res.partner', string="Client", related='equipment_id.client_id', domain=[('est_un_client', '=', True)])
    site_id = fields.Many2one('res.partner', string="Site", related='equipment_id.site_id')
    technician_id = fields.Many2one('hr.employee', string="Technicien assigné")
    sla_ids = fields.Many2many(
        'helpdesk.sla',
        relation='it_incident_sla_rel',
        column1='incident_id',
        column2='sla_id',
        string='SLAs'
    )