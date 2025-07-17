#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('pfda_id')
        r.fieldcell('invoice_det_id',width='100%')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='int_fat', op='contains', val='')

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('delrow','load_pfda,25,delrow')
        btn_pfda=bar.load_pfda.button('!![en]Load PFDA',hidden="""^gnr.avatar.user?=#v!='admin'""")
        btn_pfda.dataRpc(self.load_pfda,record='=#FORM.record')

    @public_method
    def load_pfda(self, record, **kwargs):
        record_id = record['id']
               
        tbl_arrival = self.db.table('shipsteps.arrival')
        
        tbl_fda = self.db.table('shipsteps.fda')
        record_arr = tbl_arrival.query(columns="*",where='').fetch()
        
        for r in record_arr:
            if not tbl_fda.checkDuplicate(arrival_id=r['id'],invoice_det_id=r['invoice_det_id']):
                nuovo_rec = dict(arrival_id=r['id'],pfda_id=r['pfda_id'],invoice_det_id=r['invoice_det_id'])
                tbl_fda.insert(nuovo_rec)
        
        self.db.commit() 

class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.datiFDA(bc.roundedGroupFrame(title='Dati FDA',region='top',datapath='.record',height='50px', background='lightgrey', splitter=True))
        bc_fdarighe = bc.borderContainer(region = 'center',margin='2px')
        
        self.righeFDA(bc_fdarighe.contentPane(title='!![en]FDA rows',height='100%'))
    
    def datiFDA(self,pane):
        
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('pfda_id',hasDownArrow=True,  auxColumns='$data,@imbarcazione_id.nome,@cliente_id.cliente_full',order_by='$data DESC' )
        fb.field('invoice_det_id',hasDownArrow=True ,width='80em')

    def righeFDA(self,pane):
        pane.inlineTableHandler(relation='@fda_righe',viewResource='ViewFromRigheFda',liveUpdate=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
