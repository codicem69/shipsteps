#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id')
        r.fieldcell('dest')
        r.fieldcell('description')
        r.fieldcell('email_sof')
        r.fieldcell('email_type')

    def th_order(self):
        return 'sof_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromSofEmail(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('dest', edit=True, width='10em')
        r.fieldcell('description', edit=True, width='30em')
        r.fieldcell('email_sof',  edit=dict(validate_notnull=True), width='20em')
        r.fieldcell('email_type', edit=dict(validate_notnull=True))

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id' )
        fb.field('dest' )
        fb.field('description' )
        fb.field('email_sof' )
        fb.field('email_type' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
