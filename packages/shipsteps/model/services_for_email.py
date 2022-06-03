# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('services_for_email', pkey='code', name_long='!![en]Service for email', name_plural='!![en]Services for email',
                                            caption_field='description_serv',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size=':7',name_long='!![en]Code')
        tbl.column('description_serv', name_short='!![en]Service description')
        
    @metadata(mandatory=True)
    def sysRecord_antifire(self):
        return self.newrecord(code='antfire',description_serv='antifire')

    @metadata(mandatory=True)
    def sysRecord_chemist(self):
        return self.newrecord(code='chem',description_serv='chemist')

    @metadata(mandatory=True)
    def sysRecord_dogana(self):
        return self.newrecord(code='dog',description_serv='dogana')
    
    @metadata(mandatory=True)
    def sysRecord_ens(self):
        return self.newrecord(code='ens',description_serv='ens')

    @metadata(mandatory=True)
    def sysRecord_garbage(self):
        return self.newrecord(code='garb',description_serv='garbage')

    @metadata(mandatory=True)
    def sysRecord_gdf(self):
        return self.newrecord(code='gdf',description_serv='gdf')

    @metadata(mandatory=True)
    def sysRecord_gdfroan(self):
        return self.newrecord(code='gdfroan',description_serv='gdf roan')

    @metadata(mandatory=True)
    def sysRecord_gpg(self):
        return self.newrecord(code='gpg',description_serv='gpg')

    @metadata(mandatory=True)
    def sysRecord_immigration(self):
        return self.newrecord(code='imm',description_serv='immigration')

    @metadata(mandatory=True)
    def sysRecord_mooringmen(self):
        return self.newrecord(code='moor',description_serv='mooringmen')

    @metadata(mandatory=True)
    def sysRecord_pfso(self):
        return self.newrecord(code='pfso',description_serv='pfso')

    @metadata(mandatory=True)
    def sysRecord_pilot(self):
        return self.newrecord(code='pilot',description_serv='pilot')

    @metadata(mandatory=True)
    def sysRecord_sanimare(self):
        return self.newrecord(code='usma',description_serv='sanimare')

    @metadata(mandatory=True)
    def sysRecord_tug(self):
        return self.newrecord(code='tug',description_serv='tug')

    @metadata(mandatory=True)
    def sysRecord_watersupply(self):
        return self.newrecord(code='ws',description_serv='water supply')

    @metadata(mandatory=True)
    def sysRecord_capitaneria(self):
        return self.newrecord(code='cp',description_serv='capitaneria')
    
    @metadata(mandatory=True)
    def sysRecord_adsp(self):
        return self.newrecord(code='adsp',description_serv='adsp')