# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_services', pkey='id', name_long='!![en]Services email', name_plural='!![en]Services emails',
                       caption_field='consignee', partition_agency_id='agency_id')
        self.sysFields(tbl)
        tbl.column('agency_id',size='22', name_long='agency_id'
                    ).relation('agency.id', relation_name='email_services', mode='foreignkey', onDelete='raise')
        tbl.column('service_for_email_id',size='22', name_long='service_for_email_id'
                    ).relation('services_for_email.id', relation_name='services_for_email', mode='foreignkey', onDelete='raise')
        tbl.column('consignee', name_short='!![en]Header Consignee')
        tbl.column('email', name_short='Email')
        tbl.column('email_cc', name_short='Email cc')
    #    tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='port_email_unlocode', 
    #                                                                    mode='foreignkey', onDelete='raise')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
        