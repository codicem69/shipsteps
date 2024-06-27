#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('ora_arr')
        r.fieldcell('data_arr')
        r.fieldcell('sosta_gg')
        #r.fieldcell('rif_alim')
        #r.fieldcell('bilge')
        #r.fieldcell('cargo_res')
        #r.fieldcell('altro')
        #r.fieldcell('altro_spec')
        r.fieldcell('invio_fat',width='100%')
        r.fieldcell('note', width='100%')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromGarbage(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('ora_arr', edit=dict(validate_notnull=True))
        r.fieldcell('data_arr', edit=dict(validate_notnull=True))
        r.fieldcell('sosta_gg', edit=dict(validate_notnull=True))
        #r.fieldcell('rif_alim', edit=True)
        #r.fieldcell('bilge', edit=True)
        #r.fieldcell('cargo_res', edit=True)
        #r.fieldcell('altro', edit=True)
        #r.fieldcell('altro_spec', edit=True, width='25em')
        r.fieldcell('invio_fat', edit=True, width='40em')
        r.fieldcell('note', edit=True, width='30em')
        
class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.garbageTestata(bc.borderContainer(region='top',datapath='.record',height='150px'))
        self.garbageRighe(bc.contentPane(region='center'))

    def garbageTestata(self,bc):
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb = bc.formbuilder(cols=3, border_spacing='4px',colswidth='auto',fld_width='80%',width='80%')    
        
        #fb.field('arrival_id' )
        fb.field('ora_arr', width='10em' )
        fb.field('data_arr', width='10em' )
        fb.field('sosta_gg', width='10em' )
        #fb.field('rif_alim' )
        #fb.field('bilge' )
        #fb.field('cargo_res' )
        #fb.field('altro' )
        #fb.field('altro_spec' )
        fb.field('invio_fat', colspan=3, tag='simpleTextArea' )
        fb.field('note', colspan=3, tag='simpleTextArea' )

        btn_note=fb.Button('!![en]Insert note', width='6em')
        btn_note.dataRpc('.note', self.insertNote,
                   record='=#FORM.record', 
                   _ask=dict(title='!![en]Select note to insert',fields=[dict(name='note', lbl='!![en]Note', tag='filteringSelect',
                            values='1:Si prega effettuare il ritiro alle ore,2:Si prega inserire nel formulario i quantitativi riportati',hasDownArrow=True),
                            dict(name='ora_ritiro', lbl='!![en]Time', tag='timeTextBox',validate_notnull="^.note?=#v=='1'", 
                            hidden="^.note?=#v!='1'?true:false")]),_onResult="this.form.save();")
        
    @public_method
    def insertNote(self,**kwargs):
        
        if kwargs:    
            if kwargs['note'] == '1':
                note = 'Si prega effettuare il ritiro alle ore ' + kwargs['ora_ritiro'].strftime("%H:%M") + ' ed inserire nel formulario i quantitativi riportati'   
            if kwargs['note'] == '2':
                note = 'Si prega inserire nel formulario i quantitativi riportati'
        print(x)             
        return note


    def garbageRighe(self,pane):
        pane.inlineTableHandler(relation='@garbage',viewResource='ViewFromGarbageDet',
                            picker='tip_garbage_id')

    def th_options(self):
        #return dict(dialog_height='400px', dialog_width='600px' )
        return dict(dialog_windowRatio = 1, annotations= True )