# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('ck_emailqtdest', pkey='id', name_long='!![en]Check Email q.ty destination', name_plural='!![en]Check Email q.ty destination',caption_field='')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', group='_', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='email_qtdest', mode='foreignkey', onDelete='raise')
        tbl.column('issued_date', dtype='DH', name_long='!![en]Issued date', name_short='!![en]Issued date')
        tbl.column('user', name_long='!![en]User', name_short='!![en]User')
        tbl.column('send_date', dtype='DH', name_long='!![en]Send date', name_short='!![en]Send date')
        