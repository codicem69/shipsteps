# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('prearrivals_default', pkey='id', name_long='!![en]Pre-Arrival default', 
                       name_plural='!![en]Pre-Arrivals default',caption_field='description', partition_port='port')
        self.sysFields(tbl)

        tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='portprearr_default', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('subject_email', name_short='!![en]Email Subject')
        tbl.column('body_email', name_short='!![en]Email Body')

    def defaultValues(self):
        return dict(port=self.db.currentEnv.get('current_port'))
        