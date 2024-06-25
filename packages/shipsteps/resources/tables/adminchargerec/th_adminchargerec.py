#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import floatToDecimal,decimalRound

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('prot')
        r.fieldcell('data')
        r.fieldcell('arrival_id')
        r.fieldcell('importo')

    def th_order(self):
        return 'prot'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

    def th_options(self):
        return dict(partitioned=True)
    
   
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('prot' )
        fb.field('data' )
        fb.field('arrival_id' , hasDownArrow=True, order_by='$date DESC')
        fb.field('importo' )
        fb.field('agency_id' )
        fb.dataRpc('.importo', self.calcoloAdmincharge, arr='^.arrival_id',_if='arr',gt='=#FORM.record.@arrival_id.@vessel_details_id.@imbarcazione_id.gt',
                       _onResult='this.form.save();')
    
    @public_method
    def calcoloAdmincharge(self, gt=None,**kwargs):
        tbl_admincharge=self.db.table('shipsteps.admincharge')
        admincharge = tbl_admincharge.query(columns="$importo,$descrizione",
                         where='').fetch()
 
        for r in admincharge:
            if int(gt) <= 500:
                if r['descrizione'] == 'fino a 500 GT':
                    importo=r['importo']
            if int(gt) >= 501:
                if r['descrizione'] == 'da 501 a 2000 GT':
                    importo=r['importo']  
            if int(gt) >= 2001:
                if r['descrizione'] == 'da 2001 a 5000 GT':
                    importo=r['importo'] 
            if int(gt) >= 5001:
                if r['descrizione'] == 'da 5001 a 10000 GT':
                    importo=r['importo'] 
            if int(gt) >= 10001:
                if r['descrizione'] == 'da 10001 a 30000 GT':
                    importo=r['importo'] 
            if int(gt) >= 30001:
                if r['descrizione'] == 'da 30001 a 80000 GT':
                    importo=r['importo'] 

        importo = floatToDecimal(importo)
        return importo

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',defaultPrompt=dict(title='!![en]New receipt', fields=self.newRecParameters()) )

    def newRecParameters(self):
        return [dict(value='^.data', lbl='!![en]Arrival date',tag='dateTextBox',
                    validate_notnull=True, hasDownArrow=True)]