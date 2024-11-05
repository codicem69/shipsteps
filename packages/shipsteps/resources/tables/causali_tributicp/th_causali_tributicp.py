#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class LookupView(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('uo_accertatrice')
        r.fieldcell('descr_pratica')
        r.fieldcell('code_pi')
        r.fieldcell('oggetto')
        r.fieldcell('sotto_oggetto')
        r.fieldcell('tariffa')
        r.fieldcell('note')
        r.fieldcell('norma')
        r.fieldcell('capitolo')
        r.fieldcell('iban')
        r.fieldcell('extra_descr')

    def th_order(self):
        return 'uo_accertatrice'

    def th_query(self):
        return dict(column='descr_pratica', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('uo_accertatrice' )
        fb.field('descr_pratica' )
        fb.field('code_pi' )
        fb.field('oggetto' )
        fb.field('sotto_oggetto' )
        fb.field('tariffa' )
        fb.field('note' )
        fb.field('norma' )
        fb.field('capitolo' )
        fb.field('iban' )
        fb.field('extra_descr' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
