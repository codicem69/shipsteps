from datetime import datetime

class Table(object):
    def config_db(self,pkg):
        
        tbl=pkg.table('protocollo', pkey='id', name_long='!![en]Arrival log', name_plural='!![en]Arrival logs',
                                 caption_field='prot_n')
        self.sysFields(tbl,counter='agency_id')

        tbl.column('data', dtype='D', name_short='!![en]date')
        tbl.column('data_prat', dtype='D', name_short='!![en]Pratique date')
        tbl.column('prot_n', name_short='!![en]Log number')
        tbl.column('fald_n',size='22', name_long='!![en]Folder'
                    ).relation('faldone.id', relation_name='numero_faldone', mode='foreignkey', onDelete='raise')
        #tbl.column('fald_n', name_short='!![en]Folder no.')
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='prot_arr', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        
    def counter_prot_n(self,record=None):
        #2021/000001
        tbl_agency = self.db.table('shipsteps.agency')
        codice = tbl_agency.readColumns(columns='$code', where = '$id =:ag_id', ag_id=self.db.currentEnv.get('current_agency_id'))
        
        return dict(format='$K$YY/$NNN',code=codice,  period='YY', date_field='data', showOnLoad=True, date_tolerant=True)
       

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),data = self.db.workdate)
