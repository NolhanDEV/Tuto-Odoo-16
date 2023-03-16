from odoo import models, Command

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super(InheritedModel, self).action_sold()
        self.env["account.move"].create(
            {
                "name": "Invoice",
                "move_type": 'out_invoice',
                "partner_id": self.buyer.id,
                "journal_id": 1,
                "invoice_line_ids": [
                    Command.create({
                        "name": "seller_commission",
                        "quantity": 1,
                        "price_unit": 0.06*self.selling_price,
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    })
                ],
            }
        )
        return res