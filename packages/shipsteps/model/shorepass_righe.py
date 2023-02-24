class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('shorepass_righe', pkey='id', name_long='shorepass_righe', name_plural='shorepass_righe',caption_field='id', 
                                         order_by='_row_count')
        self.sysFields(tbl,counter='shorepass_id')

        tbl.column('shorepass_id',size='22', name_long='shorepass_id'
                    ).relation('shorepass.id', relation_name='shorepass_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('name', name_short='Name')
        tbl.column('surname', name_short='Surname')
        tbl.column('rank', name_short='Rank')
        tbl.column('nationality',size='2',name_short='!![en]Nationality').relation('unlocode.nazione.code',relation_name='nationality_sp', mode='foreignkey', onDelete='raise')
        #tbl.column('nationality', name_short='Nationality')
        tbl.column('birth_date', name_short='Date of birth')
        tbl.column('birth_place', name_short='Place of birth')
        tbl.column('birth_country',size='2',name_short='!![en]Country of birth').relation('unlocode.nazione.code',relation_name='birthcountry_sp', mode='foreignkey', onDelete='raise')
        #tbl.column('birth_country', name_short='Country of birth')
        tbl.column('gender', name_short='Gender')
        tbl.column('id_doc', name_short='Identity doc')
        tbl.column('id_doc_n', name_short='Identity doc no.')
        tbl.column('id_doc_state',size='2',name_short='!![en]State identity doc').relation('unlocode.nazione.code',relation_name='docstate_sp', mode='foreignkey', onDelete='raise')
        #tbl.column('id_doc_state', name_short='State identity doc')
        tbl.column('expire_id_doc', name_short='Expiry identity doc')
        tbl.column('expire', dtype='D', name_short='expire')
        tbl.column('start_time', dtype='H', name_short='start time')
        tbl.column('stop_time', dtype='H', name_short='stop time')
        tbl.column('shorepass', dtype='B', name_short='shorepass', default=True)
        #tbl.aliasColumn('agency_id','@shorepass_id.@arrival_id.agency_id')

    def importer_con_nazioni(self, reader): 
        paesi =    self.db.table('unlocode.nazione').query(columns='$nome,$code').fetchAsDict('code') 
        for row in reader(): 
            if row['nationality']: 
                paese_id = paesi[row['nationality']]['code'] 
            else: 
                paese_id = None 
            if row['birth_country']:
                birthcountry = paesi[row['birth_country']]['code']
            else:
                birthcountry = None
            if row['doc_state']:
                stateid = paesi[row['doc_state']]['code']
            else:
                stateid = None
            
            new_crew = self.newrecord(nome=row['name'],cognome=row['surname'],grado=row['rank'],nazionalita=paese_id,
                        data_nascita=row['birth_date'],luogo_nascita=row['birth_place'],paese_nascita=birthcountry,
                        sesso=row['gender'],id_doc=row['identity_doc'],id_doc_n=row['doc_n'],id_doc_state=stateid,
                        expire_id_doc=row['expire_doc'], **row) 
            self.insert(new_crew) 
        self.db.commit()
