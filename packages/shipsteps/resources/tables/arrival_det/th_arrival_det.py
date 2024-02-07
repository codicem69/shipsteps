#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('draft_aft_arr')
        r.fieldcell('draft_fw_arr')
        r.fieldcell('draft_aft_dep')
        r.fieldcell('draft_fw_dep')
        r.fieldcell('tug_in')
        r.fieldcell('tug_out')
        r.fieldcell('ifo_arr')
        r.fieldcell('do_arr')
        r.fieldcell('lo_arr')
        r.fieldcell('fw_arr')
        r.fieldcell('ifo_dep')
        r.fieldcell('do_dep')
        r.fieldcell('lo_dep')
        r.fieldcell('fw_dep')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        rg_details = bc.roundedGroup(title='!![en]Arrival details',region = 'left',datapath='.record', width='30%', height = '100%', splitter=True).div(margin='10px',margin_left='2px')
        rg_details_dep = bc.roundedGroup(title='!![en]Departure details',region='center',datapath='.record',width='30%', height = '100%').div(margin='10px',margin_left='2px')
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        div_draft=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>DRAFT</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_draft.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('draft_aft_arr',placeholder='e.g. 4,5')
        fb.field('draft_fw_arr',placeholder='e.g. 4,5')
   
        div_draft=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>DRAFT</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_draft.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('draft_aft_dep',placeholder='e.g. 4,5')
        fb.field('draft_fw_dep',placeholder='e.g. 4,5')

        div_rem=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>REMAINS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_rem.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('ifo_arr',placeholder='e.g. mt.50')
        fb.field('do_arr',placeholder='e.g. mt.50')
        fb.field('lo_arr',placeholder='e.g. kgs.50')

        div_rem=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>REMAINS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_rem.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('ifo_dep',placeholder='e.g. mt.50')
        fb.field('do_dep',placeholder='e.g. mt.50')
        fb.field('lo_dep',placeholder='e.g. kgs.50')

        div_fw=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>FRESH WATER</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_fw.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('fw_arr',placeholder='e.g. mt.50')
 
        div_fw=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>FRESH WATER</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_fw.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('fw_dep',placeholder='e.g. mt.50')

        div_tug=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>USED TUGS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_tug.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('tug_in',placeholder='e.g. 1')
     
        div_tug=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>USED TUGS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_tug.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('tug_out',placeholder='e.g. 1')
        
        #fb = rg_details.formbuilder(cols=2, border_spacing='4px')
#
        #fb.field('arrival_id' )
        #fb.field('draft_aft_arr' )
        #fb.field('draft_fw_arr' )
        #fb.field('draft_aft_dep' )
        #fb.field('draft_fw_dep' )
        #fb.field('tug_in' )
        #fb.field('tug_out' )
        #fb.field('ifo_arr' )
        #fb.field('do_arr' )
        #fb.field('lo_arr' )
        #fb.field('ifo_dep' )
        #fb.field('do_dep' )
        #fb.field('lo_dep' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
