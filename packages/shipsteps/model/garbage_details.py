# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('garbage_details', pkey='id', name_long='!![en]Garbage detail', name_plural='!![en]Garbage detail',caption_field='tip_garbage_id')
        self.sysFields(tbl)

        tbl.column('garbage_id',size='22', group='_', name_long='garbage_id'
                    ).relation('garbage.id', relation_name='garbage', mode='foreignkey', onDelete='cascade')
        tbl.column('tip_garbage_id',size='22', name_long='!![en]Garbage type'
                    ).relation('tip_garbage.id', relation_name='tipgarb', mode='foreignkey', onDelete='raise')
        tbl.column('measure', name_short='!![en]Measure')
        tbl.column('quantity', name_short='!![en]Quantity')
        
    def trigger_onInserted(self,record=None):
        if record['tip_garbage_id']=='sludge________________' or record['tip_garbage_id']=='bilge_________________' or record['tip_garbage_id']=='sewage________________' or record['tip_garbage_id']=='dirtyoil______________':
            custombtn=True
            self.aggiornaTasklist(record,custombtn)
        else:
            custombtn=False
            self.aggiornaTasklist(record,custombtn)    
    
    def trigger_onUpdated(self,record=None,old_record=None):
        print(X)
        if record['tip_garbage_id']=='sludge________________' or record['tip_garbage_id']=='bilge_________________' or record['tip_garbage_id']=='sewage________________' or record['tip_garbage_id']=='dirtyoil______________':
            custombtn=True
            self.aggiornaTasklist(record,custombtn)
        else:
            custombtn=False
            self.aggiornaTasklist(record,custombtn)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        if record['tip_garbage_id']=='sludge________________' or record['tip_garbage_id']=='bilge_________________' or record['tip_garbage_id']=='sewage________________' or record['tip_garbage_id']=='dirtyoil______________':
            custombtn=False
            self.aggiornaTasklist(record,custombtn)
        else:
            custombtn=True
            self.aggiornaTasklist(record,custombtn)

    def aggiornaTasklist(self,record,custombtn=None):
        garbage_id = record['garbage_id']
        self.db.deferToCommit(self.db.table('shipsteps.garbage').setvalueTasklist,
                                    garbage_id=garbage_id,custombtn=custombtn,
                                    _deferredId=garbage_id)