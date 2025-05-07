from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ITIncident(models.Model):
    _name = 'it.incident'
    _inherit = 'helpdesk.ticket'
    _description = 'Incident informatique'

    equipment_id = fields.Many2one('it.equipment', string="Équipement concerné")
    description = fields.Text()
    client_id = fields.Many2one(
        'res.partner',
        string="Client",
        related='equipment_id.client_id',
        domain=[('est_un_client', '=', True)]
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
    # Ensure stage_id has a default
    stage_id = fields.Many2one(
        'helpdesk.stage',
        string='Stage',
        default=lambda self: self.env['helpdesk.stage'].search([('is_close', '=', False)], limit=1)
    )

    @api.depends('partner_id', 'equipment_id', 'stage_id')
    @api.depends('partner_id', 'equipment_id', 'stage_id')
    def _compute_partner_open_ticket_count(self):
        super()._compute_partner_open_ticket_count()  # Call parent method if needed
        for ticket in self:
            ticket.partner_open_ticket_count = 0
            if not ticket.id or not ticket.stage_id:
                _logger.info("Skipping partner_open_ticket_count for unsaved or invalid record: %s, stage_id: %s", 
                            ticket, ticket.stage_id)
                continue
            partner_id = ticket.partner_id
            if not partner_id and ticket.equipment_id and ticket.equipment_id.client_id:
                partner_id = ticket.equipment_id.client_id
            if partner_id:
                open_tickets = self.env['it.incident'].search_count([
                    ('partner_id', '=', partner_id.id),
                    ('stage_id.is_close', '=', False),
                    ('id', '!=', ticket.id),
                ])
                ticket.partner_open_ticket_count = open_tickets

    @api.depends('partner_id', 'equipment_id')
    def _compute_partner_ticket_count(self):
        for ticket in self:
            if not ticket.id:  # Skip unsaved records
                _logger.info("Skipping partner_ticket_ids for unsaved record: %s", ticket)
                ticket.partner_ticket_ids = [(5,)]
                ticket.partner_ticket_count = 0
                continue
            partner_id = ticket.partner_id
            if not partner_id and ticket.equipment_id and ticket.equipment_id.client_id:
                partner_id = ticket.equipment_id.client_id  # Fallback to equipment_id.client_id
            if partner_id:
                partner_tickets = self.env['it.incident'].search([
                    ('partner_id', '=', partner_id.id),
                    ('id', '!=', ticket.id),
                    ('id', '!=', False)
                ])
                _logger.info("Partner tickets for %s: %s (IDs: %s)", 
                             ticket.name or 'New', partner_tickets, partner_tickets.ids)
                ticket.partner_ticket_ids = partner_tickets
                ticket.partner_ticket_count = len(partner_tickets)
            else:
                _logger.info("No valid partner_id for %s, resetting partner_ticket_ids", 
                             ticket.name or 'New')
                ticket.partner_ticket_ids = [(5,)]
                ticket.partner_ticket_count = 0

    @api.onchange('equipment_id')
    def _onchange_equipment(self):
        """Synchronize partner_id with equipment_id.client_id."""
        if self.equipment_id and self.equipment_id.client_id:
            if self.equipment_id.client_id != self.partner_id:
                self.partner_id = self.equipment_id.client_id
        elif not self.equipment_id:
            self.partner_id = False
        _logger.info("Onchange equipment_id: partner_id=%s, equipment_id=%s, client_id=%s", 
                     self.partner_id, self.equipment_id, 
                     self.equipment_id.client_id if self.equipment_id else False)