#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id', width='7em')
        r.fieldcell('reference_num', width='7em')
        r.fieldcell('date')
        r.fieldcell('vessel_details_id', width='15em')
        r.fieldcell('eta', width='5em')
        r.fieldcell('etb', width='5em')
        r.fieldcell('et_start', width='5em')
        r.fieldcell('etc', width='5em')
        r.fieldcell('ets', width='5em')
        r.fieldcell('draft_aft_arr', width='5em')
        r.fieldcell('draft_fw_arr', width='5em')
        r.fieldcell('draft_aft_dep', width='5em')
        r.fieldcell('draft_fw_dep', width='5em')
        r.fieldcell('mandatory')
        r.fieldcell('dock_id', width='5em')
        r.fieldcell('info_moor')
        r.fieldcell('master_name')
        r.fieldcell('n_crew', width='5em')
        r.fieldcell('n_passengers', width='5em')
        r.fieldcell('last_port', width='7em')
        r.fieldcell('departure_lp', width='5em')
        r.fieldcell('next_port', width='7em')
        r.fieldcell('eta_np', width='5em')
        r.fieldcell('cargo_dest')
        r.fieldcell('invoice_det_id', width='40em')
        #r.fieldcell('@gpg_id.date_start')

    def th_order(self):
        return 'agency_id'

    def th_query(self):
        return dict(column='reference_num', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        bc = form.center.borderContainer()
        bc_top = bc.borderContainer(region='top',height='300px', splitter=True,datapath='.record')
        self.datiArrivo(bc_top)
        tc = bc.tabContainer(margin='2px',region='center')
        #tc_r = bc_top.tabContainer(margin='2px', region='right', width='25%')#, width='25%', splitter=True)
        #self.gpg(tc_r.contentPane(title='!![en]GPG'))
        self.gpg(bc_top)#.contentPane(title='!![en]GPG'))
        self.datiCarico(tc.contentPane(title='!![en]Cargo loading / unloading'))
        self.datiCaricoTransit(tc.contentPane(title='!![en]Transit cargo'))
        self.car_ric(tc.contentPane(title='!![en]Shippers / Receivers'))

    def datiArrivo(self,bc):
        left = bc.roundedGroup(region='left', title='!![en]Vessel arrival', width='13%', splitter=True).div(margin='10px',margin_right='20px')
        fb = left.formbuilder(cols=1, border_spacing='4px',lblpos='T')   
        fb.field('agency_id', readOnly=True )
        fb.field('reference_num', readOnly=True)
        fb.field('date')
        fb.field('vessel_details_id' )
        center = bc.roundedGroup(region='center', title='!![en]Arrival details', width='62%', splitter=True).div(margin='10px',margin_right='20px')
        fb = center.formbuilder(cols=5, border_spacing='4px',lblpos='T',fldalign='left')   
       
        fb.field('eta' , width='10em')
        fb.field('etb' , width='10em')
        fb.field('et_start' , width='10em')
        fb.field('etc' , width='10em')
        fb.field('ets', width='10em' )
        fb.field('draft_aft_arr', width='5em' )
        fb.field('draft_fw_arr' , width='5em')
        fb.field('draft_aft_dep' , width='5em')
        fb.field('draft_fw_dep' , width='5em')
        
        fb.field('dock_id' )
        fb.field('info_moor',width='30em', colspan=2 )
        fb.field('master_name' )
        fb.field('n_crew' , width='5em')
        fb.field('n_passengers' , width='5em')
        fb.br()
        fb.field('last_port',auxColumns='@nazione_code.nome' )
        fb.field('departure_lp' , width='5em')
        fb.field('next_port',auxColumns='@nazione_code.nome' )
        fb.field('eta_np' , width='5em')
        fb.br()
        fb.field('mandatory', colspan=2 , width='30em')
        fb.field('cargo_dest', colspan=2, width='30em' )
        fb.br()
        fb.field('invoice_det_id',colspan=5 ,width='80em', hasDownArrow=True)

        #tc_r = bc.tabContainer(margin='2px', region='right', width='25%', splitter=True)
        #self.gpg(tc_r.contentPane(title='!![en]GPG'))

    def datiCarico(self,pane):
        pane.inlineTableHandler(relation='@cargo_lu_arr',viewResource='ViewFromCargoLU')

    def datiCaricoTransit(self,pane):
        pane.inlineTableHandler(relation='@cargo_transit_arr',viewResource='ViewFromCargoTransit')

    def car_ric(self,pane):
        pane.dialogTableHandler(table='shipsteps.ship_rec',view_store_onStart=True,export=True)

    def gpg(self,pane):
       # pane.inlineTableHandler(relation='@gpg_arr')#,viewResource='ViewFromCargoLU')
        right = pane.roundedGroup(region='right', title='!![en]Special security guards',table='shipsteps.gpg',datapath='.@gpg_arr', width='25%').div(margin='10px',margin_right='20px')
        fb = right.formbuilder(cols=1, border_spacing='4px')
        #fb.field('arrival_id')
        fb.field('date_start')
        fb.field('date_end')
        fb.field('n_gpg')
        #pass
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
