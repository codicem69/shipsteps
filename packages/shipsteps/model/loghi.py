
class Table(object):
    def config_db(self,pkg):
        
        tbl=pkg.table('loghi', pkey='id', name_long='!![en]Logo', name_plural='!![en]Logos',
                                 caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('logo_cp', dtype='P', name_short='!![en]Logo CP', format='auto')
        tbl.column('logo_imm', dtype='P', name_short='!![en]Logo Immigration', format='auto')
        