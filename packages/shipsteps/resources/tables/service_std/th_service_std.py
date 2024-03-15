#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class LookupView(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('services_id', edit=True, hasDownArrow=True, width='50em')
        r.fieldcell('descrizione', edit=True, hasDownArrow=True, width='50em')

    def th_order(self):
        return '@services_id.description'

    def th_query(self):
        return dict(column='services_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('services_id' )
        fb.field('descrizione' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )