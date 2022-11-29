#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count')
        r.fieldcell('agency_id')
        r.fieldcell('numero')
        r.fieldcell('dal')
        r.fieldcell('al')
        

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('_row_count')
        fb.field('agency_id', readOnly=True)
        fb.field('numero')
        fb.field('dal')
        fb.field('al')
        


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
