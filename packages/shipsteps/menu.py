#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    shipsteps = root.branch('shipsteps')
    shipsteps.thpage('!![en]Invoice details',table='shipsteps.invoice_det')
    shipsteps.thpage('!![en]Transit cargoes',table='shipsteps.cargo_transit')
    shipsteps.thpage('!![en]Cargoes unloding/loading',table='shipsteps.cargo_unl_load')
    shipsteps.thpage('Shippers-Receivers',table='shipsteps.ship_rec')
    shipsteps.thpage('!![en]Agencies',table='shipsteps.agency')
    shipsteps.thpage('!![en]Staff',table='shipsteps.staff')
    shipsteps.thpage('Shipdocs',table='shipsteps.shipdoc')
    shipsteps.thpage('!![en]Vessel details',table='shipsteps.vessel_details')
    shipsteps.thpage('!![en]Owners',table='shipsteps.owner')
    shipsteps.thpage('!![en]Arrivals',table='shipsteps.arrival')
    shipsteps.lookups('Lookup tables',lookup_manager='shipsteps')
