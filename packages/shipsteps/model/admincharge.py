# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('admincharge',pkey='id',name_long='Administration charge',name_plural='Administration charges',caption_field='descrizione',lookup=True)
        self.sysFields(tbl, counter=True)
        tbl.column('descrizione',name_long='Descrizione GT')
        tbl.column('importo',dtype='N',size='10,2',name_long='Importo',format='#,###.00')

    @metadata(mandatory=True)
    def sysRecord_GT_upto250(self):
        return self.newrecord(descrizione='fino a 500 GT',importo=3.10)

    @metadata(mandatory=True)
    def sysRecord_GT_501_2000(self):
        return self.newrecord(descrizione='da 501 a 2000 GT',importo=7.75)

    @metadata(mandatory=True)
    def sysRecord_GT_2001_5000(self):
        return self.newrecord(descrizione='da 2001 a 5000 GT',importo=10.35)
    
    @metadata(mandatory=True)
    def sysRecord_GT_5001_10000(self):
        return self.newrecord(descrizione='da 5001 a 10000 GT',importo=18.08)
    
    @metadata(mandatory=True)
    def sysRecord_GT_10001_30000(self):
        return self.newrecord(descrizione='da 10001 a 30000 GT',importo=23.24)
    
    @metadata(mandatory=True)
    def sysRecord_GT_30001_80000(self):
        return self.newrecord(descrizione='da 30001 a 80000 GT',importo=25.82)