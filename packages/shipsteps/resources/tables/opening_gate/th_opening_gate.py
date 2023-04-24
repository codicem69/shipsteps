#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('details')
        #r.fieldcell('map')

    def th_order(self):
        return 'details'

    def th_query(self):
        return dict(column='details', op='contains', val='')
    
    def th_options(self):
        return dict(partitioned=True)
    
class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        #tc = form.center.tabContainer()
        #bc = tc.borderContainer()
        self.details(bc.contentPane(title='!![en]Details',region='top',datapath='.record',height='300px', splitter=True))
        #self.details(bc.borderContainer(region='top',datapath='.record',height='50px', splitter=True))
        self.map(bc.borderContainer(region='center',datapath='.record'))

    def details(self,frame):
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('details' )
        frame.simpleTextArea(title='Arrival note',value='^.details',editor=True)

    def map(self,bc):
        rg_map= bc.roundedGroup(region='left',title='Image map',width='50%').div(margin='10px',margin_right='20px')
        rg_extra=bc.roundedGroup(region='center',title='Extra',width='50%').div(margin='10px',margin_right='20px')
        fb = rg_map.formbuilder(cols=2, border_spacing='4px')
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.img(src='^.map', edit=True, crop_width='400px', crop_height='300px', 
                        placeholder=True, upload_folder='*')
        fb = rg_extra.formbuilder(cols=2, border_spacing='4px')
        fb.field('agency_id')
        fb.field('port')
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
