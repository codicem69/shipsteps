#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('vessel_details')
        r.fieldcell('cert')
        r.fieldcell('issued')
        r.fieldcell('date_cert')
        r.fieldcell('expire')
        r.fieldcell('annual_place')
        r.fieldcell('annual_date')
        r.fieldcell('note')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

class ViewFromDoc(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        #r.fieldcell('vessel_details')
        r.fieldcell('cert', width='30em', edit=True, hasArrowDown=True, order_by='code')
        r.fieldcell('issued',auxColumns='@nazione_code.nome,$unlocode',limit=20, edit=True,batch_assign=True)
        r.fieldcell('date_cert', edit=True,batch_assign=True)
        r.fieldcell('expire', edit=True,batch_assign=True)
        r.fieldcell('annual_place',auxColumns='@nazione_code.nome,$unlocode',limit=20, edit=True,batch_assign=True)
        r.fieldcell('annual_date', edit=True,batch_assign=True)
        r.fieldcell('note', edit=True, width='20em')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,resourcePrints,10,certificati,10,batchAssign')
        btn_certificati=bar.certificati.button('!![en]Insert certificates')
        btn_certificati.dataRpc('nome_temp',self.insertCert, record='=#FORM.record')
        bar.dataController("if(msgspec=='presenti') genro.publish('floating_message',{message:'Certificates already inserted', messageType:'error'});", msgspec='^nome_temp')

    @public_method
    def insertCert(self, record=None, **kwargs):
        
        tbl_cert=self.db.table('shipsteps.ship_cert')
        vess_det_id=record['id']
        certificati = tbl_cert.query(columns="$code,$certificate", order_by='$code').fetch() 
        
        tbl_shipdoc = self.db.table('shipsteps.ship_doc')
        shipdoc = tbl_shipdoc.query(columns="$cert", where='$vessel_details=:vd', vd=vess_det_id).fetch() 
        
        if len(shipdoc) >= 21:
            nome_temp = 'presenti'
            return nome_temp

        for e in range(len(certificati)):
            
            new_cert = self.db.table('shipsteps.ship_doc').newrecord(vessel_details=vess_det_id,cert=certificati[e][0])
            self.db.table('shipsteps.ship_doc').insert(new_cert)
        #print(c)
        self.db.commit()

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('_row_count')
        fb.field('vessel_details')
        fb.field('cert')
        fb.field('issued')
        fb.field('date_cert')
        fb.field('expire')
        fb.field('annual_place')
        fb.field('annual_date')
        fb.field('note')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
