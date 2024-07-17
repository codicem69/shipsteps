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
        bc = form.center.borderContainer()
        self.folder(bc.roundedGroupFrame(title='!![en]Folder',region='top',datapath='.record',height='210px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.protocollo(tc.contentPane(title='!![en]Arrival logs'))
        self.protAssegnato(tc.contentPane(title='!![en]Corrispondend Arrival logs'))

    def folder(self,pane):
        #pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('_row_count')
        fb.field('agency_id', readOnly=True)
        fb.field('numero')
        fb.field('dal')
        fb.field('al')
    
    def protocollo(self,pane):
        pane.dialogTableHandler(table='shipsteps.protocollo',#relation='@numero_faldone',
                                viewResource='ViewFromFolder',extendedQuery=True,pbl_classes=True, view_store_onStart=True)

    def protAssegnato(self,pane):
        pane.dialogTableHandler(relation='@numero_faldone',
                                viewResource='View',extendedQuery=True,pbl_classes=True, view_store_onStart=True)
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
