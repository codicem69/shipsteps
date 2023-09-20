# encoding: utf-8
from datetime import datetime

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bolli', pkey='id', name_long='!![en]Stamp', name_plural='!![en]Stamps',caption_field='id')
        self.sysFields(tbl)

        tbl.column('date', dtype='DH', name_short='!![en]Date')
        tbl.column('imbarcazione_id',size='22', name_long='!![en]Vessel'
                    ).relation('pfda.imbarcazione.id', relation_name='imbarcazioneid_bolli', mode='foreignkey', onDelete='raise')
        tbl.column('istanza', name_short='!![en]Application')
        tbl.column('id_istanza', name_short='!![en]Application id')
        tbl.column('ref_number',name_short='!![en]Reference number')
        tbl.column('bolli_tr14', dtype='N', name_short='!![en]Stamps tr.14')
        tbl.column('bolli_tr22', dtype='N', name_short='!![en]Stamps tr.22')
        tbl.column('note', name_short='!![en]Notes')
        tbl.formulaColumn('tot_tr14', select=dict(table='shipsteps.bolli',
                                                columns="""SUM($bolli_tr14)""",
                                                where='', dtype='N',name_long='Tot_tr14'))
        tbl.formulaColumn('tot_tr22', select=dict(table='shipsteps.bolli',
                                                columns="""SUM($bolli_tr22)""",
                                                where='', dtype='N',name_long='Tot_tr22'))
        tbl.formulaColumn('anno_doc',"date_part('year', $date)", dtype='D')
    
    def defaultValues(self):
        return dict(date = datetime.now())