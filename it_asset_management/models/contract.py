from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ITContract(models.Model):
    _name = 'it.contract'
    _description = 'Contrat de service informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom du contrat", required=True)
    client_id = fields.Many2one('res.partner', string="Client", required=True, domain=[('est_un_client', '=', True)])
    start_date = fields.Date(string="Date de début", default=fields.Date.today)
    end_date = fields.Date(string="Date de fin")
    billing_frequency = fields.Selection([
        ('monthly', 'Mensuel'),
        ('quarterly', 'Trimestriel'),
        ('yearly', 'Annuel')
    ], string="Fréquence de facturation", default='monthly')
    amount = fields.Float(string="Montant", required=True)
    parc_id = fields.Many2one('it.parc.informatique', string="Parc Informatique", tracking=True)
    equipment_ids = fields.One2many('it.equipment', string="Équipements", related='parc_id.equipment_ids', readonly=False)
    invoice_ids = fields.One2many('account.move', 'contract_id', string="Factures")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('expired', 'Expiré')
    ], string="État", default='draft')
    ticket_answer_time = fields.Selection([
        ('1h', '1 heure'),
        ('4h', '4 heures'),
        ('8h', '8 heures'),
        ('1d', '1 jour'),
        ('2d', '2 jours'),
        ('1w', '1 semaine')
    ], string="Délai de réponse", required=True, default='4h')

    @api.depends('parc_id')
    def _check_parc_id(self):
        for record in self:
            if not record.parc_id:
                _logger.info("parc_id is unset for contract %s", record.name)
            elif not record.parc_id.equipment_ids:
                _logger.info("equipment_ids is empty for parc %s", record.parc_id.name)

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