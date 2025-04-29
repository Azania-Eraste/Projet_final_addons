from odoo import models, fields

class ITEquipmentType(models.Model):
    _name = 'it.equipment.type'
    _description = "Type d'équipement informatique"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text()
    equipments_ids = fields.One2many('it.equipment', 'type_id', string='Équipements')