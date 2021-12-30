#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('vessel_name')
        r.fieldcell('ad_place')
        r.fieldcell('ad_date')
        r.fieldcell('ad_date_exp')
        r.fieldcell('adovt_place')
        r.fieldcell('adovt_date')
        r.fieldcell('adovt_date_exp')
        r.fieldcell('saf_eq_pass_place')
        r.fieldcell('saf_eq_pass_date')
        r.fieldcell('saf_eq_pass_exp')
        r.fieldcell('saf_eq_pass_place_last')
        r.fieldcell('saf_eq_pass_place_lastdate')
        r.fieldcell('saf_eq_place')
        r.fieldcell('saf_eq_date')
        r.fieldcell('saf_eq_exp')
        r.fieldcell('saf_eq_place_last')
        r.fieldcell('saf_eq_place_lastdate')
        r.fieldcell('saf_rt_place')
        r.fieldcell('saf_rt_date')
        r.fieldcell('saf_rt_exp')
        r.fieldcell('saf_rt_place_last')
        r.fieldcell('saf_rt_place_lastdate')
        r.fieldcell('loadline_place')
        r.fieldcell('loadline_date')
        r.fieldcell('loadline_exp')
        r.fieldcell('loadline_place_last')
        r.fieldcell('loadline_place_lastdate')
        r.fieldcell('sanitation_place')
        r.fieldcell('sanitation_date')
        r.fieldcell('sanitation_exp')
        r.fieldcell('issc_place')
        r.fieldcell('issc_date')
        r.fieldcell('issc_exp')
        r.fieldcell('issc_place_lastdate')
        r.fieldcell('doc_place')
        r.fieldcell('doc_date')
        r.fieldcell('doc_exp')
        r.fieldcell('doc_place_lastdate')
        r.fieldcell('smc_place')
        r.fieldcell('smc_date')
        r.fieldcell('smc_exp')
        r.fieldcell('smc_place_lastdate')
        r.fieldcell('iopp_place')
        r.fieldcell('iopp_date')
        r.fieldcell('iopp_exp')
        r.fieldcell('iopp_place_last')
        r.fieldcell('iopp_place_lastdate')
        r.fieldcell('pmou_place')
        r.fieldcell('pmou_date')
        r.fieldcell('msm_place')
        r.fieldcell('msm_date')
        r.fieldcell('msm_exp')
        r.fieldcell('msm_place_lastdate')
        r.fieldcell('class_place')
        r.fieldcell('class_date')
        r.fieldcell('class_exp')
        r.fieldcell('noteclass')
        r.fieldcell('ido_place')
        r.fieldcell('ido_date')
        r.fieldcell('ido_exp')
        r.fieldcell('noteido')
        r.fieldcell('ts_place')
        r.fieldcell('ts_date')
        r.fieldcell('ts_exp')
        r.fieldcell('notets')
        r.fieldcell('sb_place')
        r.fieldcell('sb_date')
        r.fieldcell('sb_exp')
        r.fieldcell('notesb')
        r.fieldcell('ass_place')
        r.fieldcell('ass_date')
        r.fieldcell('ass_exp')
        r.fieldcell('noteass')
        r.fieldcell('ruolo_num')
        r.fieldcell('ruolo_serie')
        r.fieldcell('ruolo_place')
        r.fieldcell('ruolo_date')
        r.fieldcell('noteruolo')
        r.fieldcell('speed_dich')
        r.fieldcell('speed_eff')

    def th_order(self):
        return 'vessel_name'

    def th_query(self):
        return dict(column='vessel_name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        
        self.InternationalDoc(bc.borderContainer(region='top',datapath='.record',height='135px', splitter=True))
        self.InternationalDoc2(bc.borderContainer(region='center',datapath='.record', splitter=True, background = 'lavenderblush'))
        #self.ItalianDoc(bc.borderContainer(region='bottom',datapath='.record',height='315px', splitter=True, background = 'beige'))
       # pane = form.record

    def InternationalDoc(self, bc):
        left = bc.roundedGroup(region='left', title='Vessel details', width='32%',background='lightyellow').div(margin='10px',margin_right='20px')
        center= bc.roundedGroup(region='center',title='Italian Anchorage Dues', width='34%').div(margin='10px',margin_right='20px')
        right= bc.roundedGroup(region='right',title='Safety Equipment Passenger', width='34%',background='lavenderblush').div(margin='10px',margin_right='20px')
        fbl = left.formbuilder(cols=2, border_spacing='4px')
        fbc = center.formbuilder(cols=2, border_spacing='4px')
        fbr = right.formbuilder(cols=2, border_spacing='4px')           
       # fb = pane.formbuilder(cols=4, border_spacing='4px')
        fbl.field('vessel_name', lbl = 'Name')
        fbl.field('bandiera')
        fbl.field('imo')
        fbl.br()
        fbl.field('gt')
        fbl.field('nt')
        fbl.field('loa') 

        fbc.field('ad_place', lbl = 'Issued at', width = '10em')
        fbc.field('ad_date', lbl = 'Issued date', width = '10em')
        fbc.field('ad_date_exp', lbl = 'Expire date', width = '10em')
        fbc.br()
        fbc.field('adovt_place', lbl = 'Overdues issued at', width = '10em')
        fbc.field('adovt_date', lbl = 'Overdues date', width = '10em')
        fbc.field('adovt_date_exp', lbl = 'Overdues Expire date', width = '10em')

        fbr.field('saf_eq_pass_place', lbl = 'Issued at', width = '10em')
        fbr.field('saf_eq_pass_date', lbl = 'Issued date', width = '10em')
        fbr.field('saf_eq_pass_exp', lbl = 'Expire date', width = '10em')
        fbr.br()
        fbr.field('saf_eq_pass_place_last', lbl = 'Last survey at', width = '10em')
        fbr.field('saf_eq_pass_place_lastdate', lbl = 'Last survey date', width = '10em')
    
    def InternationalDoc2(self, bc):
        #left = bc.roundedGroup(region='left', title='Doc. details', width='32%', height = '50%',margin_left='120px').div(margin='5px',margin_left='5px')
        #left2 = bc.roundedGroup(region='left', title='prova', width='22%', height = '30%',margin_top='200px').div(margin='10px',margin_right='10px')
        center= bc.roundedGroup(region='center',title='Safety Equipment', width='25%', height = '100px').div(margin='1px',margin_left='1px')
        center2= bc.roundedGroup(region='center',title='Safety Radio', width='25%', height = '100px', margin_left='25%').div(margin='1px',margin_left='1px')
        center3= bc.roundedGroup(region='center',title='Load Line', width='25%', height = '100px', margin_left='50%').div(margin='1px',margin_left='1px')
        center4= bc.roundedGroup(region='center',title='Sanitation', width='25%', height = '80px', margin_top='100px').div(margin='1px',margin_left='1px')
        center5= bc.roundedGroup(region='center',title='International ship security cert.', width='25%', height = '80px', margin_top='100px', margin_left='25%').div(margin='1px',margin_left='1px')
        center6= bc.roundedGroup(region='center',title='Document of Compliance', width='25%', height = '80px', margin_top='100px', margin_left='50%').div(margin='1px',margin_left='1px')
        center7= bc.roundedGroup(region='center',title='Safety Managment cert.', width='25%', height = '100px', margin_top='180px').div(margin='1px',margin_left='1px')
        center8= bc.roundedGroup(region='center',title='International Oil Prevention Pollution', width='25%', height = '100px', margin_top='180px', margin_left='25%').div(margin='1px',margin_left='1px')
        center9= bc.roundedGroup(region='center',title='Minimum Safe Manning doc.', width='25%', height = '100px', margin_top='180px', margin_left='50%').div(margin='1px',margin_left='1px')
        center10= bc.roundedGroup(region='center',title='Paris Mou', width='20%', height = '100px', margin_left='75%').div(margin='1px',margin_left='1px')
        center11= bc.roundedGroup(region='center',title='Ships speed', width='20%', height = '80px', margin_top='100px', margin_left='75%').div(margin='1px',margin_left='1px')
        center12= bc.roundedGroup(region='center',title='Certificato di Classe', width='25%', height = '100px', margin_top='300px',background='lightcyan').div(margin='1px',margin_left='1px')  
        center13= bc.roundedGroup(region='center',title="Certificato d'Idoneità", width='25%', height = '100px', margin_top='300px',margin_left='25%',background='lightcyan').div(margin='1px',margin_left='1px')  
        center14= bc.roundedGroup(region='center',title="Tecnico Sanitaria", width='25%', height = '100px', margin_top='300px',margin_left='50%',background='lightcyan').div(margin='1px',margin_left='1px')  
        center15= bc.roundedGroup(region='center',title="Servizi di Bordo", width='25%', height = '100px', margin_top='300px',margin_left='75%',background='lightcyan').div(margin='1px',margin_left='1px')  
        center16= bc.roundedGroup(region='center',title='Assicurazione', width='25%', height = '100px', margin_top='400px',background='lightcyan').div(margin='1px',margin_left='1px')  
        center17= bc.roundedGroup(region='center',title='Ruolo', width='25%', height = '100px', margin_top='400px',margin_left='25%',background='lightcyan').div(margin='1px',margin_left='1px')  
        #right= bc.roundedGroup(region='right',title='Doc. Details', width='34%').div(margin='10px',margin_right='20px')
        #fbl = left.formbuilder(cols=2, border_spacing='4px')
        #fbl2 = left2.formbuilder(cols=2, border_spacing='4px')
        fb_se = center.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_sr = center2.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_ll = center3.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_san = center4.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_issc = center5.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_doc = center6.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_smc = center7.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_iopp = center8.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_msm = center9.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_pm = center10.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_speed = center11.formbuilder(cols=1, border_spacing='4px', fld_width='10em')
        fb_class = center12.formbuilder(cols=2, border_spacing='4px', fld_width='10em') 
        fb_ido = center13.formbuilder(cols=2, border_spacing='4px', fld_width='10em') 
        fb_tc = center14.formbuilder(cols=2, border_spacing='4px', fld_width='10em') 
        fb_sb = center15.formbuilder(cols=2, border_spacing='4px', fld_width='10em')
        fb_ass = center16.formbuilder(cols=2, border_spacing='4px', fld_width='10em') 
        fb_ruolo = center17.formbuilder(cols=2, border_spacing='4px', fld_width='10em') 
        #fbr = right.formbuilder(cols=2, border_spacing='4px')  
       #fbl.div('Safety Equipment',width='450px',height = '175px', margin='auto',
       #         padding='1px',
       #         border='1px solid silver',rounded='1',
       #         margin_top='2px',shadow='1px 1px 2px #666')
        fb_se.field('saf_eq_place',lbl = 'Issued at')
        fb_se.field('saf_eq_date', lbl = 'Issued date', width='5em')
        fb_se.field('saf_eq_exp', lbl = 'Expire date')
        fb_se.br()
        fb_se.field('saf_eq_place_last', lbl = 'Last survey at')
        fb_se.field('saf_eq_place_lastdate', lbl = 'Last survey date', width='5em')
        fb_sr.field('saf_rt_place', lbl = 'Issued at')
        fb_sr.field('saf_rt_date',lbl='Issued date', width='5em')
        fb_sr.field('saf_rt_exp',lbl='Expire date')
        fb_sr.br()
        fb_sr.field('saf_rt_place_last',lbl='Last survey at')
        fb_sr.field('saf_rt_place_lastdate', lbl='Last survey date', width='5em')
        fb_ll.field('loadline_place', lbl='Issued at')
        fb_ll.field('loadline_date', lbl='Issued date', width='5em')
        fb_ll.field('loadline_exp', lbl='Expire date')
        fb_ll.br()
        fb_ll.field('loadline_place_last',lbl='Last survey at')
        fb_ll.field('loadline_place_lastdate', lbl='Last survey date', width='5em')
        fb_san.field('sanitation_place',lbl='Issued at')
        fb_san.field('sanitation_date', lbl='Issued date', width='5em')
        fb_san.field('sanitation_exp', lbl='Expire date')
        fb_issc.field('issc_place', lbl='Issued at')
        fb_issc.field('issc_date', lbl='Issued date', width='5em')
        fb_issc.field('issc_exp', lbl='Expire date')
        fb_issc.field('issc_place_lastdate', lbl='Last survey date', width='5em')
        fb_doc.field('doc_place', lbl='Issued at')
        fb_doc.field('doc_date', lbl='Issued date', width='5em')
        fb_doc.field('doc_exp', lbl='Expire date')
        fb_doc.field('doc_place_lastdate', lbl='Last survey date', width='5em')
        fb_smc.field('smc_place', lbl='Issued at')
        fb_smc.field('smc_date', lbl='Issued date', width='5em')
        fb_smc.field('smc_exp', lbl='Expire date')
        fb_smc.field('smc_place_lastdate', lbl='Last survey date', width='5em')
        fb_iopp.field('iopp_place',lbl='Issued at')
        fb_iopp.field('iopp_date', lbl='Issued date', width='5em')
        fb_iopp.field('iopp_exp', lbl='Expire date')
        fb_iopp.br()
        fb_iopp.field('iopp_place_last', lbl='Last survey at')
        fb_iopp.field('iopp_place_lastdate', lbl='Last survey date', width='5em')
        fb_msm.field('msm_place',lbl='Issued at')
        fb_msm.field('msm_date',lbl='Issued date', width='5em')
        fb_msm.field('msm_exp',lbl='Expire date')
        fb_msm.field('msm_place_lastdate',lbl='Last survey date', width='5em')
        fb_pm.field('pmou_place', lbl='Issued at', width='5em')
        fb_pm.field('pmou_date', lbl='Issued date', width='5em')
        fb_speed.field('speed_dich', lbl= 'Declared')
        fb_speed.field('speed_eff', lbl='Effective')
        bc.div('Concerning Italian Ship only',region='center',width='auto',height = '15px', margin='1px',
                padding='1px',align='center',background='navy',
                border='1px solid silver',rounded='1',
                margin_top='280px',style="color:white;")#,shadow='1px 1px 2px #666')
        
        fb_class.field('class_place', lbl='Issued at')
        fb_class.field('class_date', lbl='Issued date', width='5em')
        fb_class.field('class_exp',lbl='Expire date')
        fb_class.br()
        fb_class.field('noteclass', lbl='Note',colspan=2, width='23em')
        fb_ido.field('ido_place',lbl='Issued at')
        fb_ido.field('ido_date',lbl='Issued date', width='5em')
        fb_ido.field('ido_exp',lbl='Expire date')
        fb_ido.br()
        fb_ido.field('noteido', lbl='Note',colspan=2, width='23em')
        fb_tc.field('ts_place',lbl='Issued at')
        fb_tc.field('ts_date',lbl='Issued date', width='5em')
        fb_tc.field('ts_exp',lbl='Expire date')
        fb_tc.br()
        fb_tc.field('notets',lbl='Note',colspan=2, width='23em')
        fb_sb.field('sb_place',lbl='Issued at')
        fb_sb.field('sb_date',lbl='Issued date', width='5em')
        fb_sb.field('sb_exp',lbl='Expire date')
        fb_sb.br()
        fb_sb.field('notesb',lbl='Note',colspan=2, width='23em')
        fb_ass.field('ass_place', lbl='Issued at')
        fb_ass.field('ass_date', lbl='Issued date', width='5em')
        fb_ass.field('ass_exp',lbl='Expire date')
        fb_ass.br()
        fb_ass.field('noteass', lbl='Note',colspan=2, width='23em')
        fb_ruolo.field('ruolo_num', lbl='Ruolo n.')
        fb_ruolo.field('ruolo_serie', lbl = 'Serie', width='5em')
        fb_ruolo.field('ruolo_place', lbl = 'Issued at')
        fb_ruolo.field('ruolo_date', lbl = 'Issued date', width='5em')
        fb_ruolo.field('noteruolo', lbl='Note',colspan=2, width='23em')
       
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
