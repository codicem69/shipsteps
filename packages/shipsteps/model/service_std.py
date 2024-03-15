# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('service_std', pkey='id', name_long='!![en]Standard service', name_plural='!![en]Standard services',caption_field='services_id',lookup=True)
        self.sysFields(tbl)
        
        tbl.column('services_id',size='22', group='_', name_long='!![en]Service'
                    ).relation('services.id', relation_name='servizi_nave', mode='foreignkey', onDelete='raise')
        tbl.column('descrizione', name_short='!![en]Service description')