# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tributi_cp', pkey='id', name_long='!![en]Tributes HM', 
                        name_plural='!![en]Tributes HM',caption_field='id')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='tributi_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('beneficiario_id',size='22', name_long='beneficiario_id'
                    ).relation('beneficiario_tributi_cp.id', relation_name='beneficiario_tributi', mode='foreignkey', onDelete='raise')            
        tbl.column('causale', name_short='!![en]Reason',values='Capo XV Capitolo 2170 Tabella "D" tributi speciali')
        tbl.column('importo', dtype='N', name_short='!![en]Amount', format='#,###.00')
        tbl.column('imp_lettere', name_short='!![en]Amount letter')
        tbl.column('emesso', dtype='B', name_short='!![en]Issued')
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')
