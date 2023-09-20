#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('date', width='9em')
        r.fieldcell('imbarcazione_id', width='20em')
        r.fieldcell('istanza')
        r.fieldcell('id_istanza')
        r.fieldcell('ref_number')
        r.fieldcell('bolli_tr14', totalize=True)
        r.fieldcell('bolli_tr22', totalize=True)
        r.fieldcell('note')
        r.fieldcell('nome_agenzia', hidden=True)

    def th_order(self):
        return 'date'

    def th_query(self):
        return dict(column='id', op='contains', val='')
    
    def th_options(self):
        return dict(partitioned=True)
    
    def th_hiddencolumns(self):
        return "$nome_agenzia"

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px', fld_width='30em', colswidth='auto')
        fb.field('date' )
        fb.field('imbarcazione_id', hasDownArrow=True )
        fb.field('istanza')
        fb.field('id_istanza' )
        fb.field('ref_number' )
        fb.field('bolli_tr14' )
        fb.field('bolli_tr22' )
        fb.field('note', tag='simpleTextArea' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
