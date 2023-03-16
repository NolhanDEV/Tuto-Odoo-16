from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    description = fields.Text(required=False)
    postcode = fields.Char(required=False)
    date_availability = fields.Date(required=False, copy=False)
    selling_price = fields.Float(required=False, readonly=False, copy=False)
    bedrooms = fields.Integer(required=False, default=2)
    living_area = fields.Integer(required=False)
    active = fields.Boolean('Active', default=True)
    facades = fields.Integer(required=False)
    garage = fields.Boolean(required=False)
    garden = fields.Boolean(required=False)
    garden_area = fields.Integer(required=False)
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate North, South, East and West")
    state = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('offer sold', 'Offer Sold'), ('offer canceled', 'Offer Canceled'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,)
    salesman = fields.Many2one('res.users')
    buyer = fields.Many2one('res.partner')
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total")
    amount = fields.Float()
    best_price = fields.Float(compute="_compute_best_price")
    property_ids = fields.One2many("estate.property.type", "property_type_id")
    context = fields.Char(required=False)
    available = fields.Char(required=False)
    user_id = fields.Many2one("res.users")

    @api.ondelete(at_uninstall=True)
    def _state_(self):
        for property in self:
            if property.state in ("sold", "offer received", "offer accepted"):
                raise UserError("only new and canceled delete")

    @api.depends('living_area', 'garden_area')
    def _compute_total(property):
        for line in property:
            line.total_area = line.living_area + line.garden_area

    @api.depends("best_price")
    def _compute_best_price(self):
        list = [0]
        property = self
        #import pdb
        #pdb.set_trace()
        for offer in property.mapped('offer_ids'):
           list.append(offer.price)
        property.best_price = max(list)

    @api.onchange("garden")
    def _onchange_garden_id(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.constrains('expected_price')
    def check_expected_price(self):
        for property in self:
            if property.expected_price < 0:
                raise ValidationError("Number cannot be negative")
            if property.expected_price == 0:
                raise ValidationError("The expected price must be positive")

    @api.constrains('selling_price')
    def check_selling_price(self):
        for property in self:
            if property.selling_price < 0:
                raise ValidationError("Selling price must be positive")

    @api.constrains('selling_price')
    def check_selling_price(self):
        for property in self:
            if property.selling_price < 90 / 100 * property.expected_price:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")

    def action_sold(self):
        for property in self:
            if property.state == 'canceled':
                raise UserError("Canceled properties cannot be sold")
            else :
                property.state = "sold"

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold properties cannot be canceled")
            else :
                property.state = "canceled"


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_type_id = fields.Many2one('estate.property', string='Property Type')
    title = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    status = fields.Selection(
        default='new',
        selection=[('new', 'New'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True)
    _sql_constraints = [('unique_name', 'unique(name)', 'This Type already exist')]



class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(required=True)

    _sql_constraints = [('unique_name', 'unique(name)', 'This Tag already exist')]

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    name = fields.Char(required=False)
    price = fields.Float(required=False)
    status = fields.Selection(
        default='',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        nocopy=True,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(required=True)

    @api.constrains('price')
    def check_price(self):
        for property in self:
            if property.price < 0:
                raise ValidationError("Price must be positive")

    @api.constrains('price')
    def check_price(self):
        for property in self:
            if property.price < 'best_price':
                raise ValidationError("Price must be higher than the best price")

    def action_accept(self):
        for property in self:
            property.status = 'accepted'

    def action_refuse(self):
        for property in self:
            property.status = 'refused'

class InheritUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id")




