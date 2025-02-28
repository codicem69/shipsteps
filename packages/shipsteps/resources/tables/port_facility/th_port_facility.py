#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from itertools import groupby

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('facility_code', width='7em')
        r.fieldcell('country')
        r.fieldcell('nome_porto',lbl='!![en]Port name')
        r.fieldcell('nome_facility',lbl='!![en]Facility name')
        r.fieldcell('descrizione', width='40em',lbl='!![en]Description')
        r.fieldcell('longitudine', width='7em',lbl='!![en]Longitude')
        r.fieldcell('latitudine', width='7em',lbl='!![en]Latitude')
        r.fieldcell('piano_approvato', width='5em',lbl='!![en]Plan approved')
        r.fieldcell('ultimo_agg', width='8em',lbl='!![en]Last update')

    def th_order(self):
        return 'facility_code'

    def th_query(self):
        return dict(column='facility_code', op='contains', val='')

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,resourcePrints,10,importa_facility,10')
        btn_importa_facility = bar.importa_facility.paletteImporter(paletteCode='xls_importer',
                            dockButton_iconClass=False,
                            title='!!Importa facility code',
                            importButton_label='Importa facility code',
                            previewLimit=50,
                            dropMessage='Trascina qui il tuo file o clicca per cercarlo', filetype='excel',
                            importButton_action="genro.publish('import_facility',{filepath:imported_file_path})",
                            matchColumns='*')
        
        bar.dataRpc(self.importaFacility, subscribe_import_facility=True,
                      _onResult="genro.publish('floating_message',{message:result, messageType:'message'});this.form.reload();",
                      _onError="genro.publish('xls_importer_onResult',{error:error});",_lockScreen=dict(thermo=True))

    @public_method
    def importaFacility(self, filepath=None, **kwargs):
        "Importa port facilities"
        tbl_facility = self.db.table('shipsteps.port_facility')
        facility_code=tbl_facility.query(columns='$facility_code').fetchAsDict('facility_code')
        
        reader = self.utils.getReader(filepath)
        result=Bag()
        count_replace = 0
        pkeys_del=''
        
        for row in self.utils.quickThermo(reader()):
            if facility_code.get(row['imo_port_facility_number']):
                
                tbl_facility.batchUpdate(dict(facility_name=row['facility_name'],descrizione=row['description'],piano_approvato=row['plan_approved'],
                                              ultimo_agg=row['last_updated']),
                                    where='$facility_code=:f_code', f_code=facility_code.get(row['imo_port_facility_number']).get('pkey'))
                count_replace += 1 #conteggio dei record aggiornati
                #creiamo una lista delle pkeys da cancellare cercandole in facility_code se non sono presenti nel file importato 
                pkeys_del = [item for item in facility_code if item not in row['imo_port_facility_number']]
                self.db.commit()
            else:
                new_facility = self.db.table('shipsteps.port_facility').newrecord(facility_code=row['imo_port_facility_number'],country=row['country_name'],
                        nome_porto=row['port_name'],nome_facility=row['facility_name'],descrizione=row['description'],longitudine=row['longitude'],
                         latitudine=row['latitude'],piano_approvato=row['plan_approved'],ultimo_agg=row['last_updated'], **row)
            
                self.db.table('shipsteps.port_facility').insert(new_facility)    
        #cancelliamo i record che non sono presenti nella lista importata
        #dividiamo la lista pkeys_del in liste da 1000
        if pkeys_del:
            pkey=[pkeys_del[i::int(len(pkeys_del)/1000)] for i in range(int(len(pkeys_del)/1000))]
            #con il ciclo for cancelliamo 1000 record per volta per evitare l'errore di troppi record  
            for p in pkeys_del:
                #creiamo una stringa dalla lista delle pkey da cancellare
                #pkeys = (','.join(p))
                #print(X)
                tbl_facility.deleteSelection(where='$facility_code =:pkeys', pkeys=p)
        self.db.commit()
        record_cancellati = 0
        if len(pkeys_del) > 0:
            record_cancellati = len(pkeys_del)  
        result.addItem('updated_row', count_replace)
        result.addItem('deleted_row', record_cancellati)            
       
        return "Items updated "+str(count_replace) +"<br> Record deleted " + str(record_cancellati )
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('facility_code' )
        fb.field('country' )
        fb.field('nome_porto' )
        fb.field('nome_facility' )
        fb.field('descrizione' )
        fb.field('longitudine' )
        fb.field('latitudine' )
        fb.field('piano_approvato' )
        fb.field('ultimo_agg' )

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
