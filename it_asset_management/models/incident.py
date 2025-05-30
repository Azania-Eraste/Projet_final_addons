# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ITIncident(models.Model):
    _name = 'it.incident'
    _inherit = 'helpdesk.ticket'
    _description = 'Incident informatique'

    name = fields.Char(string="Nom", required=True, help="Nom de l'incident")
    description = fields.Text(string="Description")
    equipment_id = fields.Many2one('it.equipment', string="Équipement concerné")
    client_id = fields.Many2one(
        'res.partner',
        string="Client",
        related='equipment_id.client_id',
        domain=[('est_un_client', '=', True)],
        store=True
    )
    site_id = fields.Many2one('res.partner', string="Site", related='equipment_id.site_id')
    technician_id = fields.Many2one('hr.employee', string="Technicien assigné")
    sla_ids = fields.Many2many(
        'helpdesk.sla',
        relation='it_incident_sla_rel',
        column1='incident_id',
        column2='sla_id',
        string='SLAs'
    )
    stage_id = fields.Many2one(
        'helpdesk.stage',
        string="Stage",
        default=lambda self: self.env['helpdesk.stage'].search([
            ('sequence', '=', 1),
            ('fold', '=', False),
            ('is_close', '=', False)
        ], limit=1),
        tracking=True
    )
    partner_open_ticket_count = fields.Integer(
        string="Open Tickets Count",
        compute='_compute_partner_open_ticket_count',
        store=False
    )
    partner_ticket_ids = fields.Many2many(
        'it.incident',
        string="Partner Tickets",
        compute='_compute_partner_ticket_count',
        store=False
    )
    partner_ticket_count = fields.Integer(
        string="Total Partner Tickets",
        compute='_compute_partner_ticket_count',
        store=False
    )

    @api.model
    def default_get(self, fields_list):
        """Surcharge de default_get pour gérer explicitement stage_id."""
        result = super(ITIncident, self).default_get(fields_list)
        if 'stage_id' in fields_list:
            stage = self.env['helpdesk.stage'].search([
                ('sequence', '=', 1),
                ('fold', '=', False),
                ('is_close', '=', False)
            ], limit=1)
            if stage:
                result['stage_id'] = stage.id
        return result

    @api.depends('partner_id', 'equipment_id', 'stage_id')
    def _compute_partner_open_ticket_count(self):
        for ticket in self:
            if not ticket.id or not ticket.stage_id:
                ticket.partner_open_ticket_count = 0
                continue
            partner_id = ticket.partner_id or (ticket.equipment_id.client_id if ticket.equipment_id else False)
            if partner_id:
                open_tickets = self.env['it.incident'].search_count([
                    ('partner_id', '=', partner_id.id),
                    ('stage_id.fold', '=', False),
                    ('id', '!=', ticket.id),
                ])
                ticket.partner_open_ticket_count = open_tickets
            else:
                ticket.partner_open_ticket_count = 0

    @api.depends('partner_id', 'equipment_id')
    def _compute_partner_ticket_count(self):
        for ticket in self:
            if not ticket.id:
                ticket.partner_ticket_ids = [(5,)]
                ticket.partner_ticket_count = 0
                continue
            partner_id = ticket.partner_id or (ticket.equipment_id.client_id if ticket.equipment_id else False)
            if partner_id:
                partner_tickets = self.env['it.incident'].search([
                    ('partner_id', '=', partner_id.id),
                    ('id', '!=', ticket.id),
                ])
                ticket.partner_ticket_ids = partner_tickets
                ticket.partner_ticket_count = len(partner_tickets)
            else:
                ticket.partner_ticket_ids = [(5,)]
                ticket.partner_ticket_count = 0

    @api.onchange('equipment_id')
    def _onchange_equipment(self):
        if self.equipment_id and self.equipment_id.client_id:
            if self.equipment_id.client_id != self.partner_id:
                self.partner_id = self.equipment_id.client_id
        elif not self.equipment_id:
            self.partner_id = False

    @api.model_create_multi
    def create(self, vals_list):
        # Créer les enregistrements
        tickets = super(ITIncident, self).create(vals_list)
        # Appliquer les SLA avec le contexte approprié
        tickets.with_context(active_model='helpdesk.ticket').sudo()._sla_apply()
        return tickets

    @api.model
    def _sla_find(self):
        _logger.info("Appel de _sla_find pour les enregistrements : %s, Modèle : %s", self, self._name)
        
        # Convertir les enregistrements it.incident en helpdesk.ticket
        helpdesk_tickets = self.env['helpdesk.ticket'].browse(self.ids) if self else self.env['helpdesk.ticket']
        
        # Appeler la méthode parente avec les enregistrements convertis
        result = super(ITIncident, helpdesk_tickets)._sla_find()
        
        _logger.info("Résultat de _sla_find : %s", result)
        return result