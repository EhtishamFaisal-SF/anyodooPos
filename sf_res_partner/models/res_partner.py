# -*- coding: utf-8 -*-

#imports
from odoo import models, fields, api

#Inherit Res.partner class
class ResPartner(models.Model):
	#Private Attribs
	_inherit='res.partner'

	#fields
	logo = fields.Char(
	    string='Logo',
	)
	business_type = fields.Char(
	    string='Business Type',
	)

	cr = fields.Char(
	    string='CR',
	)
	subscription_start_date = fields.Date(
	    string='Subscription Start Date'
	)

	subscription_end_date = fields.Date(
	    string='Subscription End Date'
	)
