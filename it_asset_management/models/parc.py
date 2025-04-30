from odoo import models, fields, api

class ItParcInformatique(models.Model):
    _name = 'it.parc.informatique'
    _description = 'Parc Informatique'

    name = fields.Char(string="Nom du Parc", required=True)
    equipment_ids = fields.One2many('it.equipment', 'parc_id', string="Équipements")
    client_id = fields.Many2one('res.partner', string="Client")