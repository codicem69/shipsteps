# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('garbage', pkey='id', name_long='!![en]Garbage form', 
                        name_plural='!![en]Garbage form',caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='garbage_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('ora_arr', dtype='H', name_short='!![en]Arrival time')
        tbl.column('data_arr', dtype='D', name_short='!![en]Arrival date')
        tbl.column('sosta_gg', size=':2', name_short='!![en]Period of stay')
        tbl.column('rif_alim', dtype='B', name_short='!![en]Food waste')
        tbl.column('bilge', dtype='B', name_short='!![en]Bilge waste')
        tbl.column('cargo_res', dtype='B', name_short='!![en]Cargo residues')
        tbl.column('altro', dtype='B', name_short='!![en]Other')
        tbl.column('altro_spec', name_short='!![en]Specify other')
        tbl.column('invio_fat', name_short='!![en]Sending invoice')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.pyColumn('datalavoro',name_long='!![en]Workdate', static=True)
        tbl.aliasColumn('agency_fullstyle','@arrival_id.@agency_id.fullstyle')
        tbl.formulaColumn('sped_fat',"""CASE WHEN $invio_fat <> '' THEN $invio_fat ELSE $agency_fullstyle END""")
        tbl.formulaColumn('rif_alim_x',"""CASE WHEN $rif_alim = 'true' THEN 'X' ELSE '' END""")
        tbl.formulaColumn('bilge_x',"""CASE WHEN $bilge = 'true' THEN 'X' ELSE '' END""")
        tbl.formulaColumn('cargo_res_x',"""CASE WHEN $cargo_res = 'true' THEN 'X' ELSE '' END""")
        tbl.formulaColumn('altro_x',"""CASE WHEN $altro = 'true' THEN 'X' ELSE '' END""")

    def pyColumn_datalavoro(self,record,field):
        data_lavoro=self.db.workdate
        
        return data_lavoro

    