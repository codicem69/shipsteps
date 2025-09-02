#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrnumber import floatToDecimal,decimalRound

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('arrival_id')
        r.fieldcell('services_id')
        r.fieldcell('data_serv')
        r.fieldcell('descrizione')
        r.fieldcell('note')
        r.fieldcell('nt')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='services_id', op='contains', val='')

class ViewFromVesselServices(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('services_id', hasArrowDown=True, edit=True, width='20em')
        r.fieldcell('data_serv', edit=True)
        r.fieldcell('descrizione', edit=True, width='30em')
        r.fieldcell('note', edit=True, width='30em')
        r.fieldcell('nt', edit=True)

    def th_order(self):
        return '_row_count'
        
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,10,servizi_std,*,stampa_services,stampa_serv_int,5,ctm,tax_ancor,print_ta')
        btn_services_std=bar.servizi_std.button('!![en]Insert standard services')
        btn_tax_ancor=bar.tax_ancor.button('!![en]Insert Anchorage dues')
        btn_stampa_ta=bar.print_ta.button('!![en]Print Request Anchorage dues')
        btn_stampa_ta.dataRpc('nome_temp', self.print_template_services,record='=#FORM.record',
                            nome_template = 'shipsteps.arrival:tax_anchor',format_page='A4')
        btn_services_std.dataRpc('nome_temp', self.insert_StdServices,record='=#FORM.record')
        btn_tax_ancor.dataRpc('nome_temp', self.print_template_services,record='=#FORM.record',nome_template = 'shipsteps.arrival:tax_anchor',format_page='A4',
                              _ask=dict(title='!![en]Italian Anchorage Dues',fields=[dict(name='durata',lbl='!![en]Duration',tag='filteringSelect',
                                values='30gg:30 Giorni,1 Anno:1 Anno',hasDownArrow=True,validate_notnull=True),
                                dict(name='importo', lbl='!![en]Price', tag='numberTextBox',validate_notnull=True,cols=4,popup=True,colspan=2)]))
        btn_print_services=bar.stampa_services.button('!![en]Print Vessel services')
        btn_print_services.dataRpc('nome_temp', self.print_template_services,record='=#FORM.record',
                            nome_template = 'shipsteps.arrival:vess_serv',format_page='A4')
        btn_print_services_int=bar.stampa_serv_int.button('!![en]Print Vessel services private')
        btn_print_services_int.dataRpc('', self.print_template_services,record='=#FORM.record',
                            nome_template = 'shipsteps.arrival:vess_serv_int',format_page='A4')
        btn_ctm=bar.ctm.button('!![en]Print Cash to Master')
        btn_ctm.dataRpc('', self.print_template_services,record='=#FORM.record',nome_template = 'shipsteps.arrival:ctm',format_page='A4',
                            _ask=dict(title='!![en]Insert the Amount of Cash to Master',
                            fields=[dict(name='ctm', lbl='!![en]Amount', tag='numberTextBox',validate_notnull=True,table='shipsteps.arrival',
                            cols=1,popup=True,colspan=2),dict(name='datectm', lbl='!![en]Date receipt', tag='dateTextBox',validate_notnull=True,
                            cols=1,popup=True,colspan=2)]))#,_onCalling="{SET #FORM.record.ctm=ctm; SET #FORM.record.date_ctm=datectm;}this.form.save();")
    
    @public_method
    def insert_StdServices(self, record, **kwargs):
        record_id = record['id']
        tbl_std_serv = self.db.table('shipsteps.service_std')
        record_std_serv = tbl_std_serv.query(columns="*",
                         where='').fetch()
        
        tbl_vessel_serv = self.db.table('shipsteps.vessel_services')
        
        for r in record_std_serv:
            if not tbl_vessel_serv.checkDuplicate(arrival_id=record_id,services_id=r['services_id']):
                nuovo_rec = dict(arrival_id=record_id,services_id=r['services_id'],descrizione=r['descrizione'])
                tbl_vessel_serv.insert(nuovo_rec)
            
        self.db.commit() 

    @public_method
    def print_template_services(self, record, nome_template=None, format_page=None, **kwargs):
         # Crea stampa
        record_id = record['id']
        tbl_arrival = self.db.table('shipsteps.arrival')
        
        if nome_template == 'shipsteps.arrival:ctm':
            if kwargs:
                ctm=kwargs['ctm']
                date_ctm=kwargs['datectm']
                tbl_arrival.batchUpdate(dict(ctm=ctm,date_ctm=date_ctm),
                                    where='$id=:id_arr', id_arr=record_id)
                self.db.commit()
            #inseriamo nella tabella servizi il ctm
                tbl_services = self.db.table('shipsteps.services')
                services_id = tbl_services.readColumns(columns="$id", where='$description ILIKE:descr', descr='cash to master')
                tbl_vessel_services = self.db.table('shipsteps.vessel_services')
                    
                if not tbl_vessel_services.checkDuplicate(services_id=services_id,arrival_id=record_id,note='Richiesta inviata il '+str(self.db.workdate)):
                        nuovo_record = dict(services_id=services_id,descrizione='Euro '+str(decimalRound(ctm,2)),data_serv=date_ctm, note='Modulo stampato il '+str(self.db.workdate),
                                        arrival_id=record_id)
                        tbl_vessel_services.insert(nuovo_record)
                        self.db.commit()    
        #verifichiamo se stiamo stampando la tassa ancoraggio e inseriamo i valori nella tabella arrivo
        if nome_template == 'shipsteps.arrival:tax_anchor':
            if "durata" in kwargs:
                durata=kwargs['durata']
                importo=kwargs['importo']
                tbl_arrival.batchUpdate(dict(durata_anchor=durata,anchor_value=importo),
                                    where='$id=:id_arr', id_arr=record_id)
                self.db.commit()
                #inseriamo nella tabella servizi la tassa ancoraggio
                tbl_services = self.db.table('shipsteps.services')
                services_id = tbl_services.readColumns(columns="$id", where='$description ILIKE:descr', descr='italian anchorage dues')
                tbl_vessel_services = self.db.table('shipsteps.vessel_services')
                if durata == '30gg':
                    durata = '30 days'
                else:
                    durata = '1 year'     
                if not tbl_vessel_services.checkDuplicate(services_id=services_id,arrival_id=record_id,note='Richiesta inviata il '+str(self.db.workdate)):
                        nuovo_record = dict(services_id=services_id,descrizione=durata,data_serv=self.db.workdate, note='Modulo stampato il '+str(self.db.workdate),
                                        arrival_id=record_id)
                        tbl_vessel_services.insert(nuovo_record)
                        self.db.commit()
                        
        builder = TableTemplateToHtml(table=tbl_arrival)
        #nome_template = nome_template #'shipsteps.arrival:check_list'

        nome_temp = nome_template.replace('shipsteps.arrival:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        #nome_file_st = 'laboratorio_piazza_sta_{cl_id}.pdf'.format(
        #    cl_id=self.avatar.user_id)
        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
       # print(x)
       #tbl_template=self.db.table('adm.htmltemplate')
       #letterhead = tbl_template.readColumns(columns='$id',
       #          where='$name=:tp_name', tp_name='A3_orizz')
        # (pdfpath.internal_path)
        

        builder(record=record_id, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)
        #print(x)
        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)
        return nome_temp
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('services_id')
        fb.field('data_serv')
        fb.field('descrizione')
        fb.field('note')
        fb.field('nt')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

