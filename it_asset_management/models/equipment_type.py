from odoo import models, fields, api
from datetime import datetime, timedelta

class ITEquipment(models.Model):
    _name = 'it.equipment.type'
    _description = "Type d'équipement informatique"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text()
    equipments_ids = fields.One2many('it_asset_management.equipment', 'type_id', 'équipements')