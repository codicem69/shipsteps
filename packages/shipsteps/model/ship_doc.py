# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('ship_doc', pkey='id', name_long='ship_doc', name_plural='ship_doc',caption_field='cert', order_by='_row_count')
        self.sysFields(tbl, counter='vessel_details')

        tbl.column('vessel_details',size='22',name_short='!![en]vessel details'
                    ).relation('vessel_details.id',relation_name='ship_docs', mode='foreignkey', onDelete='cascade')
        tbl.column('cert',name_short='!![en]Certificate'
                    ).relation('ship_cert.code', relation_name='shipcert', mode='foreignkey', onDelete='raise')
        tbl.column('issued',size='22',name_short='!![en]Place of issue'
                    ).relation('unlocode.place.id',relation_name='issue_cert', mode='foreignkey', onDelete='raise')
        tbl.column('date_cert', dtype='D', name_short='!![en]Issue date')
        tbl.column('expire', dtype='D', name_short='!![en]Expire cert.')
        tbl.column('annual_place',size='22',name_short='!![en]Annual visit place'
                    ).relation('unlocode.place.id',relation_name='annual_visit', mode='foreignkey', onDelete='raise')
        tbl.column('annual_date', dtype='D', name_short='!![en]Annual visit date')
        tbl.column('note', name_short='!![en]Notes')
