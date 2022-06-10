# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('vessel_services', pkey='id', name_long='!![en]Vessel services', name_plural='!![en]Vessel services',caption_field='services_id')
        self.sysFields(tbl,counter=True)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='vess_services', mode='foreignkey', onDelete='cascade')
        tbl.column('services_id',size='22', name_long='!![en]Service type'
                    ).relation('services.id', relation_name='tipo_serv', mode='foreignkey', onDelete='raise')
        tbl.column('data_serv', dtype='D', name_short='!![en]Service date')
        tbl.column('descrizione', name_short='!![en]Service description')
        tbl.column('note', name_short='!![en]Internal note')
        tbl.column('nt', dtype='B', name_short='nt', default=False)
        tbl.formulaColumn('notaiterna', """CASE WHEN $nt = True then $note ELSE '' END""")
        