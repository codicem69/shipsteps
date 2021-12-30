# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('arrival', pkey='id', name_long='!![en]Arrival', name_plural='!![en]Arrivals',caption_field='reference_num', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('agency_id',size='22',name_long='!![en]Agency').relation(
                                    'agency.id',relation_name='agency_id_name', mode='foreignkey', onDelete='raise')
        tbl.column('reference_num',name_long='!![en]Reference number')
        tbl.column('date',dtype='D',name_long='!![en]Date')
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
        
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),date = self.db.workdate)


   #def defaultValues(self):
   #     return dict(date = self.db.workdate)

    def counter_reference_num(self,record=None):
        #2021/000001
        return dict(format='$K$YYYY/$NNNNNN', code='A', period='YYYY', date_field='date', showOnLoad=True, date_tolerant=True)

    def randomValues(self):
        return dict(date = dict(sorted=True))