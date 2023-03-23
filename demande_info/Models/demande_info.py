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
    status = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('en cours de traitement', 'En Cours De Traitement'), ('traité', 'Traité'),
                   ('assigné', 'Assigné')],
        required=True,)
    critere = fields.Selection(
        default='',
        selection=[('peu important', 'Peu important'), ('moyennement important', 'Moyennement Important'), ('important', 'Important'),('tres important', 'Tres Important')],
        nocopy=True,
    )
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    membre_odoo = fields.Selection(
        default='',
        selection=[('pierre', 'Pierre'), ('yann', 'Yann')]
    )

    membre_tech = fields.Selection(
        default='',
        selection=[('hendrick', 'Hendrick'), ('manu', 'Manu')]
    )

    def equipe_choice(self):
        for equipe in self:
            if equipe.id == 'Odoo':
                return 'membre_odoo',
            if equipe.id == 'Telecom':
                return 'membre_tech'
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