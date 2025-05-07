from odoo import http
from odoo.http import request

class ItAssetPortal(http.Controller):
    @http.route(['/my/it_parks'], type='http', auth="user", website=True)
    def portal_it_parks(self):
        user = request.env.user
        partner = user.partner_id
        parks = request.env['it.parc.informatique'].search([('client_id', '=', partner.id)])
        return request.render('it_asset_management.portal_it_parks', {'parks': parks})

    @http.route(['/my/it_parks/<int:park_id>'], type='http', auth="user", website=True)
    def portal_it_park_details(self, park_id):
        park = request.env['it.parc.informatique'].browse(park_id)
        if park.client_id != request.env.user.partner_id:
            return request.redirect('/my')
        equipments = park.equipment_ids
        return request.render('it_asset_management.portal_it_park_details', {'park': park, 'equipments': equipments})