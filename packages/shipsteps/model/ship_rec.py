# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('ship_rec', pkey='id', name_long='!![en]Shipper-Receiver', name_plural='Shippers-Receivers',caption_field='fullname_sr')
        self.sysFields(tbl)

        tbl.column('name', name_short='!![en]Name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('city', name_short='!![en]City-Place')
        tbl.formulaColumn('fullname_sr',"$name || coalesce(', ' || $address, '') || coalesce(', ' || $city, '')")
        