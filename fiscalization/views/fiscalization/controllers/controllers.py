# -*- coding: utf-8 -*-
# from odoo import http


# class Fiscalization(http.Controller):
#     @http.route('/fiscalization/fiscalization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fiscalization/fiscalization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fiscalization.listing', {
#             'root': '/fiscalization/fiscalization',
#             'objects': http.request.env['fiscalization.fiscalization'].search([]),
#         })

#     @http.route('/fiscalization/fiscalization/objects/<model("fiscalization.fiscalization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fiscalization.object', {
#             'object': obj
#         })
