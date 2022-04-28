#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id')
        r.fieldcell('date')
        r.fieldcell('day')
        r.fieldcell('operations')
        r.fieldcell('from')
        r.fieldcell('to')

    def th_order(self):
        return 'sof_id'

    def th_query(self):
        return dict(column='sof_id', op='contains', val='')

class ViewFromSofOperations(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('date',edit=True)
        r.fieldcell('day',edit=True)
        r.fieldcell('operations',edit=True, width='40em')
        r.fieldcell('from',edit=True, width='5em')
        r.fieldcell('to',edit=True, width='5em')
    
    def th_order(self):
        return 'date'

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id')
        fb.field('date')
        fb.field('day')
        fb.field('operations',width='30em')
        fb.field('from')
        fb.field('to')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='800px')
