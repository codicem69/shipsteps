#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('imbarcazione_id', name='Vessel')
        r.fieldcell('owner_id', name='Owner')
        r.fieldcell('imo')
        r.fieldcell('callsign')
        r.fieldcell('built')
        r.fieldcell('dwt')
        r.fieldcell('beam')
        r.fieldcell('mmsi')
        r.fieldcell('reg_place')
        r.fieldcell('reg_num')
        r.fieldcell('ex_name')
        r.fieldcell('vess_note',width='auto')
        #r.fieldcell('vess_image')

    def th_order(self):
        return 'imbarcazione_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        # pane = form.record
        bc = form.center.borderContainer()
        
        self.vesselName(bc.borderContainer(region='top',datapath='.record',height='295px', splitter=True,background='lightyellow'))
     #   self.vesselDetails(bc.borderContainer(region='center',datapath='.record',height='450px', width='50%', splitter=True))
       # bc = bc.borderContainer(region='right', width='50%', splitter=True)
        tc = bc.tabContainer(margin='2px',region='center')
        self.NoteNave(tc.contentPane(title='Vessel Note',datapath='.record'))
        self.allegatiNave(tc.contentPane(title='Attachments'))
   
    #def vesselDetails(self, bc):
    #   bc.contentPane(region='center')
    #   
    #   center = bc.roundedGroup(region='center',title='Vessel Details').div(margin='10px',margin_right='20px')
    #   fb = center.formbuilder(cols=1, border_spacing='4px')        
    #   fb.dbSelect('owner_id', width='20em', hasArrowDown=True )
    #   fb.field('imo', width='20em' )
    #   fb.field('callsign', width='20em' )
    #   fb.field('built', width='20em' )
    #   fb.field('dwt', width='20em' )
    #   fb.field('beam', width='20em' )
    #   fb.field('mmsi', width='20em' )
    #   fb.field('reg_place', width='20em' )
    #   fb.field('reg_num', width='20em' )
    #   fb.field('ex_name', width='40em' )
    #   fb.field('vess_note', width='40em' )
        

    def vesselName(self, bc):
       
        bc.contentPane(region='left', width='20%').linkerBox('imbarcazione_id',label='Vessel name',margin='2px',openIfEmpty=True, validate_notnull=True,
                                                    columns='$nome',
                                                    auxColumns='$tipo,$bandiera',
                                                    newRecordOnly=False,formResource='Form',
                                                    dialog_height='200px',dialog_width='700px')
        center= bc.roundedGroup(region='center',title='Vessel Details').div(margin='10px',margin_right='20px')
        fb = center.formbuilder(cols=1, border_spacing='4px')        
        fb.field('owner_id',lbl='Owner',auxColumns='$own_name',
                        hasDownArrow=True, width='20em')
        #fb.field('imo', width='20em' )
        fb.field('callsign', width='20em' )
        fb.field('built', width='20em' )
        fb.field('dwt', width='20em' )
        fb.field('beam', width='20em' )
        fb.field('mmsi', width='20em' )
        fb.field('reg_place',lbl='Reg. place',auxColumns='@nazione_code.nome',
                        width='20em' )
        fb.field('reg_num', width='20em' )
        fb.field('ex_name', width='40em' )
      

        right = bc.roundedGroup(region='right',title='Vessel Immagine',width='600px')
     
        right.img(src='^.vess_image', edit=True, crop_width='600px', crop_height='250px', 
                        placeholder=True, upload_folder='site:vessel', upload_filename='=.id')
        right.button('!![en]Remove image', hidden='^.vess_image?=!#v').dataRpc(self.deleteImage, image='=.vess_image')
  
    def NoteNave(self,frame):
        frame.simpleTextArea(title='Extra',value='^.vess_note',editor=True)

    def allegatiNave(self,pane):
        pane.attachmentGrid(viewResource='ViewFromVesselDocs')
        
    @public_method
    def deleteImage(self, image=None, **kwargs):
        image_path = self.sitepath + re.sub('/_storage/site', '',image).split('?',1)[0]
        os.remove(image_path)
        self.setInClientData(value=None, path='shipsteps_vessel_details.form.record.vess_image')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
