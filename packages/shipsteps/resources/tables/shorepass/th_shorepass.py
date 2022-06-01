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

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        #bc = tc.borderContainer(title='Form')
        self.shorepassTestata(bc.borderContainer(region='top',datapath='.record',height='100px'))
        self.shorepassRighe(bc.contentPane(region='center'))

    def shorepassTestata(self,bc):    
        center = bc.roundedGroup(title='!![en]Shorepass details',region='center',width='auto')
        fb = center.formbuilder(cols=3, border_spacing='4px')   
        fb.field('arrival_id')
        fb.field('data_arr')
        fb.field('data_part')

    def shorepassRighe(self,bc):
        center = bc.contentPane(region='center',width='500px')#, datapath='shipsteps_shorepass_righe')
        
        center.inlineTableHandler(relation='@shorepass_righe',viewResource='ViewFromShorepassRighe')
        


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
