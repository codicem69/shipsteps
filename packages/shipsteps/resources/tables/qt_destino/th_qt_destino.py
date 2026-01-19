#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('dailysof_id')
        r.fieldcell('wharehouse_id')
        r.fieldcell('tot_xdate')

    def th_order(self):
        return 'dailysof_id'

    def th_query(self):
        return dict(column='tot_xdate', op='contains', val='')

class ViewFromDailyQTdest(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('dailysof_id', hidden=True)
        r.fieldcell('wharehouse_id', edit=True)
        r.fieldcell('tot_xdate',edit=True, totalize=True)

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='tot_xdate', op='contains', val='')

    def th_options(self):
        return dict(grid_selfDragRows=True)

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('dailysof_id' )
        fb.field('wharehouse_id' )
        fb.field('tot_xdate' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
