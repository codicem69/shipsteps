#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id')
        r.fieldcell('dest')
        r.fieldcell('description')
        r.fieldcell('email')
        r.fieldcell('email_type')

    def th_order(self):
        return 'sof_id'

    def th_query(self):
        return dict(column='email_descr', op='contains', val='')

class ViewFromSofEmailQtDest(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('dest', edit=True, width='10em')
        r.fieldcell('description', edit=True, width='30em')
        r.fieldcell('email',  edit=dict(validate_notnull=True), width='20em')
        r.fieldcell('email_type', edit=dict(validate_notnull=True))
    
    def th_order(self):
        return '_row_count'

    def th_options(self):
        return dict(grid_selfDragRows=True)

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,resourcePrints,10,copia_email,10,batchAssign')
        btn_copia_email=bar.copia_email.button('Copia Email')
        btn_copia_email.dataRpc('nome_temp',self.copiaemail, record='=#FORM.record',_ask=dict(title='!![en]Select the Shippers/Receivers for q.ty destination',
                               fields=[dict(name='shiprec', lbl='!![en]Shippers/Receivers', tag='dbSelect',
                               table='shipsteps.ship_rec', columns='$id', auxColumns='$trader', hasDownArrow=True)]))
        bar.dataController("if(msgspec=='no_email') {alert('No emails found, please insert the emails in the Shippers/Receivers table')}", msgspec='^nome_temp')
    
    @public_method
    def copiaemail(self, record=None, **kwargs):
        tbl_email_sof=self.db.table('shipsteps.email_shiprecdest')
        shiprec_id=kwargs['shiprec']
        shiprec_id_dest = kwargs['record_attr']['_pkey']
        
        email_to= tbl_email_sof.query(columns="$dest,$description,$email,$email_type",
                                                    where='$ship_rec_id=:s_id', s_id=shiprec_id).fetch() 
        if email_to == []:
            nome_temp = 'no_email'
            return nome_temp

        for e in range(len(email_to)):
            
            new_email = self.db.table('shipsteps.email_qt_destino').newrecord(sof_id=shiprec_id_dest,dest=email_to[e][0],description=email_to[e][1],
                                                            email=email_to[e][2],email_type=email_to[e][3])
            self.db.table('shipsteps.email_qt_destino').insert(new_email)

        self.db.commit()

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id' )
        fb.field('dest' )
        fb.field('description' )
        fb.field('email' )
        fb.field('email_type' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
