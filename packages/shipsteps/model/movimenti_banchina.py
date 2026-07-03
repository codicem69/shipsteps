# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('movimenti_banchina', pkey='id', name_long='!![en]Movement on quay', name_plural='!![en]Movements on quay',caption_field='id')
        self.sysFields(tbl)
        tbl.column('arrival_id', size='22', name_long='Arrivo').relation('arrival.id',relation_name='mov_banchina', mode='foreignkey', onDelete='cascade')
        tbl.column('movement_ts', dtype='DH', name_long='Data/Ora',validate_notnull=True)
        tbl.column('dock_from_id', size='22', name_long='!![en]FROM',defaultFrom='@arrival_id.dock_id',validate_notnull=True).relation('dock.id',onDuplicate=False)
        tbl.column('dock_to_id', size='22', name_long='!![en]TO',validate_notnull=True).relation('dock.id',onDuplicate=False)
        tbl.column('pilot', dtype='B', name_long='Piloti', name_short='Piloti')
        tbl.column('moor', dtype='B', name_long='Ormeggiatori', name_short='Ormeggiatori')
        tbl.column('tug', dtype='B', name_long='Rimorchiatori', name_short='Rimorchiatori')
        tbl.column('num_tug', dtype='N', name_long='Numero Rimorchiatori', name_short='Numero Rimorchiatori')
        tbl.column('reason', name_long='!![EN]Reason', validate_notnull=True)
        tbl.column('note', name_long='Note', validate_notnull=True)

 

    def trigger_onInserted(self, record=None, **kwargs):
        self._syncArrival(record)

    def trigger_onUpdated(self, record=None, old_record=None, **kwargs):
        self._syncArrival(record)

    def trigger_onDeleted(self, record=None, **kwargs):
        self._syncArrival(record)


    def _syncArrival(self, record):
        arrival_id = record['arrival_id']
        
        last_mov = self.query(
        where='$arrival_id=:arrival_id',
        arrival_id=arrival_id,
        order_by='$movement_ts DESC',
        limit=1).fetch()
        if last_mov:
            banchina_id = last_mov[0]['dock_to_id'] if last_mov else None
    
            if record:
                #self._updateArrivalDock(record['arrival_id'])
                self.db.deferToCommit(self.db.table('shipsteps.arrival').aggiornaDati,
                                        arrival_id=arrival_id,
                                        dock_id=banchina_id,
                                        _deferredId=arrival_id)