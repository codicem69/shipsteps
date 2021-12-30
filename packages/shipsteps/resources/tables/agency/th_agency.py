#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_name')
        r.fieldcell('description')
        r.fieldcell('address')
        r.fieldcell('tel')
        r.fieldcell('fax')
        r.fieldcell('email')
        r.fieldcell('web')
        r.fieldcell('agent_name')
        r.fieldcell('mobile_agent')
        r.fieldcell('birthplace')
        r.fieldcell('birthdate')
        r.fieldcell('cciaa_n')
        r.fieldcell('cciaa_place')
        r.fieldcell('cf_agent')
        r.fieldcell('residence_address')
        r.fieldcell('cap_residence')
        r.fieldcell('residence_city')
        r.fieldcell('virtual_stamp')
        r.fieldcell('port')

    def th_order(self):
        return 'agency_name'

    def th_query(self):
        return dict(column='agency_name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
       # pane = form.record
       # fb = pane.formbuilder(cols=2, border_spacing='4px')
        bc = form.center.borderContainer()
        
        self.DatiAgenzia(bc.borderContainer(region='top',datapath='.record',height='500px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        #self.BolloVirtuale(tc.contentPane(title='Virtual Stamp description',datapath='.record'))
   
    def DatiAgenzia(self,bc):
        left = bc.roundedGroup(region='left', title='Agency details', width='100%').div(margin='10px',margin_right='20px')
        #center= bc.contentPane(region='center',title='Virtual stamp description').div(margin='10px',margin_right='20px')
               
        fb = left.formbuilder(cols=2, border_spacing='4px')
        fb.field('agency_name' )
        fb.field('description' )
        fb.field('address' )
        fb.field('tel' )
        fb.field('fax' )
        fb.field('email' )
        fb.field('web' )
        fb.field('agent_name' )
        fb.field('mobile_agent' )
        fb.field('birthplace' )
        fb.field('birthdate' )
        fb.field('cciaa_n' )
        fb.field('cciaa_place' )
        fb.field('cf_agent' )
        fb.field('residence_address' )
        fb.field('cap_residence' )
        fb.field('residence_city' )
        fb.simpleTextArea(lbl='Virtual stamp',value='^.virtual_stamp',editor=True, height='100px', width='100px' )
        fb.field('port' ,colspan=2)

   #def BolloVirtuale(self,frame):
   #    frame.simpleTextArea(title='Virtual stamp',value='^.virtual_stamp',editor=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
