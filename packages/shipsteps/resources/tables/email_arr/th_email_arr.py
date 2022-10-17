#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('dest')
        r.fieldcell('description')
        r.fieldcell('email')
        r.fieldcell('email_type')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromEmailArrival(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
       # r.fieldcell('arrival_id')
        r.fieldcell('dest', width='10em',edit=True)
        r.fieldcell('description', width='30em',edit=True)
        r.fieldcell('email',  edit=dict(validate_notnull=True), width='20em')
        r.fieldcell('email_type', edit=dict(validate_notnull=True))


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('dest' )
        fb.field('description' )
        fb.field('email' )
        fb.field('email_type' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
