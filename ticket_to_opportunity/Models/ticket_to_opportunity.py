from odoo import models, fields

class InheritedModel(models.Model):
    _inherit = "helpdesk.ticket"

    def action_sold(self):
        self.env["demande.information"].create(
            {


