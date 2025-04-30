# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Client(models.Model):
    _inherit = 'res.partner'

    est_un_client = fields.Boolean(string="Est un client", default=False, help="Indique si le partenaire est un client")
    equipment_ids = fields.One2many('it.equipment', 'client_id', string="Équipements")


    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        if self.env.context.get('est_un_client'):
            for partner in partners:
                partner.est_un_client = True
        return partners