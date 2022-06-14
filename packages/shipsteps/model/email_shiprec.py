# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_shiprec', pkey='id', name_long='email_shiprec', name_plural='email_shiprec',caption_field='description')
        self.sysFields(tbl,counter=True)
        tbl.column('ship_rec_id',size='22', name_long='ship_rec_id'
                    ).relation('ship_rec.id', relation_name='email_shiprec', mode='foreignkey', onDelete='cascade')
        tbl.column('dest', name_short='!![en]Destination',values='to:to,cc:cc')  
        tbl.column('description', name_short='!![en]Email description')
        tbl.column('email', name_short='Email SOF')
        tbl.column('email_type', size=':3', name_short='!![en]Email type', values='to:to,cc:cc,ccn:ccn')
        