#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', width='50em')
        r.fieldcell('address', width='50em')
        r.fieldcell('city', width='50em')
        r.fieldcell('extra', width='30em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px', fld_width='60em')
        fb.field('name')
        fb.field('address')
        fb.field('city')
        fb.field('extra')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
