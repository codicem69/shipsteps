# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('consignee', pkey='id', name_long='!![en]Consignee-Notify', name_plural='!![en]Consignee-Notify',caption_field='fullname_cn')
        self.sysFields(tbl)

        tbl.column('name', name_short='!![en]Name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('city', name_short='!![en]City-Place')
        tbl.column('extra', name_short='!![en]Extra info')
        tbl.formulaColumn('fullname_cn',"$name || coalesce(', ' || $address, '') || coalesce(', ' || $city, '') || coalesce(', ' || $extra, '')")