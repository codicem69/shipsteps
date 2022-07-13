#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('lavori')
        r.fieldcell('notizie')
        r.fieldcell('pilot_arr')
        r.fieldcell('pilot_arr_vhf')
        r.fieldcell('antifire_arr')
        r.fieldcell('antipol_arr')
        r.fieldcell('moor_arr')
        r.fieldcell('n_moor_arr')
        r.fieldcell('tug_arr')
        r.fieldcell('n_tug_arr')
        r.fieldcell('daywork')
        r.fieldcell('timework')
        r.fieldcell('pilot_dep')
        r.fieldcell('pilot_dep_vhf')
        r.fieldcell('antifire_dep')
        r.fieldcell('antipol_dep')
        r.fieldcell('moor_dep')
        r.fieldcell('n_moor_dep')
        r.fieldcell('tug_dep')
        r.fieldcell('n_tug_dep')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('lavori')
        fb.field('notizie')
        fb.field('pilot_arr')
        fb.field('pilot_arr_vhf')
        fb.field('antifire_arr')
        fb.field('antipol_arr')
        fb.field('moor_arr')
        fb.field('n_moor_arr')
        fb.field('tug_arr')
        fb.field('n_tug_arr')
        fb.field('daywork')
        fb.field('timework')
        fb.field('pilot_dep')
        fb.field('pilot_dep_vhf')
        fb.field('antifire_dep')
        fb.field('antipol_dep')
        fb.field('moor_dep')
        fb.field('n_moor_dep')
        fb.field('tug_dep')
        fb.field('n_tug_dep')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
