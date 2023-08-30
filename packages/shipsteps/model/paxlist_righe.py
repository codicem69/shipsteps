class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('paxlist_righe', pkey='id', name_long='paxlist_righe', name_plural='paxlist_righe',caption_field='id', 
                                         order_by='_row_count')
        self.sysFields(tbl,counter='paxlist_id')

        tbl.column('paxlist_id',size='22', name_long='paxlist_id'
                    ).relation('paxlist.id', relation_name='paxlist_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('name', name_short='Name')
        tbl.column('surname', name_short='Surname')
        tbl.column('nationality',size='2',name_short='!![en]Nationality').relation('unlocode.nazione.code',relation_name='nationality_pax', mode='foreignkey', onDelete='raise')
        #tbl.column('nationality', name_short='Nationality')
        tbl.column('birth_date', name_short='Date of birth')
        tbl.column('birth_place', name_short='Place of birth')
        tbl.column('birth_country',size='2',name_short='!![en]Country of birth').relation('unlocode.nazione.code',relation_name='birthcountry_pax', mode='foreignkey', onDelete='raise')
        #tbl.column('birth_country', name_short='Country of birth')
        tbl.column('gender', name_short='Gender')
        tbl.column('id_doc', name_short='Identity doc')
        tbl.column('id_doc_n', name_short='Identity doc no.')
        tbl.column('id_doc_state',size='2',name_short='!![en]State identity doc').relation('unlocode.nazione.code',relation_name='docstate_pax', mode='foreignkey', onDelete='raise')
        tbl.column('expire_id_doc', name_short='Expiry identity doc')
        tbl.column('port_embark', name_short='!![en]Port of Embarkation')
        tbl.column('port_disembark', name_short='!![en]Port of Disembarkation')
        tbl.column('transit', name_short='!![en]Transit passengers')
        tbl.column('visa_n', name_short='!![en]Visa number')