from odoo import models, fields

class DemandeInformation(models.Model):
    _name = "demande.information"
    _description = "Demande Information"

    nom = fields.Char(required=True)
    prenom = fields.Char(required=True)
    mail = fields.Char(required=True)
    societe = fields.Char(required=True)
    tel = fields.Char(required=True)
    description = fields.Char(required=False)
    date = fields.Date(required=False, copy=False)
    tag_ids = fields.Many2many("demande.information.tag", string="Tags")
    statut = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('en cours de traitement', 'En Cours De Traitement'), ('traité', 'Traité'),
                   ('assigné', 'Assigné')],
        required=True,)

class DemandeInformationTag(models.Model):
    _name = "demande.information.tag"
    _description = "Demande Information Tag"

    name = fields.Char(required=True)
    color = fields.Integer(required=True)

    _sql_constraints = [('unique_name', 'unique(name)', 'This Tag already exist')]