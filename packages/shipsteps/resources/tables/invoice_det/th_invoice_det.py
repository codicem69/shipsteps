#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
       
        r.fieldcell('rag_sociale')
        r.fieldcell('address')
        r.fieldcell('cap')
        r.fieldcell('city')
        r.fieldcell('vat')
        r.fieldcell('cf')
        r.fieldcell('cod_univoco')
        r.fieldcell('pec')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='rag_sociale', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        
        fb.field('rag_sociale', width='54em',colspan=2 )
        fb.br()
        fb.field('address', width='30em' )
        fb.field('cap' )
        fb.field('city', width='30em' )
        fb.field('vat' )
        fb.field('cf' )
        fb.field('cod_univoco' )
        fb.field('pec' )


    def th_options(self):
        return dict(dialog_windowRatio = 1 , annotations= True )
        #return dict(dialog_height='600px', dialog_width='800px' )
