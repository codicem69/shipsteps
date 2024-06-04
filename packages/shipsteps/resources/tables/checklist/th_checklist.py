#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('movtype_id')
        r.fieldcell('description', width='auto')

    def th_order(self):
        return '@movtype_id.hierarchical_descrizione:a'

    def th_query(self):
        return dict(column='movtype_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px',colswidth='auto',fld_width='100%')
        fb.field('movtype_id', hasDownArrow=True, width='20em' )
        fb.field('description', tag='simpleTextArea', editor=True, width='100%', height='50em' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
