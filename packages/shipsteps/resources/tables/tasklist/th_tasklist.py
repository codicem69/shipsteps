#!/usr/bin/python3
# -*- coding: utf-8 -*-

from multiprocessing import Semaphore
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('cheklist', semaphore=True)
        r.fieldcell('frontespizio')
        r.fieldcell('cartella_nave')
        r.fieldcell('modulo_nave')
        r.fieldcell('email_dogana')
        r.fieldcell('email_finanza')
        r.fieldcell('email_frontiera')
        r.fieldcell('email_usma')
        r.fieldcell('email_pfso')
        r.fieldcell('email_pilot')
        r.fieldcell('email_mooringmen')
        r.fieldcell('email_tug')
        r.fieldcell('email_garbage')
        r.fieldcell('email_chemist')
        r.fieldcell('email_antifire')
        r.fieldcell('email_gpg')
        r.fieldcell('email_ens')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('cheklist')
        fb.field('frontespizio')
        fb.field('cartella_nave')
        fb.field('modulo_nave')
        fb.field('email_dogana')
        fb.field('email_finanza')
        fb.field('email_frontiera')
        fb.field('email_usma')
        fb.field('email_pfso')
        fb.field('email_pilot')
        fb.field('email_mooringmen')
        fb.field('email_tug')
        fb.field('email_garbage')
        fb.field('email_chemist')
        fb.field('email_antifire')
        fb.field('email_gpg')
        fb.field('email_ens')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
