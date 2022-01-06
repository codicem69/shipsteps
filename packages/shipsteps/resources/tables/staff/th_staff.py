#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('user_id')
        r.fieldcell('agency_id')
        r.fieldcell('name')
        r.fieldcell('surname')
        r.fieldcell('telephone')
        r.fieldcell('email')
        r.fieldcell('note')
       # r.fieldcell('profile_photo')
        r.fieldcell('is_active')

    def th_order(self):
        return 'user_id'

    def th_query(self):
        return dict(column='username', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.staffDetails(bc.borderContainer(region='top',datapath='.record',height='295px', splitter=True))

    def staffDetails(self,bc):
        center= bc.contentPane(region='center',title='Staff details').div(margin='10px',margin_right='20px')
        fb = center.formbuilder(cols=1, border_spacing='4px')     
       
        fb.field('user_id' )
        fb.field('agency_id' )
        fb.field('name' )
        fb.field('surname' )
        fb.field('telephone' )
        fb.field('email' )
        fb.field('note', width='30em' )
       # fb.field('profile_photo' )
        fb.field('is_active' )
        right = bc.contentPane(region='right',title='Profile photo',width='200px', margin='10px')
     
        right.img(src='^.profile_photo', edit=True, crop_width='200px', crop_height='200px', 
                        placeholder=True, upload_folder='site:image', upload_filename='=.id')
        right.button('!![en]Remove image', hidden='^.profile_photo?=!#v').dataRpc(self.deleteImage, image='=.profile_photo')

    @public_method
    def deleteImage(self, image=None, **kwargs):
        image_path = self.sitepath + re.sub('/_storage/site', '',image).split('?',1)[0]
        os.remove(image_path)
        self.setInClientData(value=None, path='shipsteps_staff.form.record.profile_photo')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
