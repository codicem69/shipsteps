#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count')
        r.fieldcell('agency_id')
        r.fieldcell('data')
        r.fieldcell('data_prat', width='6em')
        r.fieldcell('prot_n',width='6em')
        r.fieldcell('fald_n')
        r.fieldcell('arrival_id')
        r.fieldcell('description', width='50em')

    def th_order(self):
        return '_row_count:d'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

class ViewFromFolder(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count')
        r.fieldcell('agency_id')
        r.fieldcell('data')
        r.fieldcell('data_prat', width='6em')
        r.fieldcell('prot_n',width='6em')
        r.fieldcell('fald_n')
        r.fieldcell('arrival_id')
        r.fieldcell('description', width='50em')

    def th_order(self):
        return '_row_count:d'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('*,batchass,2,batchAssign,*',
                        childname='superiore',_position='<bar')
                        #,gradient_from='#999',gradient_to='#888')
        bar.batchass.div('!![en]Assign Folder to the Arrival logs')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('_row_count')
        fb.field('agency_id', readOnly=True )
        fb.field('data')
        fb.field('data_prat')
        fb.field('prot_n')
        fb.field('fald_n',hasDownArrow=True)
        fb.br()
        fb.field('arrival_id',order_by='$arrival_data DESC', hasDownArrow=True, width='50em',colspan=2,selected_cargo_descr='.description')
        #fb.dbSelect(dbtable='shipsteps.arrival',lbl='!![en]Arrival',auxColumns='$arrival_data',
        #            selected_arrival_data='.description',order_by='$arrival_data DESC',
        #                hasDownArrow=True, width='28em', colspan=2)
        fb.br()
        fb.field('description', width='50em',colspan=2)


    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px')
