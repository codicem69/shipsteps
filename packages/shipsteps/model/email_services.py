# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_services', pkey='id', name_long='!![en]Services email', name_plural='!![en]Services emails',
                       caption_field='consignee', partition_port='port')
        self.sysFields(tbl)
        tbl.column('consignee', name_short='!![en]Consignee')
        tbl.column('email', name_short='Email')
        tbl.column('email_cc', name_short='Email cc')
        tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='port_email_unlocode', 
                                                                        mode='foreignkey', onDelete='raise')

    def defaultValues(self):
        return dict(port=self.db.currentEnv.get('current_port'))
        