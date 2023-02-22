#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id')
        r.fieldcell('description')
        r.fieldcell('pathfile')
        r.fieldcell('notestandard',width='60em')

    def th_options(self):
        return dict(partitioned=True)

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('agency_id', hasDownArrow=True)
        fb.field('description')
        fb.field('pathfile', width='60em', readOnly=True)
        fb.br()            
        fb.div("Documento port info da allegare all'email", height='0px', padding='20px')  
        fb.br()          
        fb.div(hidden='^.pathfile?=#v', lbl='File').dropUploader(height='100px', width='320px',colspan=2,
                            label="<div style='padding:5px'>Drop document port general info here <br>or double click</div>",
                            uploadPath='site:files', 
                            progressBar=True,
                            onUploadedMethod=self.uploadFile)
        fb.button('!![en]Remove file', hidden='^.pathfile?=!#v').dataRpc(self.deleteFile, file='=.pathfile', record='=#FORM.record', _onResult="this.form.reload();")
        fb.simpleTextArea(lbl='!![en]Default notes',value='^.notestandard',editor=True, height='300px', width='600px' )


