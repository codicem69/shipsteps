#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('arrival_id')
        r.fieldcell('rank_off')
        r.fieldcell('name_off')
        r.fieldcell('datetime_bunk')
        r.fieldcell('service')
        r.fieldcell('durata')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('rank_off')
        fb.field('name_off')
        fb.field('datetime_bunk')
        fb.field('service')
        fb.field('durata')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromBunker(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        #bc = tc.borderContainer(title='Form')
        self.bunkerTestata(bc.borderContainer(region='top',datapath='.record',height='100px'))
        self.bunkerRighe(bc.contentPane(region='center'))

    def bunkerTestata(self,bc):    
        left = bc.roundedGroup(title='Dati Bunker',region='center',width='auto')
        fb = left.formbuilder(cols=3, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('rank_off')
        fb.field('name_off')
        fb.field('datetime_bunk')
        fb.field('service')
        fb.field('durata')
    
    def bunkerRighe(self,pane):
        pane.inlineTableHandler(relation='@bunker_righe',viewResource='ViewFromBunkerRighe')
