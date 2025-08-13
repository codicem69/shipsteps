# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('garbage', pkey='id', name_long='!![en]Garbage form', 
                        name_plural='!![en]Garbage form',caption_field='arrival_ref')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='garbage_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('ora_arr', dtype='H', name_short='!![en]Arrival time')
        tbl.column('data_arr', dtype='D', name_short='!![en]Arrival date')
        tbl.column('sosta_gg', size=':2', name_short='!![en]Period of stay')
        #tbl.column('rif_alim', dtype='B', name_short='!![en]Food waste')
        #tbl.column('bilge', dtype='B', name_short='!![en]Bilge waste')
        #tbl.column('cargo_res', dtype='B', name_short='!![en]Cargo residues')
        #tbl.column('altro', dtype='B', name_short='!![en]Other')
        #tbl.column('altro_spec', name_short='!![en]Specify other')
        tbl.column('invio_fat', name_short='!![en]Sending invoice')
        tbl.column('note', name_short='!![en]Note')
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.pyColumn('datalavoro',name_long='!![en]Workdate', static=True)
        tbl.aliasColumn('agency_fullstyle','@arrival_id.@agency_id.fullstyle')
        tbl.formulaColumn('arrival_ref',"""'Garbage to be delivered ' || @arrival_id.@vessel_details_id.@imbarcazione_id.tip_imbarcazione_code 
                          || ' ' || @arrival_id.@vessel_details_id.@imbarcazione_id.nome""")
        tbl.formulaColumn('sped_fat',"""CASE WHEN $invio_fat <> '' THEN $invio_fat ELSE $agency_fullstyle END""")
        #tbl.formulaColumn('rif_alim_x',"""CASE WHEN $rif_alim = 'true' THEN 'X' ELSE '' END""")
        #tbl.formulaColumn('bilge_x',"""CASE WHEN $bilge = 'true' THEN 'X' ELSE '' END""")
        #tbl.formulaColumn('cargo_res_x',"""CASE WHEN $cargo_res = 'true' THEN 'X' ELSE '' END""")
        #tbl.formulaColumn('altro_x',"""CASE WHEN $altro = 'true' THEN 'X' ELSE '' END""")
        tbl.subQueryColumn('dettaglio_garbage', query=dict(table='shipsteps.garbage_details',
                                                                columns="$garbage_descr,$measure,$quantity",
                                                                where='$garbage_id=#THIS.id'), 
                                                 mode='json', name_long='Dettaglio garbage')
        
    def pyColumn_datalavoro(self,record,field):
        data_lavoro=self.db.workdate
        
        return data_lavoro

    
    def setvalueTasklist(self, garbage_id=None,custombtn=None):
        with self.recordToUpdate(garbage_id) as record:
            arrival_id = record['arrival_id']
            tbl_tasklist = self.db.table('shipsteps.tasklist')
            rec_updated=tbl_tasklist.batchUpdate(dict(btn_customgb=custombtn),
                                    where='$arrival_id=:a_id', a_id=arrival_id)
            
            self.db.commit()
