from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tip_mov', pkey='code', name_long='Tipologia movimentazione', name_plural='Tipologia movimentazioni',caption_field='description',lookup=True)
        self.sysFields(tbl,id=False, counter=True)
 
        tbl.column('code',name_long='!![en]Code')        
        tbl.column('description', name_short='!![en]Tip. description')

    @metadata(mandatory=True)
    def sysRecord_alimentari(self):
        return self.newrecord(code='alim', description='Alimentary')
    
    @metadata(mandatory=True)
    def sysRecord_generiche(self):
        return self.newrecord(code='gen', description='Generic')
    
    @metadata(mandatory=True)
    def sysRecord_passeggeri(self):
        return self.newrecord(code='pass',description='Passengers')