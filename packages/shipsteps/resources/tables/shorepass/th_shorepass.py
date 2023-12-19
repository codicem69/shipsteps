#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('arrival_id')
        r.fieldcell('data_arr', name='!![en]From date')
        r.fieldcell('data_part', name='!![en]To date')
        r.fieldcell('comunitari')
        r.fieldcell('extraue')
        
    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        #bc = tc.borderContainer(title='Form')
        self.shorepassTestata(bc.borderContainer(region='top',datapath='.record',height='100px'))
        self.shorepassRighe(bc.contentPane(region='center'))

    def shorepassTestata(self,bc):    
        center = bc.roundedGroup(title='!![en]Shorepass details',region='center',width='auto')
        
        fb = center.formbuilder(cols=3, border_spacing='4px')   
        fb.field('arrival_id')
        fb.div('Shorepass Validity', font_weight='bold')
        fb.br()
        fb.field('data_arr',lbl='!![en]From date')
        fb.field('data_part',lbl='!![en]To date')
        fb.br()
        fb.field('comunitari')
        fb.field('extraue')
        fb.radioButtonText(value='^.arr_dep', values='Arrival:Arrival,Departure:Departure', lbl='Crew List arr/dep: ',validate_notnull=True) 
        right = bc.roundedGroup(region='right',title='!![en]Vessel stamp',width='300px')
        right.img(src='^.@arrival_id.vessel_stamp', edit=True, crop_width='200px', crop_height='200px', border='2px dotted silver',margin_left='5px',
                        placeholder=True,upload_folder='*')
        
    def shorepassRighe(self,bc):
        center = bc.contentPane(region='center',width='500px')#, datapath='shipsteps_shorepass_righe')
        
        center.inlineTableHandler(relation='@shorepass_righe',viewResource='ViewFromShorepassRighe', export=True)
        
    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_crewlist,*,10')
        btn_crewl_print=bar.stampa_crewlist.button('Print Crew List')

        btn_crewl_print.dataRpc('nome_temp', self.print_crewlist,record='=#FORM.record',
                                vessel_name='=#FORM.record.@arrival_id.@vessel_details_id.@imbarcazione_id.nome',nome_template = 'shipsteps.shorepass:crewlist',format_page='A4')

    @public_method
    def print_crewlist(self, record, resultAttr=None, nome_template=None,vessel_name=None, format_page=None, **kwargs):
        record_id=record['id']
        
        tbl_shorepass = self.db.table('shipsteps.shorepass')
        builder = TableTemplateToHtml(table=tbl_shorepass)
        nome_nave = vessel_name.replace(' ', '_')
        nome_temp = nome_template.replace('shipsteps.crewlist:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id='crew_list_' + nome_nave)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        #builder(record=record_id, template=template)
        #if format_page=='A3':
        #    builder.page_format='A3'
        #    builder.page_width=427
        #    builder.page_height=290

        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
        letterhead=''       
        for r in range(len(templates)):
            if templates[r][1] == 'A4_orizz':
                letterhead = templates[r][0]    
            if format_page=='A3':
                if templates[r][1] == 'A3_orizz':
                    letterhead = templates[r][0]
          
        builder(record=record_id, template=template,letterhead_id=letterhead)

        result = builder.writePdf(pdfpath=pdfpath)
            
        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
