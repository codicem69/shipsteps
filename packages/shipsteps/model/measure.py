# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('measure', pkey='id', name_long='Measure', name_plural='Measures',caption_field='description', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_short='!![en]Description')
        