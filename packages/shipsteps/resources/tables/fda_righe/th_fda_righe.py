#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('fda_id')
        r.fieldcell('services_id')
        r.fieldcell('description')
        r.fieldcell('importo_pfda')
        r.fieldcell('inv_n')
        r.fieldcell('data_inv')
        r.fieldcell('importo')

    def th_order(self):
        return 'fda_id'

    def th_query(self):
        return dict(column='prot_arr', op='contains', val='')

class ViewFromRigheFda(BaseComponent):
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('services_id', edit=dict(hasDownArrow=True),width='50%')
        r.fieldcell('description', edit=True,width='100%')
        r.fieldcell('importo_pfda', edit=True, totalize=True)
        r.fieldcell('inv_n', edit=True)
        r.fieldcell('data_inv', edit=True)
        r.fieldcell('importo', edit=True, totalize=True, width='8em')

    def th_order(self):
        return '_row_count'
    
    def th_options(self):
        return dict(grid_selfDragRows=True)
    
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('delrow','loadPfdaRighe,5,insertRigheStandard,5,printTblServices,25,delrow')
        btn_pfda=bar.loadPfdaRighe.button('!![en]Load PFDA',disabled="""^#FORM.record.pfda_id?=#v==null""")
        btn_pfda_standard=bar.insertRigheStandard.button('!![en]Insert Standard Services',disabled="""^#FORM.record.pfda_id""")
        #btn_pfda=bar.loadPfdaRighe.button('!![en]Load PFDA')#,disabled="""^shipsteps_arrival.form.shipsteps_fda.form.shipsteps_fda_righe.view.count.shown?=#v>0""")
        btn_pfda_standard.dataRpc(self.insert_StdServicesFda,record='=#FORM.record')
        btn_pfda.dataRpc(self.loadPfda,record='=#FORM.record')
        template_id = self.db.table('adm.userobject').readColumns(columns="$id",
                  where='$tbl=:tbl AND $code=:code', tbl='shipsteps.fda', code='tab_servizi_fda')
        bar.printTblServices.button('Stampa Tabella servizi', iconClass='print',
                                    action="""
                               var tp = {template:template_id};
                               var kw = objectExtract(this.getInheritedAttributes(),"batch_*",true);
                               kw.table = 'shipsteps.fda';
                               kw.resource = "print_template";
                               kw.res_type = "print";
                               kw.templates = "A3_orizz";
                               kw.pkey = this.form.getCurrentPkey();
                               kw.extra_parameters = new gnr.GnrBag({template_id:tp.template,table:kw.table});
                               genro.publish("table_script_run",kw)""",template_id=template_id)#sostituire il valore template_id con la variabile
        
        #bar.printTblServices.button('Stampa Tabella servizi', iconClass='print',ask=dict(title='Template',fields=[dict(lbl='Tabella servizi',hasDownArrow=True,
        #                                                            name='template_id',tag='dbselect',dbtable='adm.userobject',auxColumns='$tbl',columns='$tbl',
        #                                                            condition='$tbl=:tbl',condition_tbl='shipsteps.fda')]),
        #                            action="""
        #                       var tp = {template:template_id};
        #                       var kw = objectExtract(this.getInheritedAttributes(),"batch_*",true);console.log(kw);
        #                       kw.table = 'shipsteps.fda';
        #                       kw.resource = "print_template";
        #                       kw.res_type = "print";
        #                       kw.pkey = this.form.getCurrentPkey();
        #                       kw.extra_parameters = new gnr.GnrBag({template_id:tp.template,table:kw.table});
        #                       genro.publish("table_script_run",kw)""")#,template_id='9aTZZ9GrOJuXawmlnYiifQ')#sostituire il valore template_id con la variabile
    @public_method
    def insert_StdServicesFda(self, record, **kwargs):
        record_id = record['id']
        tbl_std_serv = self.db.table('shipsteps.service_fda_std')
        record_std_serv = tbl_std_serv.query(columns="*",
                         where='',order_by='$_row_count').fetch()
        
        tbl_fdaRighe = self.db.table('shipsteps.fda_righe')
        
        for r in record_std_serv:
            if not tbl_fdaRighe.checkDuplicate(fda_id=record_id,services_id=r['services_id'],description=r['descrizione']):
                nuovo_rec = dict(fda_id=record_id,services_id=r['services_id'],description=r['descrizione'])
                tbl_fdaRighe.insert(nuovo_rec)
            
        self.db.commit() 

    @public_method
    def loadPfda(self, record, **kwargs):
        
        pfda_id = record['pfda_id']
        tbl_pfda = self.db.table('pfda.proforma')
        
        record_pfda = tbl_pfda.query(columns="*",
                         where='$id=:fda_id',fda_id=pfda_id).fetch()
        serviziextra = self.db.table('pfda.serviziextra').query(columns='$descrizione_servizio,$descrizione,$tariffa',
                                                                    where='$proforma_id=:p_id',
                                                                    p_id=pfda_id).fetch()
        tbl_fdaRighe = self.db.table('shipsteps.fda_righe')
        
        for r in record_pfda:
            for l in r.keys():
                if l == 'diritticp':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='HARBOUR MASTER DUES'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='HARBOUR MASTER DUES', importo_pfda=r[l]) 
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'admcharge':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='ADMINISTRATION CHARGE'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='ADMINISTRATION CHARGE', importo_pfda=r[l])         
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'pilot':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description=l.upper()):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description=l.upper(), importo_pfda=r[l])
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'moor':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='MOORINGMEN'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='MOORINGMEN', importo_pfda=r[l])
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'tug':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description=l.upper()):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description=l.upper(), importo_pfda=r[l]) 
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'agency':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='AGENCY FEES'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='AGENCY FEES', importo_pfda=r[l])
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'customs':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='CUSTOMS CLEARANCE'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='CUSTOMS CLEARANCE', importo_pfda=r[l])   
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'garbage':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description=l.upper()):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description=l.upper(), importo_pfda=r[l])
                            tbl_fdaRighe.insert(nuovo_rec)    
                if l == 'retaingarbage':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='DISPENSATION FOR LIQUID WASTE'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='DISPENSATION FOR LIQUID WASTE', importo_pfda=r[l])  
                            tbl_fdaRighe.insert(nuovo_rec)     
                if l == 'isps':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description=l.upper()):
                        if r[l]:    
                            nuovo_rec = dict(fda_id=record['id'],description=l.upper(), importo_pfda=r[l])
                            tbl_fdaRighe.insert(nuovo_rec)     
                if l == 'misc':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='MISCELLANEOUS'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='MISCELLANEOUS', importo_pfda=r[l]) 
                            tbl_fdaRighe.insert(nuovo_rec)     
                if l == 'bulkauth':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='APPLICATION AND AUTH. BULK CARGO'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='APPLICATION AND AUTH. BULK CARGO', importo_pfda=r[l]) 
                            tbl_fdaRighe.insert(nuovo_rec)     
                if l == 'antifire':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description="ANTIFIRE / ANTIPOLLUTION"):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description="ANTIFIRE / ANTIPOLLUTION", importo_pfda=r[l]) 
                            tbl_fdaRighe.insert(nuovo_rec)             
        for s in serviziextra:
            if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description=s['descrizione_servizio']+' '+s['descrizione']):
                nuovo_rec = dict(fda_id=record['id'],description=s['descrizione_servizio']+' '+s['descrizione'], importo_pfda=s['tariffa']) 
                tbl_fdaRighe.insert(nuovo_rec)    
        for r in record_pfda:
            for l in r.keys():                                   
                if l == 'stamp':
                    if not tbl_fdaRighe.checkDuplicate(fda_id=record['id'],description='TAX STAMPS'):
                        if r[l]:
                            nuovo_rec = dict(fda_id=record['id'],description='TAX STAMPS', importo_pfda=r[l])  
                            tbl_fdaRighe.insert(nuovo_rec)                                                                         
        self.db.commit()

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('fda_id' )
        fb.field('services_id' )
        fb.field('inv_n' )
        fb.field('data_inv' )
        fb.field('importo' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
