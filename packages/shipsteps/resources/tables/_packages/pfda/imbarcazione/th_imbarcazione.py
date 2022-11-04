#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tipo')
        r.fieldcell('nome',width='20em')
        r.fieldcell('bandiera')
        r.fieldcell('loa')
        r.fieldcell('gt')
        r.fieldcell('nt')
        r.fieldcell('imo', name='IMO')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')
