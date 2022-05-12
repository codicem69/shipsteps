#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('bunker_id')
        r.fieldcell('prodotto')
        r.fieldcell('quantity')
        r.fieldcell('zolfo')
        r.fieldcell('punto_infiam')
        r.fieldcell('denaturato')

    def th_order(self):
        return 'bunker_id'

    def th_query(self):
        return dict(column='bunker_id', op='contains', val='')

class ViewFromBunkerRighe(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('bunker_id')
        r.fieldcell('prodotto', edit=dict(validate_notnull=True))
        r.fieldcell('quantity', edit=dict(validate_notnull=True))
        r.fieldcell('zolfo', edit=dict(validate_notnull=True))
        r.fieldcell('punto_infiam', edit=dict(validate_notnull=True))
        r.fieldcell('denaturato', edit=dict(validate_notnull=True))


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('bunker_id')
        fb.field('prodotto')
        fb.field('quantity')
        fb.field('zolfo')
        fb.field('punto_infiam')
        fb.field('denaturato')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
