class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('beneficiario_tributi_cp', pkey='id', name_long='!![en]Tribute Beneficiary', name_plural='!![en]Tributes Beneficiary',caption_field='beneficiario',lookup=True)
        self.sysFields(tbl)

        tbl.column('beneficiario', name_short='!![en]Beneficiary')
        tbl.column('cc_posta', name_short='!![en]C/C Postal')
        tbl.column('iban', size='27',name_short='!![en]Iban code')
        
        
    
