#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count')
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
        r.fieldcell('_row_count')
        r.fieldcell('services_id', hasArrowDown=True, edit=True, width='20em')
        r.fieldcell('data_serv', edit=True)
        r.fieldcell('descrizione', edit=True, width='30em')
        r.fieldcell('note', edit=True, width='30em')
        r.fieldcell('nt', edit=True)

    def th_order(self):
        return '_row_count'
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,10,stampa_services,stampa_serv_int')
        btn_print_services=bar.stampa_services.button('!![en]Print Vessel services')
        btn_print_services.dataRpc('msg_special', self.print_template_services,record='=#FORM.record',servizio=[],
                            nome_template = 'shipsteps.arrival:vess_serv',format_page='A4')
        btn_print_services_int=bar.stampa_serv_int.button('!![en]Print Vessel services private')
        btn_print_services_int.dataRpc('msg_special', self.print_template_services,record='=#FORM.record',servizio=[],
                            nome_template = 'shipsteps.arrival:vess_serv_int',format_page='A4')

    @public_method
    def print_template_services(self, record, resultAttr=None, nome_template=None, format_page=None, **kwargs):
        # Crea stampa
        record_id = record['id']
        
        tbl_arrival = self.db.table('shipsteps.arrival')
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

