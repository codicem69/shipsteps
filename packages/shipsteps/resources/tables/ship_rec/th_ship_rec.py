#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', width='50em')
        r.fieldcell('address', width='50em')
        r.fieldcell('city', width='50em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

class ViewFromShipRec(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', width='50em',edit=True)
        r.fieldcell('address', width='50em',edit=True)
        r.fieldcell('city', width='50em',edit=True)
    
    def th_order(self):
        return 'name'

class Form(BaseComponent):
    def th_form(self,form):
        bc = form.center.borderContainer()
        self.datiShiprec(bc.roundedGroupFrame(title='Shippers / Receivers',region='top',datapath='.record',height='110px', background='lightgrey', splitter=True))
        self.emailShiprec(bc.contentPane(title='Email Shippers Receivers', region='center'))

    def datiShiprec(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=1, border_spacing='4px',fld_width='60em')
  
      #  fb = pane.formbuilder(cols=1, border_spacing='4px', fld_width ='60em')
        fb.field('name' )
        fb.field('address' )
        fb.field('city' )

    def emailShiprec(self,pane):
        pane.inlineTableHandler(title='Email Shippers Receivers', relation='@email_shiprec',viewResource='ViewFromEmailShiprec',export=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
