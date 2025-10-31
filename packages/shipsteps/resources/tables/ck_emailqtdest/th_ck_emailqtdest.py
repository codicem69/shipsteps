#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id', hidden=True)
        r.fieldcell('issued_date')
        r.fieldcell('user')
        r.fieldcell('send_date')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('issued_date' )
        fb.field('user' )
        fb.field('send_date' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
