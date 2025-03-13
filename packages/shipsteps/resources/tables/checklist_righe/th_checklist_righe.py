#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('checklist_id')
        r.fieldcell('description')

    def th_order(self):
        return 'checklist_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromRighe(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('checklist_id')
        r.fieldcell('description', edit=True,width='100%')

    def th_order(self):
        return '_row_count'

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('delrow','importer,batchAssign,delrow')
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('checklist_id' )
        fb.field('description' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
