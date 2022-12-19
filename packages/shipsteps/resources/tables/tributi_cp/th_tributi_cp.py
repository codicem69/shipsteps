#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('beneficiario_id')
        r.fieldcell('causale')
        r.fieldcell('importo')
        r.fieldcell('imp_lettere')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class ViewFromTributi(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('beneficiario_id', edit=dict(validate_notnull=True), name='!![en]Beneficiary', width='30em')
        r.fieldcell('causale', edit=dict(validate_notnull=True), width='50em')
        r.fieldcell('importo', edit=dict(validate_notnull=True))
        r.fieldcell('imp_lettere', edit=True)
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('beneficiario_id')
        fb.field('causale')
        fb.field('importo')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
