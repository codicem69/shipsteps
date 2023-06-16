#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('facility_code', width='7em')
        r.fieldcell('country')
        r.fieldcell('port_name')
        r.fieldcell('facility_name')
        r.fieldcell('description', width='40em')
        r.fieldcell('longitude', width='7em')
        r.fieldcell('latitude', width='7em')
        r.fieldcell('plan_approved', width='5em')
        r.fieldcell('last_updated', width='8em')

    def th_order(self):
        return 'facility_code'

    def th_query(self):
        return dict(column='facility_code', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('facility_code' )
        fb.field('country' )
        fb.field('port_name' )
        fb.field('facility_name' )
        fb.field('description' )
        fb.field('longitude' )
        fb.field('latitude' )
        fb.field('plan_approved' )
        fb.field('last_updated' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
