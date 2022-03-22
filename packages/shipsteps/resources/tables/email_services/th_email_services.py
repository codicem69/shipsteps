#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id')
        r.fieldcell('service_for_email_id')
        r.fieldcell('consignee')
        r.fieldcell('email')
        r.fieldcell('email_cc')
        r.fieldcell('email_bcc')
        r.fieldcell('email_pec')
        r.fieldcell('email_cc_pec')
        

        #r.fieldcell('port')

    def th_order(self):
        return 'consignee'

    def th_query(self):
        return dict(column='consignee', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('agency_id', width='10em')
        fb.br()
        fb.field('service_for_email_id')
        fb.br()
        fb.field('consignee', width='40em')
        fb.br()
        fb.div("!![en]Insert the emails separate by commas",font_weight='bold', margin_top='10px')
        fb.br()
        fb.field('email',width='40em', height='10em',tag='textarea')
        
        fb.field('email_cc',width='40em', height='10em',tag='textarea')
        fb.field('email_bcc',width='40em', height='10em',tag='textarea')
        fb.br()
        fb.div("!![en]Insert the emails separate by commas",font_weight='bold', margin_top='10px')
        fb.br()
        fb.field('email_pec',width='40em', height='10em',tag='textarea')
        
        fb.field('email_cc_pec',width='40em', height='10em',tag='textarea')
        #fb.field('port')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
