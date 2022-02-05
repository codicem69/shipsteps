#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id')
        r.fieldcell('consignee')
        r.fieldcell('email')
        r.fieldcell('email_cc')
        r.fieldcell('port')

    def th_order(self):
        return 'consignee'

    def th_query(self):
        return dict(column='consignee', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('agency_id', width='10em')
        fb.field('consignee', width='40em')
        fb.div("!![en]Insert the emails separate by commas", margin_top='10px')
        fb.field('email',width='40em', height='10em')
        fb.div(' ')
        fb.div("!![en]Insert the emails separate by commas", margin_top='10px')
        fb.field('email_cc',width='40em', height='10em')
        fb.field('port')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
