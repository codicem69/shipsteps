#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromVesselDocs(BaseComponent):
    
    def th_hiddencolumns(self):
        return '$fileurl,$is_foreign_document'
    
    def th_struct(self,struct):
        r = struct.view().rows()
        
        r.fieldcell('description', edit=True)
        r.fieldcell('expire_date', name='Expire date', edit=True, width='5em')
        r.fieldcell('__ins_ts', width='auto')
        r.fieldcell('fileurl', width='10em')
        r.fieldcell('mimetype')
      

    def th_order(self):
        return '__ins_ts:d'

