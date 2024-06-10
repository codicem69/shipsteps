#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('garbage_id')
        r.fieldcell('tip_garbage_id')
        r.fieldcell('measure')
        r.fieldcell('quantity')

    def th_order(self):
        return 'garbage_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromGarbageDet(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tip_garbage_id', edit=True, width='20em', hasDownArrow=True)
        r.fieldcell('measure',edit=True, values='m3:m3',hasDownArrow=True)
        r.fieldcell('quantity',edit=True)

    def th_order(self):
        return 'garbage_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('garbage_id' )
        fb.field('tip_garbage_id' )
        fb.field('measure' )
        fb.field('quantity' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
