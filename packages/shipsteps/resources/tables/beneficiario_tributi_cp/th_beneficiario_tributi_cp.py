#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class LookupView(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id', edit=True, hasDownArrow=True)
        r.fieldcell('beneficiario', edit=True, width='30em')
        r.fieldcell('cc_posta', edit=True)
        r.fieldcell('iban',edit=True, width='16em')
        
    def th_order(self):
        return 'beneficiario'

    def th_query(self):
        return dict(column='beneficiario', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('beneficiario')
        fb.field('cc_posta')
        fb.field('iban')
        


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
