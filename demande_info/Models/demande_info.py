from odoo import models, fields
AVAILABLE_PRIORITIES = [
    ('0', 'peu important'),
    ('1', 'moyennement important'),
    ('2', 'important'),
    ('3', 'tres important'),
]

class DemandeInformation(models.Model):
    _name = "demande.information"
    _description = "Demande Information"

    nom = fields.Char(required=True)
    prenom = fields.Char(required=True)
    object = fields.Char(required=True)
    mail = fields.Char(required=True)
    societe = fields.Char(required=True)
    tel = fields.Char(required=True)
    description = fields.Char(required=False)
    date = fields.Date(required=False, copy=False)
    tag_ids = fields.Many2many("demande.information.tag", string="Tags")
    equipe_id = fields.Many2one("demande.information.equipe", string="Equipe")
    membre = fields.Many2one("res.users", string='membre')
    context = fields.Char(required=False)
    status = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('en cours de traitement', 'En Cours De Traitement'), ('traité', 'Traité'),
                   ('assigné', 'Assigné')],
        required=True,)

    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])
class DemandeInformationTag(models.Model):
    _name = "demande.information.tag"
    _description = "Demande Information Tag"

    name = fields.Char(required=True)
    color = fields.Integer(required=True)

    _sql_constraints = [('unique_name', 'unique(name)', 'This Tag already exist')]

class DemandeInformationEquipe(models.Model):
    _name = "demande.information.equipe"
    _description = "Demande Information Equipe"

    name = fields.Char("nom")

    _sql_constraints = [('unique_name', 'unique(name)', 'This Team already exist')]

class InheritUsers(models.Model):
    _inherit = "res.users"

    equipe_id = fields.Many2one("demande.information.equipe", string="equipe")

# class search(models.Model):
#     _inherit = 'res.partner'
#     def get_demande(self):
#         self.ensure_one()
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Demande',
#             'view_mode': 'tree',
#             'res_model': 'contacts.demande',
#             'domain': [('contacts_id', '=', self.id)],
#             'context': "{'create': False}"
#         }