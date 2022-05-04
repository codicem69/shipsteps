#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('sof_n',width='5em')
        r.fieldcell('nor_tend')
        r.fieldcell('nor_rec')
        r.fieldcell('nor_acc')
        r.fieldcell('ops_commenced')
        r.fieldcell('ops_completed')
        r.fieldcell('doc_onboard')
        r.fieldcell('ship_rec', width='40em')
        r.fieldcell('intestazione_sof')
        
    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class ViewFromSof(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('sof_n',width='3em')
        r.fieldcell('nor_tend', edit=True)
        r.fieldcell('nor_rec', edit=True)
        r.fieldcell('nor_acc', edit=True)
        r.fieldcell('ops_commenced', edit=True)
        r.fieldcell('ops_completed', edit=True)
        r.fieldcell('doc_onboard', edit=True)
        r.fieldcell('ship_rec')
        r.fieldcell('intestazione_sof', edit=True)

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('sof_n')
        fb.field('nor_tend')
        fb.field('nor_rec')
        fb.field('nor_acc')
        fb.field('ops_commenced')
        fb.field('ops_completed')
        fb.field('doc_onboard')
        fb.field('int_sof')
        

class FormSof(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiSof(bc.roundedGroupFrame(title='Dati SOF',region='top',datapath='.record',height='110px', background='lightgrey', splitter=True))
        tc = bc.tabContainer(region = 'center',margin='2px')
        
        self.cargoSof(tc.contentPane(title='Cargo SOF'))
        self.operationsSof(tc.contentPane(title='SOF Operations'))

        tc_rem = tc.tabContainer(title='!![en]Remarks',margin='2px',tabPosition='left-h')#, region='center', height='450px', splitter=True)
        
        self.remarks_rs(tc_rem.contentPane(title='Receivers/Shippers Remarks',datapath='.record'))
        self.remarks_cte(tc_rem.contentPane(title='Master Remarks',datapath='.record'))
        self.remarks_note(tc_rem.contentPane(title='Note Remarks',datapath='.record'))
        self.onbehalf_remarks(tc_rem.contentPane(title='!![en]On behalf Sippers/Receivers',datapath='.record'))

        tc_tanks = tc.tabContainer(title='!![en]Tank times',margin='2px')
        self.tanks(tc_tanks.contentPane(title='Time tanks'))
        self.emailSof(tc.contentPane(title='Email SOF'))
        self.editSof(tc.framePane(title='Edit SOF', datapath='#FORM.editPagine'))
        self.Sofpdf(tc.framePane(title='SOF pdf', datapath='#FORM.pdf'))

    def datiSof(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        #fb.field('arrival_id')
        fb.field('sof_n', readOnly=True)
        fb.field('nor_tend')
        fb.field('nor_rec')
        fb.field('nor_acc')
        fb.field('ops_commenced')
        fb.field('ops_completed')
        fb.field('doc_onboard')
        fb.field('ship_rec', readOnly=True, width='30em',height='2em',colspan=2, tag='textArea')
        fb.field('int_sof')
        
    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_sof,20,email_arrivo,*,10')
        btn_sof_print=bar.stampa_sof.button('Print SOF')
        btn_sof_arrivo=bar.email_arrivo.button('Email arrival')
        btn_sof_print.dataRpc('msg_special', self.print_sof,record='=#FORM.record',nome_template = 'shipsteps.sof:sof',format_page='A4')
        btn_sof_arrivo.dataRpc('msg_special', self.email_sof_arrival,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_rinfusa_cp',
                            nome_template = 'shipsteps.rinfusa:bulk_app',format_page='A4')
    
    @public_method
    def print_sof(self, record, resultAttr=None, nome_template=None, format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_sof = self.db.table('shipsteps.sof')
        builder = TableTemplateToHtml(table=tbl_sof)

        nome_temp = nome_template.replace('shipsteps.sof:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        #builder(record=selId, template=template)
        builder(record=record_id, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)

    def email_sof_arrival(self):
        pass

    def cargoSof(self,pane):
        pane.inlineTableHandler(relation='@sof_cargo_sof',viewResource='ViewFromSof_Cargo',
                                picker='cargo_unl_load_id',
                                picker_condition='arrival_id=:aid',
                                picker_condition_aid='^#FORM.record.arrival_id',
                                picker_viewResource='ViewFromCargoLU_picker')

    def operationsSof(self,pane):
        pane.inlineTableHandler(relation='@sof_operations',viewResource='ViewFromSofOperations')

    

    def remarks_cte(self,frame):
        frame.simpleTextArea(title='!![en]Master Remarks',value='^.remarks_cte',editor=True)

    def remarks_note(self,frame):
        frame.simpleTextArea(title='!![en]Note / General Remarks',value='^.note',editor=True)

    def remarks_rs(self,frame):
        
        fb = frame.formbuilder(cols=1, border_spacing='4px',fld_width='50em', width='800px')
        fb.simpleTextArea(value='^.remarks_rs',editor=True, height='200px')
        fb.br()
        fb.button('Inserisci',lbl='Remark Wheat/Corn',action="""SET ^.remarks_rs = note_remark;
                                            alert("Inserito - Ricordati di salvare");""",
                    note_remark='=gnr.app_preference.shipsteps.remarks_wheat_corn')
    
    def onbehalf_remarks(self,frame):
        frame.simpleTextArea(value='^.onbehalf',editor=True)

    def tanks(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=2, border_spacing='4px',fld_width='10em',table='shipsteps.sof_tanks',datapath='.record.@sof_tanks')
        fb.field('start_insp')
        fb.field('stop_insp')
        fb.field('cargo_calc')
        fb.br()
        fb.field('start_ullage')
        fb.field('stop_ullage')
        fb.field('hose_conn')
        fb.field('hose_disconn')
        fb.field('average')

    def emailSof(self,pane):
        pane.inlineTableHandler(title='Email SOF', relation='@sof_email',viewResource='ViewFromSofEmail')

    def editSof(self, frame):
        bar = frame.top.slotBar('10, lett_select,*',height='20px',border_bottom='1px solid silver')
        fb = bar.lett_select.formbuilder(cols=2,datapath='#FORM.record.htmlbag')
        fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
        fb.button('Get Html Doc').dataRpc('#FORM.record.htmlbag.source',self.db.table('shipsteps.sof').getHTMLDoc,
                                            sof_id='=#FORM.pkey',
                                            record_template='sof',
                                            letterhead='.letterhead_id')
        
        frame.pagedEditor(value='^#FORM.record.htmlbag.source',pagedText='^#FORM.record.htmlbag.output',
                          border='1px solid silver',
                          letterhead_id='^#FORM.record.htmlbag.letterhead_id',
                          datasource='#FORM.record',printAction=True)
    def Sofpdf(self,frame):
        self.printDisplay(frame,resource='shipsteps.sof:html_res/sof_template')

    def printDisplay(self, frame, resource=None, html=None):
        bar = frame.top.slotBar('10,lett_select,*', height='20px', border_bottom='1px solid silver')
        bar.lett_select.formbuilder().dbselect('^.curr_letterhead_id',
                                                table='adm.htmltemplate',
                                                lbl='Carta intestata',
                                                hasDownArrow=True)
        frame.documentFrame(resource=resource,
                            pkey='^#FORM.pkey',
                            html=html,
                            letterhead_id='^.curr_letterhead_id',
                            missingContent='NO SOF',
                          _if='pkey',_delay=100)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
