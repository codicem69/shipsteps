#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code', width='3em')
        r.fieldcell('agency_name')
        r.fieldcell('description')
        r.fieldcell('address')
        r.fieldcell('tel', width='6em')
        r.fieldcell('fax', width='6em')
        r.fieldcell('email')
        r.fieldcell('web')
        r.fieldcell('agent_name')
        r.fieldcell('mobile_agent', width='8em')
        r.fieldcell('birthplace', width='8em')
        r.fieldcell('birthdate')
        r.fieldcell('cciaa_n', width='5em')
        r.fieldcell('cciaa_place', width='6em')
        r.fieldcell('cf_agent')
        r.fieldcell('residence_address')
        r.fieldcell('cap_residence', width='5em')
        r.fieldcell('residence_city', width='7em')
        r.fieldcell('virtual_stamp')
        r.fieldcell('emailpec_account_id')
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
       # tc = bc.tabContainer(margin='2px',region='center')
        #self.BolloVirtuale(tc.contentPane(title='Virtual Stamp description',datapath='.record'))
        
    def DatiAgenzia(self,bc):
        center = bc.roundedGroup(region='center', title='Agency details').div(margin='10px',margin_right='20px')
        #center= bc.contentPane(region='center',title='Virtual stamp description').div(margin='10px',margin_right='20px')
               
        fb = center.formbuilder(cols=2, border_spacing='4px',fld_width='30em')
        fb.field('code', placeholder='Max 2 letters' )
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
        fb.simpleTextArea(lbl='Virtual stamp',value='^.virtual_stamp',editor=True, height='150px', width='150px' )
        fb.field('emailpec_account_id', hasDownArrow=True )

        fb.field('port' ,colspan=2)
        fb.br()
        right = bc.roundedGroup(region='right',title='!![en]Agency stamp',width='400px')
        #right = bc.roundedGroup(region='right',title='!![en]Agency stamp', width='20%', height='100%', margin='10px',margin_right='20px')
        #cp=right.contentPane()
        right.img(src='^.agency_stamp', edit=True, crop_width='100px', crop_height='100px', border='2px dotted silver',
                        placeholder=True, upload_folder='site:image', upload_filename='=.id', width='100px', height='100px')
        #right.button('!![en]Remove image', hidden='^.agency_stamp?=!#v').dataRpc(self.deleteImage, image='=.agency_stamp')

   #def BolloVirtuale(self,frame):
   #    frame.simpleTextArea(title='Virtual stamp',value='^.virtual_stamp',editor=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

    #@public_method
    #def deleteImage(self, image=None, **kwargs):
    #    image_path = self.sitepath + re.sub('/_storage/site', '',image).split('?',1)[0]
    #    os.remove(image_path)
    #    self.setInClientData(value=None, path='shipsteps_staff.form.record.agency_stamp')