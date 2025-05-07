# -*- coding: utf-8 -*-
from odoo import fields, models

class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    is_close = fields.Boolean(
        string='Closing Stage',
        default=False,
        help="Indicate if this stage represents a closed ticket."
    )