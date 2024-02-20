#!/usr/bin/python3
# -*- coding: utf-8 -*-

from turtle import width
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('own_name', width='45em')
        r.fieldcell('address_own', width='auto')

    def th_order(self):
        return 'own_name'

    def th_query(self):
        return dict(column='own_name', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('own_name', width='50em')
        fb.field('address_own', width='50em')


    def th_options(self):
        return dict(dialog_windowRatio = 1)
