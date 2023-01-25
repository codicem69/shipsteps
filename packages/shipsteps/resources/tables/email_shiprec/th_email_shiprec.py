#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('email_sof_id')
        r.fieldcell('dest')
        r.fieldcell('description')
        r.fieldcell('email')
        r.fieldcell('email_type')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

class ViewFromEmailShiprec(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('dest', edit=True, width='10em')
        r.fieldcell('description', edit=True, width='30em')
        r.fieldcell('email',  edit=dict(validate_notnull=True), width='20em')
        r.fieldcell('email_type', edit=dict(validate_notnull=True))
    
    def th_order(self):
        return '_row_count'
        
    def th_query(self):
        return dict(column='_row_count', op='contains', val='')
    
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('#','#,importer')
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('_row_count')
        fb.field('email_sof_id')
        fb.field('dest')
        fb.field('description')
        fb.field('email')
        fb.field('email_type')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
