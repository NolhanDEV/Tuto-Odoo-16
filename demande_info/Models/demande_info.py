from odoo import models, fields, api
AVAILABLE_PRIORITIES = [
    ('0', 'peu important'),
    ('1', 'moyennement important'),
    ('2', 'important'),
    ('3', 'tres important'),
]

class DemandeInformation(models.Model):
    _name = "demande.information"
    _description = "Demande Information"

    name_id = fields.Many2one("res.partner", "Name", required=True)
    object = fields.Char(required=True)
    email = fields.Char(required=True)
    company = fields.Char(required=True)
    phone = fields.Char(required=True)
    description = fields.Char(required=False)
    date = fields.Date(required=False, copy=False)
    tag_ids = fields.Many2many("demande.information.tag", string="Tags")
    equipe_id = fields.Many2one("demande.information.equipe", string="Equipe")
    membre = fields.Many2one("res.users", string='membre')
    context = fields.Char(required=False)
    contact_id = fields.Many2one("res.partner", "Name", nocopy=True)
    status = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('en cours de traitement', 'En Cours De Traitement'), ('traité', 'Traité'),
                   ('assigné', 'Assigné')],
        required=True,)

    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    def contact_page(self, contact):
        act = {
                'type': 'ir.actions.act_window',
                'name': 'Contact Page',
                'view_mode': 'form',
                'res_model': 'res.partner',
                'res_id': contact.id,
                'views': [[self.env.ref('base.view_partner_form').id, 'form']],
            }
        return act

    def contact_create(self):
        company = self.env["res.partner"].search(
            [
                ('name', '=', self.company)
            ]
        )
        if not company:
            company = self.env["res.partner"].create(
                {
                    "name": self.company,
                })
        contact = self.env["res.partner"].create(
            {
                "name": self.name_id,
                "email": self.email,
                "phone": self.phone,
                "parent_id": company.id,
            })
        return contact

    def contact_button(self):

        contact = self.env['res.partner'].search(
            [
                ('name', '=', self.name_id),
                ('email', '=', self.email),
                ('phone', '=', self.phone),
                # ('parent_id', '=', self.company)
            ]
        )
        if contact:
            return self.contact_page(contact)
        else:
            self.contact_create()

    @api.onchange('name_id')
    def _onchange_contact_id(self):
        self.company = self.name_id.parent_id.name
        self.phone = self.name_id.phone
        self.email = self.name_id.email
class DemandeInformationTag(models.Model):
    _name = "demande.information.tag"
    _description = "Demande Information Tag"

    name = fields.Char(required=True)
    color = fields.Integer(required=True)

    _sql_constraints = [('unique_name', 'unique(name)', 'This Tag already exist')]

class DemandeInformationEquipe(models.Model):
    _name = "demande.information.equipe"
    _description = "Demande Information Equipe"

    name = fields.Char("name_id")

    _sql_constraints = [('unique_name', 'unique(name)', 'This Team already exist')]

class InheritUsers(models.Model):
    _inherit = "res.users"

    equipe_id = fields.Many2one("demande.information.equipe", string="equipe")

class InheritContact(models.Model):
    _inherit = 'res.partner'

    contact_id = fields.Many2one("demande.information", string="contact")
    name_id = fields.Many2one("demande.information", string="name")