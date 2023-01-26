#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('port')
        r.fieldcell('description')
        r.fieldcell('subject_email')
        r.fieldcell('body_email', width='80em')

    def th_order(self):
        return 'port'

    def th_query(self):
        return dict(column='port', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('port')
        fb.field('description')
        fb.field('subject_email')
        fb.field('body_email')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromPrearrival_df(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"
   
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.prearrdf_left(bc.contentPane(region='left',datapath='.record', width='50%',splitter=True))
        self.prearrdf_center(bc.contentPane(region='center'))

    def prearrdf_left(self,bc):
        left = bc.roundedGroup(title='Dati Istanza',region='left', height = 'auto').div(margin='10px',margin_left='2px')
        fb = left.formbuilder(cols=2, border_spacing='4px')
        fb.field('port')
        fb.field('description', width='35em')
        fb.field('subject_email', width='57em', colspan=2)
        fb.field('body_email', tag='simpleTextArea', editor=True, width='50em', height='50em', colspan=2)

    def prearrdf_center(self,pane):
        pane.attachmentGrid(viewResource='View')  

