from odoo import models, fields

class DemandeInformation(models.Model):
    _name = "demande.information"
    _description = "Demande Information"

    nom = fields.Char(required=True)
    prenom = fields.Char(required=True)
    mail = fields.Char(required=True)
    societe = fields.Char(required=True)
    tel = fields.Char(required=True)