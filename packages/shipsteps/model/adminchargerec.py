# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('adminchargerec', pkey='id', name_long='Administartion charge receipt', name_plural='Administartion charges receipt',caption_field='arrival_id')
        self.sysFields(tbl,counter=True)

        tbl.column('prot',name_long='!![en]Admin charge number',unique=True)
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('arrival_id',size='22', group='_', name_long='arrival_id',
                    ).relation('arrival.id', relation_name='admincharge_arrival', mode='foreignkey', onDelete='raise')
        tbl.column('importo',dtype='N',size='10,2',name_long='Importo',format='#,###.00')

    def counter_prot(self,record=None):
        return dict(format='$YY/$NNNN', code='*', period='YY', date_field='data', showOnLoad=True, date_tolerant=True, recycle=True)

    def randomValues(self):
        return dict(data = dict(sorted=True))
    
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
    
    