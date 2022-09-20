from datetime import datetime

class Table(object):
    def config_db(self,pkg):
        
        tbl=pkg.table('protocollo', pkey='id', name_long='!![en]Arrival log', name_plural='!![en]Arrival logs',
                                 caption_field='prot_n', partition_agency_id='agency_id')
        self.sysFields(tbl,counter=True)
        tbl.column('agency_id',size='22',name_long='!![en]Agency').relation(
                                    'agency.id',relation_name='name_agency', mode='foreignkey', onDelete='raise')
        tbl.column('data', dtype='D', name_short='!![en]date')
        tbl.column('data_prat', dtype='D', name_short='!![en]Pratique date')
        tbl.column('prot_n', name_short='!![en]Log number')
        tbl.column('fald_n', name_short='!![en]Folder no.')
        tbl.column('description', name_short='!![en]Description')
        tbl.pyColumn('datacorrente',name_long='!![en]Current date', static=True)

    def counter_prot_n(self,record=None):
        #2021/000001
        return dict(format='$K$YY/$NNN',code='A',  period='YY', date_field='data', showOnLoad=True, date_tolerant=True)
    
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),data = self.db.workdate)

    def pyColumn_datacorrente(self,record,field):
        data_lavoro=self.db.workdate