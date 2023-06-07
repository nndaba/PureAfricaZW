# -*- coding: utf-8 -*-
# from odoo import http


# class AutomationWorkflow(http.Controller):
#     @http.route('/automation_workflow/automation_workflow', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automation_workflow/automation_workflow/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('automation_workflow.listing', {
#             'root': '/automation_workflow/automation_workflow',
#             'objects': http.request.env['automation_workflow.automation_workflow'].search([]),
#         })

#     @http.route('/automation_workflow/automation_workflow/objects/<model("automation_workflow.automation_workflow"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automation_workflow.object', {
#             'object': obj
#         })
