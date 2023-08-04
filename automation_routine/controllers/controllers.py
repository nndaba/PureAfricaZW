# -*- coding: utf-8 -*-
# from odoo import http


# class AutomationRoutine(http.Controller):
#     @http.route('/automation_routine/automation_routine', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automation_routine/automation_routine/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('automation_routine.listing', {
#             'root': '/automation_routine/automation_routine',
#             'objects': http.request.env['automation_routine.automation_routine'].search([]),
#         })

#     @http.route('/automation_routine/automation_routine/objects/<model("automation_routine.automation_routine"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automation_routine.object', {
#             'object': obj
#         })
