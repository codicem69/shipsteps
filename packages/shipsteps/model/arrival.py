# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('arrival', pkey='id', name_long='!![en]Arrival', name_plural='!![en]Arrivals',
                                 caption_field='reference_num', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('agency_id',size='22',name_long='!![en]Agency').relation(
                                    'agency.id',relation_name='agency_id_name', mode='foreignkey', onDelete='raise')
        tbl.column('reference_num',name_long='!![en]Reference number')
        tbl.column('date',dtype='D',name_long='!![en]Date')
        tbl.column('pfda_id',size='22',name_short='!![en]Pfda no.').relation('pfda.proforma.id',relation_name='pfda_arr', mode='foreignkey', onDelete='raise')
        tbl.column('vessel_details_id',size='22',name_long='!![en]Vessel',validate_notnull=True).relation(
                                    'vessel_details.id',relation_name='vessel_details_name', mode='foreignkey', onDelete='raise')
        tbl.column('eta', dtype='DH', name_short='!![en]ETA')
        tbl.column('etb', dtype='DH', name_short='!![en]ETB')
        tbl.column('et_start', dtype='DH', name_short='!![en]ET start')
        tbl.column('etc', dtype='DH', name_short='!![en]ETC')
        tbl.column('ets', dtype='DH', name_short='!![en]ETS')
        tbl.column('draft_aft_arr', dtype='N',size='10,2', name_short='!![en]AFT draft arr.', format='#,###.00')
        tbl.column('draft_fw_arr', dtype='N',size='10,2', name_short='!![en]FW draft arr.', format='#,###.00')
        tbl.column('draft_aft_dep', dtype='N',size='10,2', name_short='!![en]AFT draft dep.', format='#,###.00')
        tbl.column('draft_fw_dep', dtype='N',size='10,2', name_short='!![en]FW draft dep', format='#,###.00')
        tbl.column('mandatory', name_short='!![en]Mandatory')
        tbl.column('dock_id',size='22', name_long='!![en]Dock'
                    ).relation('dock.id', relation_name='dock_id_arr', mode='foreignkey', onDelete='raise')
        tbl.column('info_moor', name_short='!![en]Moor info')
        tbl.column('master_name', name_short='!![en]Master name')
        tbl.column('n_crew', dtype='N',name_short='!![en]Crew no.')
        tbl.column('n_passengers', dtype='N',name_short='!![en]Passengers no.')
        tbl.column('last_port',size='22',name_short='!![en]Last port').relation('unlocode.place.id',relation_name='lastport_arr', mode='foreignkey', onDelete='raise')
        tbl.column('departure_lp', dtype='DH', name_short='!![en]Departure last port')
        tbl.column('next_port',size='22',name_short='!![en]Next port').relation('unlocode.place.id',relation_name='nextport_arr', mode='foreignkey', onDelete='raise')
        tbl.column('eta_np', dtype='DH', name_short='!![en]ETA next port')
        tbl.column('cargo_dest', name_short='!![en]Cargo destination')
        tbl.column('invoice_det_id',size='22', name_long='!![en]Invoicing'
                    ).relation('invoice_det.id', relation_name='invoicing_arr', mode='foreignkey', onDelete='raise')
        tbl.column('cargo_onboard', name_short='!![en]Cargo on board')
        tbl.column('transit_cargo', name_short='!![en]Transit Cargo')
        #tbl.formulaColumn('cargoboard',select=dict(table='shipsteps.cargo_transit', columns='SUM($description)', where='$arrival_id=#THIS.id'), dtype='T',name_long='cargo on board')
        tbl.pyColumn('cargo',name_long='!![en]Cargo', static=True)
        #tbl.aliasColumn('carico_a_bordo','@cargo_onboard_arr.carico_a_bordo')
        tbl.aliasColumn('carico_arr','@cargo_lu_arr.cargo_arr',name_long='Carico in arrivo')
        tbl.aliasColumn('cargo_lu_en','@cargo_lu_arr.cargo_ship_rec',name_long='!![en]Cargo L/U')
       # tbl.aliasColumn('transit_cargo','@cargo_transit_arr.transit_cargo')
        tbl.aliasColumn('ship_rec','@cargo_lu_arr.ship_rec',name_long='!![en]Shipper/Receivers')
        tbl.aliasColumn('tot_cargo','@cargo_lu_arr.tot_cargo')#,name_long='!![en]Cargo total')
        tbl.aliasColumn('lastport','@last_port.citta_nazione', name_long='!![en]Last port')
        tbl.aliasColumn('nextport','@next_port.citta_nazione', name_long='!![en]Next port')
        tbl.formulaColumn('prox_port', """CASE WHEN $nextport = 'ORDER - ORDINI' THEN '' ELSE $nextport END""" )

    def pyColumn_cargo(self,record,field):
        
        pkey=record['pkey']
        
        #carico = self.db.table('shipsteps.cargo_unl_load').readColumns(columns='$description', where='$arrival_id=:a_id',a_id=pkey)
        carico = self.db.table('shipsteps.cargo_unl_load').query(columns="COALESCE($operation,'') || ': ' || COALESCE(@measure_id.description,'') || ' ' || $quantity || ' ' || COALESCE($description,'')",
                                                                    where='$arrival_id=:a_id',
                                                                    a_id=pkey).fetch()
        n_car = len(carico) 
        cargo=''                                                               
        for r in range (n_car):
            cargo += ' - ' + carico[r][0] + '<br>'

       
        return cargo
        
        
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),date = self.db.workdate)


   #def defaultValues(self):
   #     return dict(date = self.db.workdate)

    def counter_reference_num(self,record=None):
        #2021/000001
        return dict(format='$K$YYYY/$NNNNNN', code='A', period='YYYY', date_field='date', showOnLoad=True, date_tolerant=True)

    def randomValues(self):
        return dict(date = dict(sorted=True))
