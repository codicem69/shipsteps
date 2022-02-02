#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('nor_tend')
        r.fieldcell('nor_rec')
        r.fieldcell('nor_acc')
        r.fieldcell('ops_commenced')
        r.fieldcell('ops_completed')
        r.fieldcell('doc_onboard')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class ViewFromSof(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('nor_tend', edit=True)
        r.fieldcell('nor_rec', edit=True)
        r.fieldcell('nor_acc', edit=True)
        r.fieldcell('ops_commenced', edit=True)
        r.fieldcell('ops_completed', edit=True)
        r.fieldcell('doc_onboard', edit=True)


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('nor_tend')
        fb.field('nor_rec')
        fb.field('nor_acc')
        fb.field('ops_commenced')
        fb.field('ops_completed')
        fb.field('doc_onboard')

class FormSof(BaseComponent):
    
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiSof(bc.roundedGroupFrame(title='Dati SOF',region='top',datapath='.record',height='80px', background='lightgrey'))
        tc = bc.tabContainer(region = 'center',margin='2px')
        
        self.cargoSof(tc.contentPane(title='Cargo SOF'))
        self.operationsSof(tc.contentPane(title='SOF Operations'))

        tc_rem = tc.tabContainer(title='!![en]Remarks',margin='2px',tabPosition='left-h')#, region='center', height='450px', splitter=True)
        
        self.remarks_rs(tc_rem.contentPane(title='Receivers/Shippers Remarks',datapath='.record'))
        self.remarks_cte(tc_rem.contentPane(title='Master Remarks',datapath='.record'))
        self.remarks_note(tc_rem.contentPane(title='Note Remarks',datapath='.record'))

        tc_tanks = tc.tabContainer(title='!![en]Tank times',margin='2px')
        self.tanks(tc_tanks.contentPane(title='Time tanks'))
        self.emailSof(tc.contentPane(title='Email SOF'))

    def datiSof(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        fb.field('arrival_id')
        fb.field('nor_tend')
        fb.field('nor_rec')
        fb.field('nor_acc')
        fb.field('ops_commenced')
        fb.field('ops_completed')
        fb.field('doc_onboard')

    def cargoSof(self,pane):
        pane.dialogTableHandler(relation='@sof_cargo_sof',viewResource='ViewFromSof_Cargo',
                                picker='cargo_unl_load_id')

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

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
