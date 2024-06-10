from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tip_garbage', pkey='id', name_long='!![en]Garbage type', name_plural='!![en]garbage types',caption_field='description',lookup=True)
        self.sysFields(tbl, counter=True)      
        tbl.column('description', name_short='!![en]Garbage type')

    @metadata(mandatory=True)
    def sysRecord_plastic(self):
        return self.newrecord(description='A) Plastica')
    
    @metadata(mandatory=True)
    def sysRecord_food(self):
        return self.newrecord(description='B) Rifiuti alimentari')
    
    @metadata(mandatory=True)
    def sysRecord_domestic(self):
        return self.newrecord(description='C) Rifiuti domestici')
    
    @metadata(mandatory=True)
    def sysRecord_cookoil(self):
        return self.newrecord(description='D) Olio da cucina/Cooking Oil')
    
    @metadata(mandatory=True)
    def sysRecord_bilge(self):
        return self.newrecord(description='Bilge - Acque oleose di sentina')
    
    @metadata(mandatory=True)
    def sysRecord_sludge(self):
        return self.newrecord(description='Sludge - residui oleosi (fanghi)')
    
    @metadata(mandatory=True)
    def sysRecord_dirtyoil(self):
        return self.newrecord(description='Dirty oil - olio sporco')