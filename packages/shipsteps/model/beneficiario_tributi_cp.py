class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('beneficiario_tributi_cp', pkey='id', name_long='!![en]Tribute Beneficiary', name_plural='!![en]Tributes Beneficiary',caption_field='beneficiario', 
                        partition_agency_id='agency_id',lookup=True)
        self.sysFields(tbl)
        tbl.column('agency_id',size='22',name_long='!![en]Agency').relation(
                                    'agency.id',relation_name='agency_id_tributi', mode='foreignkey', onDelete='raise')
        tbl.column('beneficiario', name_short='!![en]Beneficiary')
        tbl.column('cc_posta', name_short='!![en]C/C Postal')
        tbl.column('iban', size='27',name_short='!![en]Iban code')
        
        
    