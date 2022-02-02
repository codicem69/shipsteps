#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id')
        r.fieldcell('start_insp')
        r.fieldcell('stop_insp')
        r.fieldcell('cargo_calc')
        r.fieldcell('start_ullage')
        r.fieldcell('stop_ullage')
        r.fieldcell('hose_conn')
        r.fieldcell('hose_disconn')
        r.fieldcell('average')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id' )
        fb.field('start_insp' )
        fb.field('stop_insp' )
        fb.field('cargo_calc' )
        fb.field('start_ullage' )
        fb.field('stop_ullage' )
        fb.field('hose_conn' )
        fb.field('hose_disconn' )
        fb.field('average' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
