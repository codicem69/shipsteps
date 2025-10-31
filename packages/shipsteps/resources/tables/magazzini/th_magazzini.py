#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class LookupView(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('descrizione', edit=True, width='100%')

    def th_order(self):
        return 'descrizione'

    def th_query(self):
        return dict(column='descrizione', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('descrizione' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
