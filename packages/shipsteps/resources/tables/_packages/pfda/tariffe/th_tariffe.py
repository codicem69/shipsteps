#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id')
        r.fieldcell('codice')
        r.fieldcell('descrizione')
        r.fieldcell('valore')
        r.fieldcell('tariffa_tipo_id')

    def th_options(self):
        return dict(partitioned=True)
