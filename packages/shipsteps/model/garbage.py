# encoding: utf-8
from datetime import datetime

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
        tbl.aliasColumn('agency_fullstyle','@arrival_id.@agency_id.fullstyle')
        tbl.formulaColumn('sped_fat',"""CASE WHEN $invio_fat <> '' THEN $invio_fat ELSE $agency_fullstyle END""")
        tbl.pyColumn('datalavoro',name_long='!![en]Workdate', static=True)
        tbl.pyColumn('saluto',name_long='!![en]Greeting', static=True)

    def pyColumn_datalavoro(self,record,field):
        data_lavoro=self.db.workdate
        
        return data_lavoro

    def pyColumn_saluto(self,record,field):
        
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno'  
        if cur_time < '17:00:00':
            sal='Buon pomeriggio'
        if cur_time < '24:00:00':
            sal = 'Buonasera'    
        if cur_time < '04:00:00':
            sal = 'Buona notte'      
        return sal