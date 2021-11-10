# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api
from odoo.exceptions import UserError

class Vehicle(models.Model):
    _name = 'vehicle.vehicle'
    _description = "Vehicle Model"

    name = fields.Char(
        string="Name",
        required=True,
    )

    license_plate = fields.Char(
        string="license plate",
        required=True,
    )

    vehicle_type = fields.Selection(
        selection=[
                ('bike', 'bike'),
                ('car', 'car'),   
                ('truck', 'truck')
        ],
        required=True,
        string='vehicle type')

    daily_fare = fields.Float(
        string="daily fare",
        compute='_compute_daily_fare',
        store=True,
        required=True,
    )

    registration_year = fields.Integer(
        string="Registration year",
        required=True,
    )

    garage_id = fields.Many2one(
        comodel_name='garage.garage',
        string="Garage"
    )
    _sql_constraints = [("license_plate_unique", "UNIQUE(license_plate)", "Warning: license plate already exists!")]
    @api.model
    def create(self,values):
        values['name']=values['name'].upper()
        garage = self.env['garage.garage'].search([('id', '=', values["garage_id"])])
        if garage.vehicles_number == garage.vehicles_number_compute:
            raise UserError("Maximum veichle reached")
        return super(Vehicle,self).create(values)


    @api.depends("vehicle_type")
    def _compute_daily_fare(self):
        if self.vehicle_type == 'bike':
            self.daily_fare=5
        elif self.vehicle_type == 'car':
            self.daily_fare=10
        elif self.vehicle_type == 'truck':
            self.daily_fare=15

    def write(self,values):
        try:
            if values['name']!=None:
                values['name']=values['name'].upper()
        except KeyError:
            self.name = self.name.upper()
        return super(Vehicle,self).write(values)

