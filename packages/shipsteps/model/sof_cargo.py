# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof_cargo', pkey='id', name_long='sof_cargo', name_plural='sof_cargo',caption_field='id')
        self.sysFields(tbl)

        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_cargo_sof', mode='foreignkey', onDelete='cascade')   
        tbl.column('cargo_unl_load_id',size='22', name_long='cargo_unl_load_id'
                    ).relation('cargo_unl_load.id', relation_name='cargo_sof', mode='foreignkey', onDelete='cascade')   
        
        #tbl.aliasColumn('agency_id','@sof_id.@arrival_id.agency_id')
        tbl.aliasColumn('ship_rec','@cargo_unl_load_id.ship_rec')

    #con trigger onInserted e OnUpdated richiamiamo nel model sof la funzione insertShipRec per inserire il nome dello shipper o receiver e cargo type    
    def aggiornaSof(self,record):
        sof_id = record['sof_id']
        cargo_un_id = record['cargo_unl_load_id']
        self.db.deferToCommit(self.db.table('shipsteps.sof').insertShipRec,
                                    sof_id=sof_id,cargo_un_id=cargo_un_id,
                                    _deferredId=sof_id)    
        
    def trigger_onInserted(self,record=None):
        self.aggiornaSof(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaSof(record)
    
    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:   
            return
        self.aggiornaSof_onDel(record)

    #con trigger onDeleted richiamiamo nel model sof la funzione insertShipRec per togliere il nome dello shipper o receiver e cargo type
    def aggiornaSof_onDel(self,record):
        sof_id = record['sof_id']
        self.db.deferToCommit(self.db.table('shipsteps.sof').insertShipRec,
                                    sof_id=sof_id,cargo_un_id=None,
                                    _deferredId=sof_id)    