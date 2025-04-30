from odoo import models, fields, api


class intervention(models.Model):
    _name = 'it.intervention'
    _description = 'Intervention'


    name = fields.Char("Numero")
    description = fields.Text()
    incident_id = fields.Many2one('it.incident', 'incident')
    image = fields.Binary('Image')