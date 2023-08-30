#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('data_arr')
        r.fieldcell('data_part')
        r.fieldcell('arr_dep')
        r.fieldcell('comunitari')
        r.fieldcell('extraue')
        
    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    #def th_form(self, form):
    #    pane = form.record
    #    fb = pane.formbuilder(cols=2, border_spacing='4px')
    #    fb.field('arrival_id' )
    #    fb.field('data_arr' )
    #    fb.field('data_part' )
    #    fb.field('arr_dep' )

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        #bc = tc.borderContainer(title='Form')
        self.paxTestata(bc.borderContainer(region='top',datapath='.record',height='100px'))
        self.paxRighe(bc.contentPane(region='center'))

    def paxTestata(self,bc):    
        center = bc.roundedGroup(title='!![en]Pax list details',region='center',width='auto')
        
        fb = center.formbuilder(cols=4, border_spacing='4px')   
        fb.field('arrival_id')
        fb.field('data_arr')
        fb.field('data_part')
        fb.radioButtonText(value='^.arr_dep', values='Arrival:Arrival,Departure:Departure', lbl='Pax List arr/dep: ',validate_notnull=True) 
        fb.field('comunitari')
        fb.field('extraue')
        right = bc.roundedGroup(region='right',title='!![en]Vessel stamp',width='300px')
        right.img(src='^.@arrival_id.vessel_stamp', edit=True, crop_width='200px', crop_height='100px', border='2px dotted silver',margin_left='5px',
                        placeholder=True,upload_folder='*')
        
    def paxRighe(self,bc):
        center = bc.contentPane(region='center',width='500px')#, datapath='shipsteps_shorepass_righe')
        
        center.inlineTableHandler(relation='@paxlist_righe',viewResource='ViewFromPaxRighe', export=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
