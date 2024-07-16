#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import floatToDecimal,decimalRound
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('prot')
        r.fieldcell('data')
        r.fieldcell('arrival_id')
        r.fieldcell('importo')

    def th_order(self):
        return 'prot:d'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

    def th_options(self):
        return dict(partitioned=True)
    
   
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('prot' )
        fb.field('data',validate_notnull=True )
        fb.field('arrival_id' , hasDownArrow=True, order_by='$date DESC', colspan=2, width='100%')
        fb.br()
        fb.field('importo' )
        fb.br()
        btn_adm = fb.Button('!![en]Print Administration charge', hidden='^.arrival_id?=#v==null')
        fb.dataRpc('.importo', self.calcoloAdmincharge, arr='^.arrival_id',_if='arr',gt='=#FORM.record.@arrival_id.@vessel_details_id.@imbarcazione_id.gt',
                       _onResult='this.form.save();')
        btn_adm.dataRpc('nome_temp', self.print_template_admincharge,record='=#FORM.record',nome_template = 'shipsteps.adminchargerec:admincharge',
                        format_page='A4',_onResult='this.form.save();')
        
    @public_method
    def calcoloAdmincharge(self, gt=None,**kwargs):
        tbl_admincharge=self.db.table('shipsteps.admincharge')
        admincharge = tbl_admincharge.query(columns="$importo,$descrizione",
                         where='').fetch()
        #convertiamo la virgola in gt in punto per la successiva conversione da stringa ad int 
        gt = float(gt.replace(',','.'))

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

    @public_method
    def print_template_admincharge(self, record, nome_template=None, format_page=None, **kwargs):
        rec_id=record['id']
        tbl_admincharge = self.db.table('shipsteps.adminchargerec')
        builder = TableTemplateToHtml(table=tbl_admincharge)

        nome_temp = nome_template.replace('shipsteps.adminchargerec:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
        letterhead=''      
        for r in range(len(templates)):
            if templates[r][1] == 'A4_vert':
                letterhead = templates[r][0]    
            if format_page=='A3':
                if templates[r][1] == 'A3_orizz':
                    letterhead = templates[r][0]
          
        builder(record=rec_id, template=template,letterhead_id=letterhead)
        result = builder.writePdf(pdfpath=pdfpath)
        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',defaultPrompt=dict(title='!![en]New receipt', fields=self.newRecParameters()) )

    def newRecParameters(self):
        return [dict(value='^.data', lbl='!![en]Arrival date',tag='dateTextBox',
                    validate_notnull=True, hasDownArrow=True)]