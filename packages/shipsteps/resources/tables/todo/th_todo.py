#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('title')
        r.fieldcell('description')
        r.fieldcell('due_date')
        r.fieldcell('done')
        r.fieldcell('remind_at')
        r.fieldcell('snooze_until')

    def th_order(self):
        return 'title'

    def th_query(self):
        return dict(column='title', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('title' )
        fb.field('description' )
        fb.field('due_date' )
        fb.field('done' )
        fb.field('remind_at' )
        fb.field('snooze_until' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

    