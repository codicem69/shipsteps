#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('eosp', width='8em')
        r.fieldcell('aor', width='8em')
        r.fieldcell('anchored', width='8em')
        r.fieldcell('anchor_up', width='8em')
        r.fieldcell('pob', width='8em')
        r.fieldcell('first_rope', width='8em')
        r.fieldcell('moored', width='8em')
        r.fieldcell('poff', width='8em')
        r.fieldcell('gangway', width='8em')
        r.fieldcell('free_p', width='8em')
        r.fieldcell('pobd', width='8em')
        r.fieldcell('last_line', width='8em')
        r.fieldcell('sailed', width='8em')
        r.fieldcell('cosp', width='8em')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('eosp' )
        fb.field('aor' )
        fb.field('anchored' )
        fb.field('anchor_up' )
        fb.field('pob' )
        fb.field('first_rope' )
        fb.field('moored' )
        fb.field('poff')
        fb.field('gangway' )
        fb.field('free_p' )
        fb.field('pobd',border_color="^pildep") #tramite il datacontroller in th_sof viene assegnata alla variabile pildep il colore del bordo
        fb.field('last_line' )
        fb.field('sailed' ,border_color="^sail") #tramite il datacontroller in th_sof viene assegnata alla variabile sail il colore del bordo
        fb.field('cosp' )

        btn_arrivo=fb.button('Email arrival',hidden="^checksof")#.controller.title?=#v!=null")
        btn_partenza=fb.button('Email departure',hidden="^checksof")#.controller.title?=#v!=null")
        fb.dataRpc('checksof', self.checkSof,  record='=#FORM.record', cur_tab='^#FORM/parent/#FORM.current_tab',
                   rec_id='=.id',pkey='^#FORM.record.id',_if="cur_tab==5||rec_id")

        btn_arrivo.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_arrivo',
                            nome_template = 'shipsteps.arrival:email_arrivo',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        btn_partenza.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_departure',
                            nome_template = 'shipsteps.arrival:email_departure',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))

    @public_method
    def checkSof(self, record, **kwargs):
        tabname=kwargs['cur_tab']
        record_id = record['arrival_id']
        tbl_sof = self.db.table('shipsteps.sof')
        sof = tbl_sof.query(columns='$id',where = '$arrival_id = :arr_id', arr_id=record_id).fetch()
        if sof:
            return True
        else:
            return False
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
