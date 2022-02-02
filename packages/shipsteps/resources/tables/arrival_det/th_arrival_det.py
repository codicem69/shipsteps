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
        r.fieldcell('ifo_dep')
        r.fieldcell('do_dep')
        r.fieldcell('lo_dep')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('draft_aft_arr' )
        fb.field('draft_fw_arr' )
        fb.field('draft_aft_dep' )
        fb.field('draft_fw_dep' )
        fb.field('tug_in' )
        fb.field('tug_out' )
        fb.field('ifo_arr' )
        fb.field('do_arr' )
        fb.field('lo_arr' )
        fb.field('ifo_dep' )
        fb.field('do_dep' )
        fb.field('lo_dep' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
