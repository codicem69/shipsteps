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
        tbl.aliasColumn('garbage_descr', '@tip_garbage_id.description',name_long='descrizione prodotto')

   #def setCustombtn(self,record):
   #    if record['tip_garbage_id']=='sludge________________' or record['tip_garbage_id']=='bilge_________________' or record['tip_garbage_id']=='dirtyoil______________':
   #        custombtn=True
   #        
   #    elif not record['tip_garbage_id']=='sludge________________' or record['tip_garbage_id']=='bilge_________________' or record['tip_garbage_id']=='dirtyoil________________' or record['tip_garbage_id']=='dirtyoil______________':
   #            custombtn=True
   #    else:
   #            custombtn=False
   #    self.aggiornaTasklist(record,custombtn)

    def trigger_onInserted(self,record=None):
        self.aggiornaTasklist(record)
        #self.setCustombtn(record)
        
    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaTasklist(record)
        #self.setCustombtn(record)
 
    def trigger_onDeleted(self,record=None):
        self.aggiornaTasklist(record)
        #self.setCustombtn(record)
 
    def aggiornaTasklist(self,record):
        garbage_id = record['garbage_id']
        tbl_garbagedet = self.db.table('shipsteps.garbage_details')
        garbage_details = tbl_garbagedet.query(columns='$tip_garbage_id', where='$garbage_id=:garbage_id',garbage_id=garbage_id).fetch()
        garbage_annexI={'sludge________________','bilge_________________','dirtyoil______________'}
        annexI = [d for d in garbage_details if d["tip_garbage_id"] in garbage_annexI]
        if annexI:
            custombtn = True
        else:
            custombtn =False

        self.db.table('shipsteps.garbage').setvalueTasklist(
                                    garbage_id=garbage_id,custombtn=custombtn)
                             