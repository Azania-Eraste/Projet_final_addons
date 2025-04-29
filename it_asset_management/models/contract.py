from odoo import models, fields, api

class ITContract(models.Model):
    _name = 'it.contract'
    _description = 'Contrat de service informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom du contrat", required=True)
    client_id = fields.Many2one('res.partner', string="Client", required=True)
    start_date = fields.Date(string="Date de début", default=fields.Date.today)
    end_date = fields.Date(string="Date de fin")
    billing_frequency = fields.Selection([
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('annuel', 'Annuel')
    ], string="Fréquence de facturation", default='monthly')
    equipment_ids = fields.Many2many('it.equipment', string="Équipements couverts")
    invoice_ids = fields.One2many('account.move', 'contract_id', string="Factures")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('expired', 'Expiré')
    ], string="État", default='draft')

    @api.model
    def generate_recurring_invoices(self):
        """Génère les factures récurrentes pour les contrats actifs."""
        today = fields.Date.today()
        contracts = self.search([('state', '=', 'active')])
        for contract in contracts:
            if contract.billing_frequency == 'monthly' and today.day == 1:
                self._create_invoice(contract)
            elif contract.billing_frequency == 'quarterly' and today.day == 1 and today.month in [1, 4, 7, 10]:
                self._create_invoice(contract)
            elif contract.billing_frequency == 'yearly' and today.day == 1 and today.month == 1:
                self._create_invoice(contract)

    def _create_invoice(self, contract):
        """Crée une facture pour le contrat."""
        invoice_vals = {
            'partner_id': contract.client_id.id,
            'move_type': 'out_invoice',
            'contract_id': contract.id,
            'invoice_line_ids': [(0, 0, {
                'name': f"Prestation pour {contract.name}",
                'quantity': 1,
                'price_unit': contract.amount
            })]
        }
        self.env['account.move'].create(invoice_vals)   