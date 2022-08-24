#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent


class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
       # r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('name', width='50em')
        r.fieldcell('address', width='50em')
        r.fieldcell('city', width='50em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

class ViewFromCharterers(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('name', width='50em', edit=True)
        r.fieldcell('address', width='50em', edit=True)
        r.fieldcell('city', width='50em', edit=True)
    
    def th_order(self):
        return 'name'

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px', fld_width='60em')
        fb.field('name')
        fb.field('address')
        fb.field('city')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
