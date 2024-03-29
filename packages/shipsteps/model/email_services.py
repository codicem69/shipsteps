# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_services', pkey='id', name_long='!![en]Services email', name_plural='!![en]Services emails',
                       caption_field='consignee', partition_agency_id='agency_id')
        self.sysFields(tbl)
        tbl.column('agency_id',size='22', name_long='agency_id'
                    ).relation('agency.id', relation_name='email_services', mode='foreignkey', onDelete='raise')
        tbl.column('service_for_email_id',size=':7', name_long='service_for_email_id'
                    ).relation('services_for_email.code', relation_name='services_for_email', mode='foreignkey', onDelete='raise')
        tbl.column('consignee', name_short='!![en]Header Consignee')
        tbl.column('email', name_short='Email')
        tbl.column('email_cc', name_short='Email cc')
        tbl.column('email_bcc', name_short='Email bcc')
        tbl.column('email_pec', name_short='Email pec')
        tbl.column('email_cc_pec', name_short='Email cc pec')
        tbl.column('default', name_short='Default', dtype='B')

    #    tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='port_email_unlocode', 
    #                                                                    mode='foreignkey', onDelete='raise')
        tbl.aliasColumn('service_for_email','@service_for_email_id.description_serv')
       # tbl.formulaColumn('dog_int', """CASE WHEN $service_for_email = 'dogana' THEN $consignee ELSE NULL END""")
        #tbl.formulaColumn('dog_email', """CASE WHEN $service_for_email = 'dogana' THEN $email END""")
        #tbl.formulaColumn('dog_email_cc', """CASE WHEN $service_for_email = 'dogana' THEN $email_cc END""")
        

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
        