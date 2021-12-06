# -*- coding: utf-8 -*-
# from odoo import http


# class SfResPartner(http.Controller):
#     @http.route('/sf_res_partner/sf_res_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sf_res_partner/sf_res_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sf_res_partner.listing', {
#             'root': '/sf_res_partner/sf_res_partner',
#             'objects': http.request.env['sf_res_partner.sf_res_partner'].search([]),
#         })

#     @http.route('/sf_res_partner/sf_res_partner/objects/<model("sf_res_partner.sf_res_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sf_res_partner.object', {
#             'object': obj
#         })
