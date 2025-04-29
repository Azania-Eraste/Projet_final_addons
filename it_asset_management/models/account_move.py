from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    contract_id = fields.Many2one('it.contract', string='Contrat', help="Contrat lié à la facture")

