#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    shipsteps = root.branch('shipsteps')
    shipsteps.thpage('!![en]Operations SOF',table='shipsteps.sof_operations')
    shipsteps.thpage('sof',table='shipsteps.sof',formResource='FormSof')
    shipsteps.thpage('email arrival',table='shipsteps.email_arr')
    shipsteps.thpage('sof_cargo',table='shipsteps.sof_cargo')
    shipsteps.thpage('!![en]Invoice details',table='shipsteps.invoice_det')
    shipsteps.thpage('Sof tanks',table='shipsteps.sof_tanks')
    shipsteps.thpage('!![en]Cargoes unloding/loading',table='shipsteps.cargo_unl_load')
    shipsteps.thpage('!![en]arrival times',table='shipsteps.arrival_time')
    shipsteps.thpage('Shippers-Receivers',table='shipsteps.ship_rec')
    shipsteps.thpage('!![en]Agencies',table='shipsteps.agency')
    shipsteps.thpage('!![en]Staff',table='shipsteps.staff')
    shipsteps.thpage('Shipdocs',table='shipsteps.shipdoc')
    shipsteps.thpage('GPG',table='shipsteps.gpg')
    shipsteps.thpage('!![en]Arrival details',table='shipsteps.arrival_det')
    shipsteps.thpage('!![en]Vessel details',table='shipsteps.vessel_details')
    shipsteps.thpage('!![en]Owners',table='shipsteps.owner')
    shipsteps.thpage('!![en]Arrivals',table='shipsteps.arrival')
    shipsteps.lookups('Lookup tables',lookup_manager='shipsteps')
