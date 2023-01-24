#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromCertificates_atc(BaseComponent):

    def th_hiddencolumns(self):
        return '$fileurl,$is_foreign_document'
    
    def th_struct(self,struct):
        r = struct.view().rows()
        
        r.fieldcell('description', edit=True, width='20em')
        r.fieldcell('__ins_ts', width='auto')
        r.fieldcell('fileurl', width='10em')
        r.fieldcell('mimetype')
      

    def th_order(self):
        return '__ins_ts:d'