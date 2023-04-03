#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('logo_cp', width='60em')
        r.fieldcell('logo_imm', width='60em')

    def th_order(self):
        return 'id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        bc= form.center.borderContainer()
        self.loghi(bc.borderContainer(region='top',datapath='.record',height='100%', splitter=True))

    def loghi(self,bc):
        logocp = bc.roundedGroup(title='Logo CP',width='160px',region='left')
        logocp.img(src='^.logo_cp', edit=True, crop_width='150px', crop_height='150px',
                        placeholder=True, upload_folder='*')
        logoimm = bc.roundedGroup(title='Logo Immigration',width='260px',region='center')
        logoimm.img(src='^.logo_imm', edit=True, crop_width='250px', crop_height='350px',
                        placeholder=True, upload_folder='*')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
