#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromEmailServicesAtc(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        
        #r.fieldcell('external_url')
        r.fieldcell('description')
        r.fieldcell('mimetype')
        

    def th_order(self):
        return 'description'

    




